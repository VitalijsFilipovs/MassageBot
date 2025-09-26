# app/utils/seed.py
from datetime import datetime
from app.database import SessionLocal
from app import models

def run():
    db = SessionLocal()
    try:
        # Пользователь-массажистка
        u = models.User(
            telegram_id="seed_m1",
            phone=None,
            role="masseuse",
            name_display="Alina",
            email=None,
            is_active=True,
        )
        db.add(u)
        db.flush()  # чтобы получить u.id

        m = models.Masseuse(
            user_id=u.id,
            city="Рига",
            description="Классический, расслабляющий, антицеллюлитный",
            services=["classic", "relax", "anticellulite"],
            photos=[],
            schedule={"mon_fri": "10:00-19:00"},
            subscription_status="active",
            paypal_subscription_id=None,
            last_payment_at=datetime.utcnow(),
            kyc_status=None,
        )
        db.add(m)

        # Ещё одна для примера
        u2 = models.User(
            telegram_id="seed_m2",
            role="masseuse",
            name_display="Marina",
            is_active=True,
        )
        db.add(u2); db.flush()
        m2 = models.Masseuse(
            user_id=u2.id,
            city="Юрмала",
            description="Тайский, спортивный",
            services=["thai", "sport"],
            schedule={"sat_sun": "12:00-18:00"},
            subscription_status="active",
        )
        db.add(m2)

        db.commit()
        print("Seed done")
    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    run()
