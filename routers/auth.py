from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from auth.hash import verify_password
from auth.jwt import create_access_token
from models.usuario import Usuario
from database import get_db
from schemas.usuario import Token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.email == form_data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}