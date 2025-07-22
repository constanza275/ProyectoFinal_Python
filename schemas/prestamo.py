from pydantic import BaseModel
from datetime import datetime

class PrestamoBase(BaseModel):
    usuario_id: int
    libro_id: int


class PrestamoCreate(PrestamoBase):
    pass

class PrestamoOut(PrestamoBase):
    id: int
    usuario_id: int
    libro_id: int
    fecha_prestamo: datetime
    fecha_devolucion: datetime

    class Config:
        orm_mode = True
