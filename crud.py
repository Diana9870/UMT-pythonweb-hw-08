# crud.py
from sqlalchemy.orm import Session
from datetime import date, timedelta
import models, schemas

# -------------------------
# CREATE
# -------------------------
def create_contact(db: Session, contact: schemas.ContactCreate):
    db_contact = models.Contact(
        first_name=contact.first_name,
        last_name=contact.last_name,
        email=contact.email,
        phone=contact.phone,
        birthday=contact.birthday,
        extra_data=contact.extra_data
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

# -------------------------
# READ ALL
# -------------------------
def get_contacts(db: Session):
    return db.query(models.Contact).all()

# -------------------------
# READ ONE
# -------------------------
def get_contact(db: Session, contact_id: int):
    return db.query(models.Contact).filter(models.Contact.id == contact_id).first()

# -------------------------
# UPDATE
# -------------------------
def update_contact(db: Session, contact_id: int, data: schemas.ContactUpdate):
    contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if not contact:
        return None
    # оновлюємо тільки передані поля
    for field, value in data.dict(exclude_unset=True).items():
        setattr(contact, field, value)
    db.commit()
    db.refresh(contact)
    return contact

# -------------------------
# DELETE
# -------------------------
def delete_contact(db: Session, contact_id: int):
    contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if not contact:
        return None
    db.delete(contact)
    db.commit()
    return contact

# -------------------------
# SEARCH
# -------------------------
def search_contacts(db: Session, query: str):
    return db.query(models.Contact).filter(
        (models.Contact.first_name.ilike(f"%{query}%")) |
        (models.Contact.last_name.ilike(f"%{query}%")) |
        (models.Contact.email.ilike(f"%{query}%"))
    ).all()

# -------------------------
# UPCOMING BIRTHDAYS (7 днів)
# -------------------------
def upcoming_birthdays(db: Session):
    today = date.today()
    next_week = today + timedelta(days=7)
    contacts = db.query(models.Contact).all()
    upcoming = []
    for c in contacts:
        # беремо день і місяць дати народження
        birthday_this_year = c.birthday.replace(year=today.year)
        if today <= birthday_this_year <= next_week:
            upcoming.append(c)
    return upcoming