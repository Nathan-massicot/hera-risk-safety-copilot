"""Login, logout, register-with-invite, and current-user endpoints."""

from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..config import settings
from ..db import get_db
from ..deps import current_user
from ..models import InviteToken, OnboardingProfile, User
from ..schemas import LoginIn, RegisterIn, UserOut
from ..security import (
    create_session,
    hash_password,
    is_rate_limited,
    new_token,
    record_login_attempt,
    revoke_session,
    verify_password,
)

# A pre-filled mHealth app for the one-click demo account: spans EU + Swiss law
# and uses AI, so the copilot has rich GDPR / MDR / AI-Act / nFADP material to
# retrieve and reason over.
DEMO_PROFILE = {
    "app_name": "CardioCompanion",
    "app_type": "Chronic-condition self-management",
    "app_purpose": (
        "Help patients with hypertension track blood pressure and medication "
        "adherence, with AI-generated lifestyle tips."
    ),
    "target_users": "Adults (40+) with diagnosed hypertension in the EU and Switzerland",
    "data_collected": (
        "Blood pressure readings, heart rate, medication logs, weight, "
        "free-text symptom notes"
    ),
    "technology": "React Native app, cloud backend, an LLM for the tip generator",
    "has_ai": True,
    "deployment_markets": "EU (Germany, France) and Switzerland",
    "extra_notes": "Considering a future SaMD classification; not yet CE-marked.",
}

router = APIRouter(prefix="/api/auth", tags=["auth"])


def _set_session_cookie(response: Response, token: str, remember_me: bool) -> None:
    if remember_me:
        max_age = settings.remember_me_lifetime_days * 24 * 3600
    else:
        max_age = settings.session_lifetime_hours * 3600
    response.set_cookie(
        key=settings.session_cookie_name,
        value=token,
        max_age=max_age,
        httponly=True,
        secure=False,  # localhost — flip to True behind HTTPS
        samesite="lax",
        path="/",
    )


def _client_ip(request: Request) -> str:
    return request.client.host if request.client else "unknown"


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterIn, db: Session = Depends(get_db)) -> User:
    # Registration is open: anyone can sign up with email + password. An invite
    # token is optional — if one is supplied it is validated and consumed.
    invite: InviteToken | None = None
    if payload.invite_token:
        invite = db.get(InviteToken, payload.invite_token)
        if invite is None:
            raise HTTPException(status_code=400, detail="Invalid invite token")
        if invite.used_by_user_id is not None:
            raise HTTPException(status_code=400, detail="Invite token already used")
        if invite.expires_at is not None and invite.expires_at < datetime.utcnow():
            raise HTTPException(status_code=400, detail="Invite token expired")

    email = payload.email.lower()
    existing = db.execute(select(User).where(User.email == email)).scalar_one_or_none()
    if existing is not None:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(email=email, password_hash=hash_password(payload.password))
    db.add(user)
    db.flush()  # populate user.id
    if invite is not None:
        invite.used_by_user_id = user.id
        invite.used_at = datetime.utcnow()
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=UserOut)
def login(
    payload: LoginIn,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
) -> User:
    ip = _client_ip(request)
    if is_rate_limited(db, payload.email, ip):
        raise HTTPException(
            status_code=429,
            detail=(
                f"Too many failed attempts. Try again in "
                f"{settings.login_window_minutes} minutes."
            ),
        )

    email = payload.email.lower()
    user = db.execute(select(User).where(User.email == email)).scalar_one_or_none()
    if user is None or not verify_password(payload.password, user.password_hash):
        record_login_attempt(db, email, ip, success=False)
        raise HTTPException(status_code=401, detail="Invalid email or password")

    record_login_attempt(db, email, ip, success=True)
    session = create_session(db, user_id=user.id, remember_me=payload.remember_me)
    _set_session_cookie(response, session.id, payload.remember_me)
    return user


@router.get("/demo-login")
def demo_login(db: Session = Depends(get_db)) -> Response:
    """One-click magic link (demo mode only): log into a pre-onboarded demo
    account and land straight on the chatbot. Disabled unless HERA_DEMO_MODE."""
    if not settings.demo_mode:
        raise HTTPException(status_code=404, detail="Not found")

    email = settings.demo_email.lower()
    user = db.execute(select(User).where(User.email == email)).scalar_one_or_none()
    if user is None:
        user = User(
            email=email,
            password_hash=hash_password(new_token(16)),  # random — login is via the link
            onboarded=True,
            consent_given=True,
            consent_at=datetime.utcnow(),
        )
        db.add(user)
        db.flush()  # populate user.id
        db.add(OnboardingProfile(user_id=user.id, **DEMO_PROFILE))
        db.commit()
        db.refresh(user)

    session = create_session(db, user_id=user.id, remember_me=True)
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    _set_session_cookie(response, session.id, remember_me=True)
    return response


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
) -> Response:
    token = request.cookies.get(settings.session_cookie_name)
    if token:
        revoke_session(db, token)
    response.delete_cookie(settings.session_cookie_name, path="/")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(current_user)) -> User:
    return user
