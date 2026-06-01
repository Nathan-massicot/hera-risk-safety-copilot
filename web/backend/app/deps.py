"""FastAPI dependencies."""

from __future__ import annotations

from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .config import settings
from .db import get_db
from .models import User
from .security import get_active_session


def current_user(
    db: Session = Depends(get_db),
    session_token: str | None = Cookie(default=None, alias=settings.session_cookie_name),
) -> User:
    session = get_active_session(db, session_token)
    if session is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )
    user = db.get(User, session.user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Account no longer exists"
        )
    return user


def onboarded_user(user: User = Depends(current_user)) -> User:
    if not user.onboarded:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Onboarding not completed"
        )
    return user
