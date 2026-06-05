"""Chat endpoints: status, history, send, reset."""

from __future__ import annotations

import json
import re
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..db import SessionLocal, get_db
from ..deps import current_user
from ..models import Conversation, Message, User
from ..ollama_client import (
    build_rag_query,
    chat as ollama_chat,
    chat_stream,
    check_ollama,
    format_passages,
    passages_to_citations,
    rag_system_prompt,
    report_system_prompt,
    retrieve_passages,
    system_prompt_with_profile,
)
from ..schemas import ChatIn, ChatOut, ConversationOut, MessageOut, StatusOut, StreamChatIn
from ..transcripts import append_turn
from ..config import settings

router = APIRouter(prefix="/api/chat", tags=["chat"])

_THINK_RE = re.compile(r"<think>.*?</think>", re.DOTALL)
REPORT_REQUEST_TEXT = "Please produce a structured HERA risk report for my app now."


def _profile_dict(user: User) -> dict | None:
    if user.profile is None:
        return None
    p = user.profile
    return {
        "app_name": p.app_name,
        "app_type": p.app_type,
        "app_purpose": p.app_purpose,
        "target_users": p.target_users,
        "data_collected": p.data_collected,
        "technology": p.technology,
        "has_ai": p.has_ai,
        "deployment_markets": p.deployment_markets,
        "extra_notes": p.extra_notes,
    }


def _sse(event: str | None, data: dict) -> str:
    prefix = f"event: {event}\n" if event else ""
    return f"{prefix}data: {json.dumps(data)}\n\n"


def _active_conversation(db: Session, user: User) -> Conversation:
    stmt = (
        select(Conversation)
        .where(Conversation.user_id == user.id, Conversation.is_active.is_(True))
        .order_by(Conversation.id.desc())
    )
    convo = db.execute(stmt).scalars().first()
    if convo is None:
        convo = Conversation(user_id=user.id)
        db.add(convo)
        db.commit()
        db.refresh(convo)
    return convo


@router.get("/status", response_model=StatusOut)
def status(_: User = Depends(current_user)) -> StatusOut:
    ok, msg = check_ollama()
    return StatusOut(ollama_ok=ok, ollama_status=msg, model=settings.ollama_model)


@router.get("/conversation", response_model=ConversationOut)
def get_conversation(
    user: User = Depends(current_user),
    db: Session = Depends(get_db),
) -> ConversationOut:
    convo = _active_conversation(db, user)
    return ConversationOut(
        id=convo.id,
        created_at=convo.created_at,
        messages=[MessageOut.model_validate(m) for m in convo.messages],
    )


@router.post("/message", response_model=ChatOut)
def send_message(
    payload: ChatIn,
    user: User = Depends(current_user),
    db: Session = Depends(get_db),
) -> ChatOut:
    convo = _active_conversation(db, user)

    user_msg = Message(conversation_id=convo.id, role="user", content=payload.content)
    db.add(user_msg)
    db.commit()
    db.refresh(user_msg)
    append_turn(user.email, convo.id, "user", payload.content)

    profile_dict = _profile_dict(user)

    payload_messages = [{"role": "system", "content": system_prompt_with_profile(profile_dict)}]
    payload_messages.extend(
        {"role": m.role, "content": m.content} for m in convo.messages
    )

    try:
        assistant_text = ollama_chat(payload_messages)
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    assistant_msg = Message(conversation_id=convo.id, role="assistant", content=assistant_text)
    db.add(assistant_msg)
    db.commit()
    db.refresh(assistant_msg)
    append_turn(user.email, convo.id, "assistant", assistant_text)

    return ChatOut(
        user_message=MessageOut.model_validate(user_msg),
        assistant_message=MessageOut.model_validate(assistant_msg),
        conversation_id=convo.id,
    )


