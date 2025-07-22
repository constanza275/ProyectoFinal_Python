from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.libro import Libro
from schemas.libro import LibroCreate, LibroOut
from typing import List

router = APIRouter(prefix="/libros", tags=["libros"])

@router.post("/", response_model=LibroOut)
def crear_libro(libro: LibroCreate, db: Session = Depends(get_db)):
    nuevo_libro = Libro(titulo=libro.titulo, autor=libro.autor, disponible=True)
    db.add(nuevo_libro)
    db.commit()
    db.refresh(nuevo_libro)
    return nuevo_libro

@router.get("/", response_model=List[LibroOut])
def listar_libros(db: Session = Depends(get_db)):
    return db.query(Libro).all()

@router.get("/{libro_id}", response_model=LibroOut)
def obtener_libro(libro_id: int, db: Session = Depends(get_db)):
    libro = db.query(Libro).filter(Libro.id == libro_id).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro

