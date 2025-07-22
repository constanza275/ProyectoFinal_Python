from pydantic import BaseModel

class LibroBase(BaseModel):
    titulo: str
    autor: str

class LibroCreate(LibroBase):
    pass

class LibroOut(LibroBase):
    id: int
    disponible: bool

    class Config:
        orm_mode = True
