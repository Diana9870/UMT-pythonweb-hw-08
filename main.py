from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
import crud

from database import engine, Base, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Contacts API")

@app.get("/")
def read_root():
    return {"message": "API is working"}

@app.post("/contacts/", response_model=schemas.ContactResponse)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    return crud.create_contact(db, contact)


@app.get("/contacts/", response_model=list[schemas.ContactResponse])
def get_contacts(db: Session = Depends(get_db)):
    return crud.get_contacts(db)


@app.get("/contacts/{contact_id}", response_model=schemas.ContactResponse)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = crud.get_contact(db, contact_id)

    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    return contact


@app.put("/contacts/{contact_id}", response_model=schemas.ContactResponse)
def update_contact(contact_id: int, contact: schemas.ContactUpdate, db: Session = Depends(get_db)):
    updated = crud.update_contact(db, contact_id, contact)

    if not updated:
        raise HTTPException(status_code=404, detail="Contact not found")

    return updated


@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_contact(db, contact_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Contact not found")

    return {"message": "Contact deleted"}


@app.get("/contacts/search/", response_model=list[schemas.ContactResponse])
def search_contacts(
    first_name: str = None,
    last_name: str = None,
    email: str = None,
    db: Session = Depends(get_db)
):
    return crud.search_contacts(db, first_name, last_name, email)


@app.get("/contacts/birthdays/upcoming/", response_model=list[schemas.ContactResponse])
def upcoming_birthdays(db: Session = Depends(get_db)):
    return crud.upcoming_birthdays(db)