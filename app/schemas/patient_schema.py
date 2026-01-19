from pydantic import BaseModel, field_validator
from datetime import date
import re


class PatientBase(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    email: str
    phone: str

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
    
    @field_validator('date_of_birth')
    def validate_date_of_birth(cls, value):
        if not value:
            raise ValueError('Value for date of birth is required but is missing')
        return value
    
    @field_validator('email')
    def validate_email(cls, value):
        if not value:
            return value

        email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
        if not re.match(email_pattern, value):
            raise ValueError('email must be a valid email address')
        
        return value
        
    @field_validator('phone')
    def validate_phone(cls, value):
        if not value:
            raise ValueError('Value for phone is required but is missing')

        phone_pattern = r'^\(\d{3}\) \d{3}-\d{4}$'
        if not re.match(phone_pattern, value):
            raise ValueError('phone must be formatted as (XXX) XXX-XXXX, e.g., (501) 374-2303')
        
        return value


class PatientCreate(PatientBase):
    pass


class PatientResponse(PatientBase):
	id: int 

	class Config:
		from_attributes = True