@router.post("/stream")
def stream_message(
    payload: StreamChatIn,
    user: User = Depends(current_user),
    db: Session = Depends(get_db),
) -> StreamingResponse:
    """RAG-augmented, token-by-token streaming turn (mode=chat) or RLM-synthesized
    structured risk report (mode=report). Emits Server-Sent Events:
      event: meta  → {conversation_id, user_message, citations}
      data: {t}    → each generated text chunk
      event: done  → {assistant_message_id}
      event: error → {detail}
    """
    convo = _active_conversation(db, user)
    mode = payload.mode

    if mode == "report":
        user_content = REPORT_REQUEST_TEXT
    else:
        user_content = payload.content.strip()
        if not user_content:
            raise HTTPException(status_code=422, detail="Message is empty")

    # --- All DB work happens BEFORE the stream starts (the request's db session
    #     may be torn down once StreamingResponse takes over). ---
    user_msg = Message(conversation_id=convo.id, role="user", content=user_content)
    db.add(user_msg)
    db.commit()
    db.refresh(user_msg)
    append_turn(user.email, convo.id, "user", user_content)

    convo_id = convo.id
    user_email = user.email
    user_message_payload = {
        "id": user_msg.id,
        "role": "user",
        "content": user_content,
        "created_at": user_msg.created_at.isoformat(),
    }
    profile_dict = _profile_dict(user)

    history = db.execute(
        select(Message).where(Message.conversation_id == convo_id).order_by(Message.id)
    ).scalars().all()
    convo_msgs = [{"role": m.role, "content": m.content} for m in history]

    # --- Retrieval (RAG) ---
    if mode == "report":
        # Retrieve against the app pitch (first user turn), not the report request.
        rag_query = next((m["content"] for m in convo_msgs if m["role"] == "user"), "")
    else:
        rag_query = build_rag_query(convo_msgs)
    passages = retrieve_passages(rag_query)
    citations = passages_to_citations(passages)

    # --- Build the generation messages ---
    if mode == "report":
        convo_text = "\n".join(
            f"### {m['role'].upper()}\n{m['content']}"
            for m in convo_msgs
            if m["role"] != "system" and m["content"] != REPORT_REQUEST_TEXT
        )
        system = report_system_prompt() + format_passages(passages)
        gen_messages = [
            {"role": "system", "content": system},
            {
                "role": "user",
                "content": f"CONVERSATION:\n{convo_text}\n\nNow write the structured HERA risk report.",
            },
        ]
        temperature, max_tokens = 0.4, 1600
    else:
        system = rag_system_prompt(profile_dict, passages)
        gen_messages = [{"role": "system", "content": system}]
        gen_messages.extend(m for m in convo_msgs if m["role"] != "system")
        temperature, max_tokens = 0.7, 1200

    def event_stream():
        yield _sse("meta", {
            "conversation_id": convo_id,
            "user_message": user_message_payload,
            "citations": citations,
        })
        chunks: list[str] = []
        try:
            for delta in chat_stream(gen_messages, temperature=temperature, max_tokens=max_tokens):
                chunks.append(delta)
                yield _sse(None, {"t": delta})
        except RuntimeError as exc:
            yield _sse("error", {"detail": str(exc)})
            return

        full = _THINK_RE.sub("", "".join(chunks)).strip()
        assistant_id = None
        s = SessionLocal()
        try:
            am = Message(conversation_id=convo_id, role="assistant", content=full)
            s.add(am)
            s.commit()
            s.refresh(am)
            assistant_id = am.id
        finally:
            s.close()
        append_turn(user_email, convo_id, "assistant", full)
        yield _sse("done", {"assistant_message_id": assistant_id})

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@router.post("/reset", response_model=ConversationOut)
def reset_conversation(
    user: User = Depends(current_user),
    db: Session = Depends(get_db),
) -> ConversationOut:
    convo = _active_conversation(db, user)
    convo.is_active = False
    convo.ended_at = datetime.utcnow()
    new_convo = Conversation(user_id=user.id)
    db.add(new_convo)
    db.commit()
    db.refresh(new_convo)
    return ConversationOut(id=new_convo.id, created_at=new_convo.created_at, messages=[])
