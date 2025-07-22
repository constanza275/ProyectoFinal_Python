from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.prestamo import Prestamo
from models.libro import Libro
from schemas.prestamo import PrestamoCreate, PrestamoOut
from typing import List
from datetime import datetime, timedelta

router = APIRouter(prefix="/prestamos", tags=["prestamos"])

@router.post("/", response_model=PrestamoOut)
def crear_prestamo(data: PrestamoCreate, db: Session = Depends(get_db)):
    libro = db.query(Libro).filter(Libro.id == data.libro_id).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    if not libro.disponible:
        raise HTTPException(status_code=400, detail="El libro no está disponible")
    
    fecha_prestamo = datetime.utcnow()
    fecha_devolucion_estimada = fecha_prestamo + timedelta(days=5)


    prestamo = Prestamo(
        usuario_id=data.usuario_id,
        libro_id=data.libro_id,
        fecha_prestamo=datetime.utcnow(),
        fecha_devolucion=fecha_devolucion_estimada
    )
    libro.disponible = False  # Marca como no disponible
    db.add(prestamo)
    db.commit()
    db.refresh(prestamo)
    return prestamo

@router.get("/", response_model=List[PrestamoOut])
def listar_prestamos(db: Session = Depends(get_db)):
    return db.query(Prestamo).all()

@router.post("/{prestamo_id}/devolver", response_model=PrestamoOut)
def devolver_prestamo(prestamo_id: int, db: Session = Depends(get_db)):
    prestamo = db.query(Prestamo).filter(Prestamo.id == prestamo_id).first()
    if not prestamo:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    if prestamo.fecha_devolucion:
        raise HTTPException(status_code=400, detail="El libro ya fue devuelto")

    prestamo.fecha_devolucion = datetime.utcnow()

    libro = db.query(Libro).filter(Libro.id == prestamo.libro_id).first()
    if libro:
        libro.disponible = True

    db.commit()
    db.refresh(prestamo)
    return prestamo