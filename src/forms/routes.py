from typing import List

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from src.forms.schemas import (Form as FormSchema, Question as QuestionSchema, Option as OptionSchema)
from src.database import get_db
from src.forms.models import FormModel, QuestionModel, OptionModel
from src.users.routes import get_user

router = APIRouter(
    prefix="/forms",
    tags=["forms"]
)
 
@router.get("/", response_model=List[FormSchema])
def list_forms(db: Session = Depends(get_db)) -> List[FormSchema]:
    forms = db.query(FormModel).all()
    return forms

@router.get("/{form_id}", response_model=FormSchema)
def select_form(form_id: int, db: Session = Depends(get_db)) -> FormSchema:
    form = db.query(FormModel).filter(FormModel.id == form_id).first()
    if form is None:
        raise HTTPException(status_code=404, detail="Form not found")
    return form

@router.patch("/{form_id}", response_model=FormSchema)
def change_form(form_id: int, form_update: FormSchema, db: Session = Depends(get_db)) -> FormSchema:
    form = db.query(FormModel).filter(FormModel.id == form_id).first()
    if form is None:
        raise HTTPException(status_code=404, detail="Form not found")
    
    if form_update.title:
        form.title = form_update.title
    if form_update.description:
        form.description = form_update.description
    if form_update.questions:
        for q in form_update.questions:
            db_question = QuestionModel(text=q.text, type=q.type, form_id=form.id, allow_multiple=q.allow_multiple)
            db.add(db_question)
            db.commit()
            
            if q.options:
                for o in q.options:
                    db_option = OptionModel(text=o.text, question_id=db_question.id)
                    db.add(db_option)
                    db.commit()

    form.save(db)
    return form

@router.post("/", response_model=FormSchema)
def create_form(form: FormSchema, db: Session = Depends(get_db), user_id: int = 1):
    db_user = get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=400, detail="Invalid user ID")
    
    db_form = FormModel(title=form.title, description=form.description, owner_id=db_user.id)
    db.add(db_form)
    db.commit()
    db.refresh(db_form)
    
    for q in form.questions:
        db_question = QuestionModel(text=q.text, type=q.type, form_id=db_form.id, allow_multiple=q.allow_multiple)
        db.add(db_question)
        db.commit()
        db.refresh(db_question)

        if q.options:
            for o in q.options:
                db_option = OptionModel(text=o.text, question_id=db_question.id)
                db.add(db_option)
                db.commit()
                db.refresh(db_option)
    
    return db_form

@router.delete("/{form_id}")
def delete_form(form_id: int, db: Session = Depends(get_db)):
    form = db.query(FormModel).filter(FormModel.id == form_id).first()
    if form is None:
        raise HTTPException(status_code=404, detail="Form not found")
    
    for question in form.questions:
        for option in question.options:
            db.delete(option)
            db.commit()
        db.delete(question)
        db.commit()
    
    db.delete(form)
    db.commit()
    return {"detail": "Form deleted successfully"}
