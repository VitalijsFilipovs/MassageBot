from sqlalchemy import (
    Column, Integer, String, Enum, Boolean, DateTime, ForeignKey, JSON, Text, Numeric
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
import enum

from .database import Base

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

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    telegram_id: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=True)
    phone: Mapped[str] = mapped_column(String(32), unique=True, nullable=True)
    role: Mapped[Role] = mapped_column(Enum(Role), nullable=False)
    name_display: Mapped[str] = mapped_column(String(120), nullable=True)
    email: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

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
