# app/models.py
from __future__ import annotations

import enum
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# ---- Enums (ровно те значения, с которыми работает API/бот) ----
class Role(str, enum.Enum):
    admin = "admin"
    provider = "provider"
    client = "client"

# для поля profiles.status
PROFILE_STATUS = sa.Enum("pending", "approved", "rejected", "frozen", name="profile_status")

# для поля profiles.subscription_status
SUB_STATUS = sa.Enum("none", "active", "past_due", "suspended", "cancelled", name="subscription_status")


# -------------------- Core tables --------------------
class User(Base):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True)
    tg_id = sa.Column(sa.BigInteger, unique=True, index=True, nullable=False)

    # admin | provider | client
    role = sa.Column(sa.String(16), nullable=False, server_default="client")

    gender = sa.Column(sa.String(8))                     # female|male|other
    locale = sa.Column(sa.String(5), server_default="ru")
    phone = sa.Column(sa.String(32))
    share_phone_publicly = sa.Column(sa.Boolean, nullable=False, server_default=sa.text("false"))
    is_active = sa.Column(sa.Boolean, nullable=False, server_default=sa.text("true"))

    created_at = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False)

    # связь с профилем (1:1)
    profile = relationship("Profile", uselist=False, back_populates="user")


class City(Base):
    __tablename__ = "cities"

    id = sa.Column(sa.Integer, primary_key=True)
    slug = sa.Column(sa.String(64), unique=True, index=True, nullable=False)
    name_ru = sa.Column(sa.String(128), nullable=False)
    name_lv = sa.Column(sa.String(128), nullable=False)
    name_en = sa.Column(sa.String(128), nullable=False)
    is_active = sa.Column(sa.Boolean, nullable=False, server_default=sa.text("true"))


class Profile(Base):
    __tablename__ = "profiles"

    id = sa.Column(sa.Integer, primary_key=True)

    # владелец
    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    user = relationship("User", back_populates="profile")

    # привязка к городу
    city_id = sa.Column(sa.Integer, sa.ForeignKey("cities.id"), nullable=False, index=True)

    display_name = sa.Column(sa.String(128), nullable=False)
    about = sa.Column(sa.Text)
    price_from = sa.Column(sa.Integer)
    services = sa.Column(sa.JSON, nullable=False, server_default=sa.text("'[]'::jsonb"))
    photos = sa.Column(sa.JSON, nullable=False, server_default=sa.text("'[]'::jsonb"))
    gender = sa.Column(sa.String(8))  # фильтрация клиентами

    # модерация
    status = sa.Column(PROFILE_STATUS, nullable=False, server_default="pending")
    is_published = sa.Column(sa.Boolean, nullable=False, index=True, server_default=sa.text("false"))

    # подписка
    subscription_status = sa.Column(SUB_STATUS, nullable=False, server_default="none")
    plan_id = sa.Column(sa.String(64))         # PayPal plan id
    subscription_id = sa.Column(sa.String(64)) # PayPal subscription id
    next_billing_at = sa.Column(sa.DateTime(timezone=True))
    last_payment_at = sa.Column(sa.DateTime(timezone=True))

    # контакт (по желанию показывается на карточке)
    phone_public = sa.Column(sa.String(32))
    share_phone_publicly = sa.Column(sa.Boolean, nullable=False, server_default=sa.text("false"))

    created_at = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False)
    updated_at = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False)


class Favorite(Base):
    __tablename__ = "favorites"

    id = sa.Column(sa.Integer, primary_key=True)
    client_user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    profile_id = sa.Column(sa.Integer, sa.ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    created_at = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False)

    __table_args__ = (
        sa.UniqueConstraint("client_user_id", "profile_id", name="uq_fav_client_profile"),
    )


class PaymentLog(Base):
    __tablename__ = "payments_logs"

    id = sa.Column(sa.Integer, primary_key=True)
    masseuse_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"))
    paypal_event = sa.Column(sa.Text)
    amount = sa.Column(sa.Numeric(10, 2), server_default="0")
    currency = sa.Column(sa.String(8), server_default="EUR")
    status = sa.Column(sa.String(50), server_default="")
    raw_payload = sa.Column(sa.JSON, server_default=sa.text("'{}'::jsonb"))
    created_at = sa.Column(sa.DateTime, default=datetime.utcnow)


class AdminAction(Base):
    __tablename__ = "admin_actions"

    id = sa.Column(sa.Integer, primary_key=True)
    admin_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"))
    action_type = sa.Column(sa.String(100))
    target_id = sa.Column(sa.String(100))
    notes = sa.Column(sa.Text, server_default="")
    created_at = sa.Column(sa.DateTime, default=datetime.utcnow)
