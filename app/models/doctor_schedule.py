from sqlalchemy import Integer, Time, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import time
from typing import TYPE_CHECKING
from app.models.base import Base 

if TYPE_CHECKING:
    from app.models.doctor import Doctor

class DoctorSchedule(Base):
    __tablename__ = 'doctor_schedules'

    # Columns 
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    weekday_start_time: Mapped[time] = mapped_column(Time, nullable=False)   # Allow null for weekday/weekend for doctor's off days
    weekday_end_time: Mapped[time] = mapped_column(Time, nullable=False)
    weekend_start_time: Mapped[time] = mapped_column(Time, nullable=True)
    weekend_end_time: Mapped[time] = mapped_column(Time, nullable=True)    

    # Foreign Key
    doctor_id: Mapped[int] = mapped_column(Integer, ForeignKey('doctors.id', ondelete='cascade'), unique=True, nullable=False)

    # Relationships
    doctor: Mapped['Doctor'] = relationship(back_populates='doctor_schedule')

