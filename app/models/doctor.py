from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from app.models.base import Base 

if TYPE_CHECKING:
    from app.models.appointment import Appointment 
    from app.models.doctor_schedule import DoctorSchedule

class Doctor(Base):
    __tablename__ = 'doctors'

    # Columns 
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    # Relationships
    appointments: Mapped[list['Appointment']] = relationship(back_populates='doctor', cascade='all delete-orphan', lazy='selectin')
    doctor_schedule: Mapped['DoctorSchedule'] = relationship(back_populates='doctor', uselist=False, cascade='all, delete-orphan')
