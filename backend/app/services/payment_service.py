from datetime import date, datetime

from sqlalchemy import select, update
from sqlalchemy.orm import Session, joinedload

from app.models.contract import Contract
from app.models.payment import Payment
from app.schemas.payment import PaymentCreate, PaymentMarkPaid


def list_payments(db: Session, status: str | None = None) -> list[Payment]:
    refresh_overdue_payments(db)
    stmt = (
        select(Payment)
        .options(joinedload(Payment.contract))
        .order_by(Payment.due_date.asc())
    )
    if status:
        stmt = stmt.where(Payment.status == status)
    return list(db.scalars(stmt).all())


def create_payment(db: Session, payload: PaymentCreate) -> Payment:
    contract = db.get(Contract, payload.contract_id)
    if not contract:
        raise ValueError("contract_not_found")
    payment = Payment(**payload.model_dump(), status="unpaid")
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment


def mark_payment_paid(db: Session, payment_id: int, payload: PaymentMarkPaid) -> tuple[Payment | None, bool]:
    payment = db.get(Payment, payment_id)
    if not payment:
        return None, False
    if payment.status == "paid":
        return payment, True
    update_values = {"status": "paid", "paid_at": datetime.utcnow(), "method": payload.method}
    if payload.note is not None:
        update_values["note"] = payload.note
    result = db.execute(
        update(Payment)
        .where(Payment.id == payment_id, Payment.status != "paid")
        .values(**update_values)
    )
    db.commit()
    affected_rows = result.rowcount
    db.refresh(payment)
    already_paid = affected_rows == 0
    return payment, already_paid


def overdue_payments(db: Session) -> list[Payment]:
    refresh_overdue_payments(db)
    stmt = (
        select(Payment)
        .options(joinedload(Payment.contract))
        .where(Payment.status == "overdue")
        .order_by(Payment.due_date.asc())
    )
    return list(db.scalars(stmt).all())


def refresh_overdue_payments(db: Session) -> None:
    today = date.today()
    payments = db.scalars(
        select(Payment).where(Payment.status == "unpaid", Payment.due_date < today)
    ).all()
    for payment in payments:
        payment.status = "overdue"
    if payments:
        db.commit()
