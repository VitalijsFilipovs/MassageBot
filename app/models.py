from sqlalchemy import (
    Column, Integer, String, Enum, Boolean, DateTime, ForeignKey, JSON, Text, Numeric
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
import enum

from .database import Base

# app/models.py (добавь/обнови фрагменты)
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from app.database import Base

class Role(str, enum.Enum):
    admin = "admin"
    masseuse = "masseuse"
    client = "client"

class SubscriptionStatus(str, enum.Enum):
    active = "active"
    past_due = "past_due"
    canceled = "canceled"

class BookingStatus(str, enum.Enum):
    requested = "requested"
    confirmed = "confirmed"
    cancelled = "cancelled"
    done = "done"

class User(Base):
    __tablename__ = "users"
    id = sa.Column(sa.Integer, primary_key=True)
    tg_id = sa.Column(sa.BigInteger, unique=True, index=True, nullable=False)
    role = sa.Column(sa.String(16), nullable=False, server_default="client")  # admin|provider|client
    gender = sa.Column(sa.String(8))  # female|male|other
    locale = sa.Column(sa.String(5), server_default="ru")
    phone = sa.Column(sa.String(32))
    share_phone_publicly = sa.Column(sa.Boolean, nullable=False, server_default=sa.text("false"))
    is_active = sa.Column(sa.Boolean, nullable=False, server_default=sa.text("true"))
    created_at = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False)

    masseuse_profile = relationship("Masseuse", back_populates="user", uselist=False)
    client_profile = relationship("Client", back_populates="user", uselist=False)

class Masseuse(Base):
    __tablename__ = "masseuses"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    city: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text, default="")
    services: Mapped[dict] = mapped_column(JSON, default=dict)
    photos: Mapped[list] = mapped_column(JSON, default=list)
    schedule: Mapped[dict] = mapped_column(JSON, default=dict)
    subscription_status: Mapped[SubscriptionStatus] = mapped_column(Enum(SubscriptionStatus), default=SubscriptionStatus.past_due)
    paypal_subscription_id: Mapped[str] = mapped_column(String(100), nullable=True)
    last_payment_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    kyc_status: Mapped[str | None] = mapped_column(String(50), nullable=True)

    user = relationship("User", back_populates="masseuse_profile")

class Client(Base):
    __tablename__ = "clients"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    favorites: Mapped[list] = mapped_column(JSON, default=list)
    reviews: Mapped[list] = mapped_column(JSON, default=list)

    user = relationship("User", back_populates="client_profile")

class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    masseuse_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date: Mapped[str] = mapped_column(String(10))
    time: Mapped[str] = mapped_column(String(8))
    duration_min: Mapped[int] = mapped_column(Integer, default=60)
    status: Mapped[str] = mapped_column(Enum(BookingStatus), default=BookingStatus.requested)

class PaymentLog(Base):
    __tablename__ = "payments_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    masseuse_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    paypal_event: Mapped[str] = mapped_column(Text)
    amount: Mapped[Numeric] = mapped_column(Numeric(10, 2), default=0)
    currency: Mapped[str] = mapped_column(String(8), default="EUR")
    status: Mapped[str] = mapped_column(String(50), default="")
    raw_payload: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class AdminAction(Base):
    __tablename__ = "admin_actions"

    id: Mapped[int] = mapped_column(primary_key=True)
    admin_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    action_type: Mapped[str] = mapped_column(String(100))
    target_id: Mapped[str] = mapped_column(String(100))
    notes: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

# Города — как раньше
class City(Base):
    __tablename__ = "cities"
    id = sa.Column(sa.Integer, primary_key=True)
    slug = sa.Column(sa.String(64), unique=True, index=True, nullable=False)
    name_ru = sa.Column(sa.String(128), nullable=False)
    name_lv = sa.Column(sa.String(128), nullable=False)
    name_en = sa.Column(sa.String(128), nullable=False)
    is_active = sa.Column(sa.Boolean, nullable=False, server_default=sa.text("true"))

# Статусы профиля и подписки
PROFILE_STATUS = sa.Enum("pending","approved","rejected","frozen", name="profile_status")
SUB_STATUS     = sa.Enum("none","active","past_due","suspended","cancelled", name="subscription_status")

class Profile(Base):
    __tablename__ = "profiles"
    id = sa.Column(sa.Integer, primary_key=True)

    # владелец
    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    user = relationship("User")

    # привязка к городу
    city_id = sa.Column(sa.Integer, sa.ForeignKey("cities.id"), nullable=False, index=True)

    display_name = sa.Column(sa.String(128), nullable=False)
    about = sa.Column(sa.Text)
    price_from = sa.Column(sa.Integer)
    services = sa.Column(sa.JSON, nullable=False, server_default=sa.text("'[]'::jsonb"))
    photos = sa.Column(sa.JSON, nullable=False, server_default=sa.text("'[]'::jsonb"))
    gender = sa.Column(sa.String(8))  # для фильтрации клиентами

    # модерация
    status = sa.Column(PROFILE_STATUS, nullable=False, server_default="pending")
    is_published = sa.Column(sa.Boolean, nullable=False, index=True, server_default=sa.text("false"))

    # подписка
    subscription_status = sa.Column(SUB_STATUS, nullable=False, server_default="none")
    plan_id = sa.Column(sa.String(64))            # PayPal plan id
    subscription_id = sa.Column(sa.String(64))    # PayPal subscription id
    next_billing_at = sa.Column(sa.DateTime(timezone=True))
    last_payment_at = sa.Column(sa.DateTime(timezone=True))

    # контакт на карточке (по желанию)
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