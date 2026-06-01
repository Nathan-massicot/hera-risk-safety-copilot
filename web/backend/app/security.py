"""Password hashing, session tokens, rate limiting."""

from __future__ import annotations

import secrets
from datetime import datetime, timedelta

import bcrypt
from sqlalchemy import select
from sqlalchemy.orm import Session

from .config import settings
from .models import LoginAttempt, UserSession


# ---------------------------------------------------------------------------
# Password hashing
# ---------------------------------------------------------------------------

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=settings.bcrypt_rounds)
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
    except ValueError:
        return False


# ---------------------------------------------------------------------------
# Session tokens
# ---------------------------------------------------------------------------

def new_token(nbytes: int = 32) -> str:
    return secrets.token_urlsafe(nbytes)


def create_session(db: Session, user_id: int, remember_me: bool) -> UserSession:
    if remember_me:
        lifetime = timedelta(days=settings.remember_me_lifetime_days)
    else:
        lifetime = timedelta(hours=settings.session_lifetime_hours)
    session = UserSession(
        id=new_token(),
        user_id=user_id,
        expires_at=datetime.utcnow() + lifetime,
        remember_me=remember_me,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def revoke_session(db: Session, token: str) -> None:
    session = db.get(UserSession, token)
    if session is not None:
        db.delete(session)
        db.commit()


def get_active_session(db: Session, token: str | None) -> UserSession | None:
    if not token:
        return None
    session = db.get(UserSession, token)
    if session is None:
        return None
    if session.expires_at < datetime.utcnow():
        db.delete(session)
        db.commit()
        return None
    return session


# ---------------------------------------------------------------------------
# Login rate limiting (simple SQL-backed window)
# ---------------------------------------------------------------------------

def record_login_attempt(db: Session, email: str, ip: str, success: bool) -> None:
    db.add(LoginAttempt(email=email.lower(), ip=ip, success=success))
    db.commit()


def is_rate_limited(db: Session, email: str, ip: str) -> bool:
    window_start = datetime.utcnow() - timedelta(minutes=settings.login_window_minutes)
    stmt = (
        select(LoginAttempt)
        .where(
            LoginAttempt.attempted_at >= window_start,
            LoginAttempt.success.is_(False),
            (LoginAttempt.email == email.lower()) | (LoginAttempt.ip == ip),
        )
    )
    failed = db.execute(stmt).scalars().all()
    return len(failed) >= settings.login_max_attempts
