"""Onboarding profile + consent capture."""

from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from ..deps import current_user
from ..models import OnboardingProfile, User
from ..schemas import OnboardingIn, OnboardingOut

router = APIRouter(prefix="/api/onboarding", tags=["onboarding"])


@router.get("", response_model=OnboardingOut | None)
def get_profile(
    user: User = Depends(current_user),
    db: Session = Depends(get_db),
) -> OnboardingProfile | None:
    return user.profile


@router.post("", response_model=OnboardingOut)
def upsert_profile(
    payload: OnboardingIn,
    user: User = Depends(current_user),
    db: Session = Depends(get_db),
) -> OnboardingProfile:
    if not payload.consent:
        raise HTTPException(
            status_code=400,
            detail="Consent is required to use the HERA Copilot for this research project.",
        )

    profile = user.profile
    if profile is None:
        profile = OnboardingProfile(user_id=user.id, **payload.model_dump(exclude={"consent"}))
        db.add(profile)
    else:
        for field, value in payload.model_dump(exclude={"consent"}).items():
            setattr(profile, field, value)

    user.consent_given = True
    user.consent_at = datetime.utcnow()
    user.onboarded = True

    db.commit()
    db.refresh(profile)
    return profile
