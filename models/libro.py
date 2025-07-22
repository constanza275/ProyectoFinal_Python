from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Libro(Base):
    __tablename__ = "libros"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    autor = Column(String, nullable=False)
    disponible = Column(Boolean, default=True)
