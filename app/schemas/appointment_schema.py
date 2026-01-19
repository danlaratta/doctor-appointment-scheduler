from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from app.enums.appointment_status import AppointmentStatus
from app.enums.appointment_duration import AppointmentDuration


class AppointmentBase(BaseModel):
    appointment_date_time: datetime
    status: AppointmentStatus = Field(default=AppointmentStatus.SCHEDULED)
    duration: AppointmentDuration 

    @field_validator('appointment_date_time')
    def validate_appointment_date_time(cls, value):
        if not value:
            raise ValueError('Value for appointment date time is required but is missing')
        return value
    
    @field_validator('status')
    def validate_status(cls, value):
        if not value:
            raise ValueError('Value for appointment status is required but is missing')
        return value
    
    @field_validator('duration')
    def validate_appointment_duration(cls, value):
        if not value:
            raise ValueError('Value for appointment duration is required but is missing')
        return value
        

class AppointmentCreate(AppointmentBase):
    patient_id: int
    doctor_id: int


class AppointmentUpdate(AppointmentBase):
    pass


class AppointmentResponse(AppointmentBase):
	id: int 

	class Config:
		from_attributes = True