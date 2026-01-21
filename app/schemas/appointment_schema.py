from pydantic import BaseModel, Field, field_validator
from datetime import date, time
from app.enums.appointment_status import AppointmentStatus
from app.enums.appointment_duration import AppointmentDuration


class AppointmentBase(BaseModel):
    appointment_date: date
    appointment_time: time
    status: AppointmentStatus = Field(default=AppointmentStatus.SCHEDULED)
    duration: AppointmentDuration 

    @field_validator('duration')
    def validate_appointment_duration(cls, value):
        if not value:
            raise ValueError('Value for appointment duration is required but is missing')
        return value
        

class AppointmentCreate(AppointmentBase):
    patient_id: int
    doctor_id: int


class AppointmentReschedule(AppointmentBase):
    pass


class AppointmentCancel(BaseModel):
    status: AppointmentStatus


class AppointmentResponse(AppointmentBase):
    id: int 
    patient_id: int
    doctor_id: int

    class Config:
        from_attributes = True