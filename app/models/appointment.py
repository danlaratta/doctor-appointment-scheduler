from sqlalchemy import Integer, Date, Time, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date, time
from typing import TYPE_CHECKING
from app.models.base import Base 
from app.enums.appointment_status import AppointmentStatus
from app.enums.appointment_duration import AppointmentDuration

if TYPE_CHECKING:
    from app.models.doctor import Doctor
    from app.models.patient import Patient

class Appointment(Base):
    __tablename__ = 'appointments'

    # Columns 
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    appointment_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    appointment_time: Mapped[time | None] = mapped_column(Time, nullable=True)
    status: Mapped[AppointmentStatus] = mapped_column(
        Enum(
            AppointmentStatus,
            name='appointmentstatus',
            native_enum=True,
            values_callable=lambda enum_cls: [e.value for e in enum_cls]
        ),
        default=AppointmentStatus.SCHEDULED,
        nullable=False
    )
    duration: Mapped[AppointmentDuration] = mapped_column(
        Enum(
            AppointmentDuration,
             name='appointmentduration',
            native_enum=True,
            values_callable=lambda enum_cls: [e.value for e in enum_cls]
        ), 
        nullable=False
    )

    # Foreign Keys
    patient_id: Mapped[int] = mapped_column(Integer, ForeignKey('patients.id'), nullable=False)
    doctor_id: Mapped[int] = mapped_column(Integer, ForeignKey('doctors.id'), nullable=False)

    # Relationships
    patient: Mapped['Patient'] = relationship(back_populates='appointments')
    doctor: Mapped['Doctor'] = relationship(back_populates='appointments')


