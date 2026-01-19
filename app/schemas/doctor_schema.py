from pydantic import BaseModel, field_validator
import re


class DoctorBase(BaseModel):
    first_name: str
    last_name: str
    email: str

    @field_validator('first_name')
    def validate_first_name(cls, value):
        if not value:
            raise ValueError('Value for first name is required but is missing')
        return value
        
    @field_validator('last_name')
    def validate_last_name(cls, value):
        if not value:
            raise ValueError('Value for last name is required but is missing')
        return value
        
    @field_validator('email')
    def validate_email(cls, value):
        if not value:
            return value

        email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
        if not re.match(email_pattern, value):
            raise ValueError('email must be a valid email address')
        
        return value
		

class DoctorCreate(DoctorBase):
    pass


class DoctorResponse(DoctorBase):
	id: int 

	class Config:
		from_attributes = True