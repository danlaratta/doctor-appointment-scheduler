from pydantic import BaseModel, field_validator
from datetime import time


class DoctorScheduleBase(BaseModel):
    weekday_start_time: time 
    weekday_end_time: time 
    weekend_start_time: time | None 
    weekend_start_time: time | None 

    @field_validator('weekday_start_time')
    def validate_weekday_start_time(cls, value):
        if not value:
            raise ValueError('Value for weekday start time is required but is missing')
        return value
    
    @field_validator('weekday_end_time')
    def validate_weekday_end_time(cls, value):
        if not value:
            raise ValueError('Value for weekday end time is required but is missing')
        return value
    

class DoctorScheduleCreate(DoctorScheduleBase):
    pass


class DoctorScheduleUpdate(DoctorScheduleBase):
    pass


class DoctorScheduleResponse(DoctorScheduleBase):
	id: int 

	class Config:
		from_attributes = True