"""Admin CLI for the HERA web app: invite tokens, user management.

Usage (after `uv sync --extra web`):
    uv run hera-cli invite create --note "Supervisor"
    uv run hera-cli invite list
    uv run hera-cli user list
    uv run hera-cli user reset-password me@example.com
"""

from __future__ import annotations

from datetime import datetime, timedelta

import typer
from sqlalchemy import select

from .app.db import SessionLocal, init_db
from .app.models import InviteToken, User
from .app.security import hash_password, new_token

app = typer.Typer(help="HERA Copilot admin CLI")
invite_app = typer.Typer(help="Manage invite tokens")
user_app = typer.Typer(help="Manage users")
app.add_typer(invite_app, name="invite")
app.add_typer(user_app, name="user")


@app.callback()
def _bootstrap() -> None:
    init_db()


# --- Invites ---------------------------------------------------------------

@invite_app.command("create")
def invite_create(
    note: str = typer.Option("", help="Free-form note (recipient name, etc.)"),
    expires_days: int = typer.Option(14, help="Days until the invite expires (0 = never)"),
) -> None:
    """Generate a new invite token."""
    with SessionLocal() as db:
        token = InviteToken(
            token=new_token(24),
            note=note or None,
            expires_at=(
                datetime.utcnow() + timedelta(days=expires_days) if expires_days > 0 else None
            ),
        )
        db.add(token)
        db.commit()
        typer.echo(f"Invite token: {token.token}")
        typer.echo(f"Expires at:   {token.expires_at or 'never'}")
        if note:
            typer.echo(f"Note:         {note}")


@invite_app.command("list")
def invite_list() -> None:
    with SessionLocal() as db:
        invites = db.execute(select(InviteToken).order_by(InviteToken.created_at)).scalars().all()
        if not invites:
            typer.echo("No invites yet.")
            return
        for inv in invites:
            used = "USED" if inv.used_by_user_id else "free"
            exp = inv.expires_at.isoformat() if inv.expires_at else "no expiry"
            typer.echo(f"{inv.token}  [{used}]  expires={exp}  note={inv.note or ''}")


# --- Users -----------------------------------------------------------------

@user_app.command("list")
def user_list() -> None:
    with SessionLocal() as db:
        users = db.execute(select(User).order_by(User.created_at)).scalars().all()
        if not users:
            typer.echo("No users yet.")
            return
        for u in users:
            flags = []
            if u.onboarded:
                flags.append("onboarded")
            if u.consent_given:
                flags.append("consent")
            typer.echo(f"{u.id:>3}  {u.email:<40}  {','.join(flags) or '-'}")


@user_app.command("reset-password")
def user_reset_password(email: str, new_password: str) -> None:
    if len(new_password) < 10:
        typer.echo("Password must be at least 10 characters.", err=True)
        raise typer.Exit(code=1)
    with SessionLocal() as db:
        user = db.execute(select(User).where(User.email == email.lower())).scalar_one_or_none()
        if user is None:
            typer.echo(f"No user with email {email}", err=True)
            raise typer.Exit(code=1)
        user.password_hash = hash_password(new_password)
        db.commit()
        typer.echo(f"Password updated for {user.email}")


if __name__ == "__main__":
    app()
