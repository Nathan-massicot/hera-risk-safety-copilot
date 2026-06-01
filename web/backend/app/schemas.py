"""Pydantic request/response schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

class LoginIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1)
    remember_me: bool = False


class RegisterIn(BaseModel):
    invite_token: str = Field(min_length=8)
    email: EmailStr
    password: str = Field(min_length=10, max_length=200)


class UserOut(BaseModel):
    id: int
    email: EmailStr
    onboarded: bool
    consent_given: bool
    created_at: datetime

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Onboarding
# ---------------------------------------------------------------------------

class OnboardingIn(BaseModel):
    app_name: str = Field(min_length=1, max_length=255)
    app_type: str = Field(min_length=1, max_length=120)
    app_purpose: str = Field(min_length=1)
    target_users: str = Field(min_length=1)
    data_collected: str = Field(min_length=1)
    technology: str = Field(min_length=1)
    has_ai: bool = False
    deployment_markets: str = Field(min_length=1)
    extra_notes: str | None = None
    consent: bool


class OnboardingOut(BaseModel):
    app_name: str
    app_type: str
    app_purpose: str
    target_users: str
    data_collected: str
    technology: str
    has_ai: bool
    deployment_markets: str
    extra_notes: str | None
    updated_at: datetime

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Chat
# ---------------------------------------------------------------------------

class MessageOut(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ChatIn(BaseModel):
    content: str = Field(min_length=1, max_length=8000)


class ChatOut(BaseModel):
    user_message: MessageOut
    assistant_message: MessageOut
    conversation_id: int


class ConversationOut(BaseModel):
    id: int
    created_at: datetime
    messages: list[MessageOut]


class StatusOut(BaseModel):
    ollama_ok: bool
    ollama_status: str
    model: str
