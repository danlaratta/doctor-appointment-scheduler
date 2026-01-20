from datetime import date, time
from app.crud.doctor_crud import DoctorCrud
from app.crud.patient_crud import PatientCrud
from app.crud.appointment_crud import AppointmentCrud
from app.enums.appointment_duration import AppointmentDuration
from app.enums.appointment_status import AppointmentStatus
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.models.appointment import Appointment


class AppointmentService:
    def __init__(self, doctor_crud: DoctorCrud, patient_crud: PatientCrud, appointment_crud: AppointmentCrud) -> None:
        self.doctor_crud = doctor_crud
        self.patient_crud = patient_crud
        self.appointment_crud = appointment_crud

    # Schedule appointment
    async def schedule_appointment(self, appt_date: date, appt_time: time, duration: AppointmentDuration, doctor_id: int, patient_id: int) -> Appointment:
        # Get and validate doctor and patient exist
        doctor: Doctor = await self.doctor_crud.get_doctor(doctor_id)
        patient: Patient = await self.patient_crud.get_patient(patient_id)

        # Check appointment availability
        is_available: bool = await self.appointment_crud.check_appointment_availability(appt_date, appt_time, doctor_id)

        if not is_available:
            raise ValueError('Doctor is not available at this time for an appointment')
        
        appointment: Appointment = Appointment(
            appointment_date = appt_date,
            appointment_time = appt_time,
            doctor_id=doctor,
            patient_id=patient,
            # appointment_status=AppointmentStatus.SCHEDULED
            duration=duration,
        )

        return await self.appointment_crud.create_appointment(appointment)
    

    # Reschedule appointment
    async def reschedule_appointment(self, appt_id: int, appt_date: date, appt_time: time, duration: AppointmentDuration, doctor_id: int, patient_id: int, status: AppointmentStatus) -> Appointment:
        # Get appointment 
        appointment: Appointment = await self.appointment_crud.get_doctor_appointment(appt_id, appt_date, doctor_id, patient_id)

        # Validate appointment isn't canceled - cannot reschedule canceled appointment
        if appointment.status == AppointmentStatus.CANCELED:
            raise ValueError('Canceled appointments cannot be rescheduled, must create a new appointment')
        
        # Check appointment availability
        is_available: bool = await self.appointment_crud.check_appointment_availability(appt_date, appt_time, doctor_id)

        if not is_available:
            raise ValueError('Doctor is not available at this time for an appointment')
        
        # Reschedule appointment
        appointment.appointment_date = appt_date
        appointment.appointment_time = appt_time
        appointment.duration = duration
        appointment.status = status

        return await self.appointment_crud.update_appointment(appointment)
    

     # Cancel appointment
    async def cancel_appointment(self, appt_id: int, appt_date: date, doctor_id: int, patient_id: int) -> Appointment:
        # Get appointment 
        appointment: Appointment = await self.appointment_crud.get_doctor_appointment(appt_id, appt_date, doctor_id, patient_id)

        # Validate appointment isn't canceled - cannot cancel canceled appointment
        if appointment.status == AppointmentStatus.CANCELED:
            raise ValueError('Appointment is already canceled')
        
        # Cancel appointment
        appointment.appointment_date = None
        appointment.appointment_time = None
        appointment.duration = AppointmentDuration.ZERO_MINUTES
        appointment.status = AppointmentStatus.CANCELED

        return await self.appointment_crud.update_appointment(appointment)
    




