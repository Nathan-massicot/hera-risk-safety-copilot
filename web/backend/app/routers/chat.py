"""Chat endpoints: status, history, send, reset."""

from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..db import get_db
from ..deps import onboarded_user
from ..models import Conversation, Message, User
from ..ollama_client import chat as ollama_chat
from ..ollama_client import check_ollama, system_prompt_with_profile
from ..schemas import ChatIn, ChatOut, ConversationOut, MessageOut, StatusOut
from ..transcripts import append_turn
from ..config import settings

router = APIRouter(prefix="/api/chat", tags=["chat"])


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
def status(_: User = Depends(onboarded_user)) -> StatusOut:
    ok, msg = check_ollama()
    return StatusOut(ollama_ok=ok, ollama_status=msg, model=settings.ollama_model)


@router.get("/conversation", response_model=ConversationOut)
def get_conversation(
    user: User = Depends(onboarded_user),
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
    user: User = Depends(onboarded_user),
    db: Session = Depends(get_db),
) -> ChatOut:
    convo = _active_conversation(db, user)

    user_msg = Message(conversation_id=convo.id, role="user", content=payload.content)
    db.add(user_msg)
    db.commit()
    db.refresh(user_msg)
    append_turn(user.email, convo.id, "user", payload.content)

    profile_dict = (
        {
            "app_name": user.profile.app_name,
            "app_type": user.profile.app_type,
            "app_purpose": user.profile.app_purpose,
            "target_users": user.profile.target_users,
            "data_collected": user.profile.data_collected,
            "technology": user.profile.technology,
            "has_ai": user.profile.has_ai,
            "deployment_markets": user.profile.deployment_markets,
            "extra_notes": user.profile.extra_notes,
        }
        if user.profile is not None
        else None
    )

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


@router.post("/reset", response_model=ConversationOut)
def reset_conversation(
    user: User = Depends(onboarded_user),
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
