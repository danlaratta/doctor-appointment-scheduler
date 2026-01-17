from sqlalchemy import Integer, DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import TYPE_CHECKING
from app.models.base import Base 
from app.enums.appointment_status import AppointmentStatus

if TYPE_CHECKING:
    from app.models.doctor import Doctor
    from app.models.patient import Patient

class Appointment(Base):
    __tablename__ = 'appointments'

    # Columns 
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    appointment_date_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    appointment_status: Mapped[AppointmentStatus] = mapped_column(
        Enum(
            AppointmentStatus,
            name='appointmentstatus',
            native_enum=True,
            values_callable=lambda enum_cls: [e.value for e in enum_cls]
        ),
        nullable=False
    )
    duration: Mapped[int] = mapped_column(Integer, nullable=False)

    # Foreign Keys
    patient_id: Mapped[int] = mapped_column(Integer, ForeignKey('patients.id'), nullable=False)
    doctor_id: Mapped[int] = mapped_column(Integer, ForeignKey('doctors.id'), nullable=False)

    # Relationships
    patient: Mapped['Patient'] = relationship(back_populates='appointments')
    doctor: Mapped['Doctor'] = relationship(back_populates='appointments')


