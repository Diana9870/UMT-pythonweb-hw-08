from sqlalchemy.orm import Session
from datetime import date
import models
import schemas


def create_contact(db: Session, contact: schemas.ContactCreate):
    db_contact = models.Contact(**contact.model_dump())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def get_contacts(db: Session):
    return db.query(models.Contact).all()


def get_contact(db: Session, contact_id: int):
    return db.query(models.Contact).filter(
        models.Contact.id == contact_id
    ).first()


def update_contact(db: Session, contact_id: int, contact: schemas.ContactUpdate):
    db_contact = get_contact(db, contact_id)

    if not db_contact:
        return None

    for key, value in contact.model_dump().items():
        setattr(db_contact, key, value)

    db.commit()
    db.refresh(db_contact)
    return db_contact


def delete_contact(db: Session, contact_id: int):
    db_contact = get_contact(db, contact_id)

    if not db_contact:
        return None

    db.delete(db_contact)
    db.commit()
    return db_contact


def search_contacts(db: Session, first_name=None, last_name=None, email=None):
    query = db.query(models.Contact)

    if first_name:
        query = query.filter(models.Contact.first_name.ilike(f"%{first_name}%"))

    if last_name:
        query = query.filter(models.Contact.last_name.ilike(f"%{last_name}%"))

    if email:
        query = query.filter(models.Contact.email.ilike(f"%{email}%"))

    return query.all()


def upcoming_birthdays(db: Session):
    today = date.today()
    result = []

    contacts = db.query(models.Contact).all()

    for contact in contacts:
        birthday = contact.birthday.replace(year=today.year)

        if birthday < today:
            birthday = birthday.replace(year=today.year + 1)

        delta = (birthday - today).days

        if 0 <= delta <= 7:
            result.append(contact)

    return result