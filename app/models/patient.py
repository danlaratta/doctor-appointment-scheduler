from sqlalchemy import Integer, String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from datetime import date
from app.models.base import Base 

if TYPE_CHECKING:
    from app.models.appointment import Appointment

class Patient(Base):
    __tablename__ = 'patients'

    # Columns 
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String(15), nullable=False)


    # Relationships
    appointments: Mapped[list['Appointment']] = relationship(back_populates='patieent', cascade='all delete-orphan', lazy='selectin')
    

