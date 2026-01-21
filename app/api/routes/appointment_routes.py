from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from app.crud.doctor_crud import DoctorCrud
from app.crud.patient_crud import PatientCrud
from app.crud.appointment_crud import AppointmentCrud
from app.database.database import get_db
from app.exceptions.database_exception import DatabaseException
from app.models.appointment import Appointment
from app.schemas.appointment_schema import AppointmentCreate, AppointmentReschedule, AppointmentCancel, AppointmentResponse
from app.services.appointment_service import AppointmentService


# Create appointment router
router = APIRouter(prefix='/appointment', tags=['Appointments'])


# Dependency builder that wires Route → Service → Crud → DB Session
def get_appointment_service(db: AsyncSession = Depends(get_db)) -> AppointmentService:
    doctor_crud: DoctorCrud = DoctorCrud(db)
    patient_crud: PatientCrud = PatientCrud(db)
    appointment_crud: AppointmentCrud = AppointmentCrud(db)
    return AppointmentService(doctor_crud, patient_crud, appointment_crud)


# Create Route
@router.post('/', response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
async def create_apppointment_route(appt_create: AppointmentCreate, service: AppointmentService = Depends(get_appointment_service)) -> AppointmentResponse:
    try:
        appointment: Appointment = await service.schedule_appointment(
            appt_date = appt_create.appointment_date,
            appt_time = appt_create.appointment_time,
            duration =  appt_create.duration,
            doctor_id = appt_create.doctor_id, 
            patient_id = appt_create.patient_id,
        )
        return AppointmentResponse.model_validate(appointment)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# Get Route
@router.get('get/{appt_id}', response_model=AppointmentResponse, status_code=status.HTTP_200_OK)
async def get_apppointment_route(appt_id: int, appt_date: date, doctor_id: int, patient_id: int, service: AppointmentService = Depends(get_appointment_service)) -> AppointmentResponse:
    try:
        appointment: Appointment = await service.appointment_crud.get_doctor_appointment(appt_id, appt_date, doctor_id, patient_id)
        return AppointmentResponse.model_validate(appointment) 
    except DatabaseException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# Get All Route
@router.get('/get-all-on-{appt_date}', response_model=AppointmentResponse, status_code=status.HTTP_200_OK)
async def get_all_apppointments_route(appt_date: date, doctor_id: int, service: AppointmentService = Depends(get_appointment_service)) -> list[AppointmentResponse]:
    try:
        appointments: list[Appointment] = await service.appointment_crud.get_all_doctor_appointments_for_day(appt_date, doctor_id)
        responses = [AppointmentResponse.model_validate(appt) for appt in appointments]  
        return responses
    except DatabaseException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# Reschedule Route
@router.put('/reschedule/{appt_id}', response_model=AppointmentResponse, status_code=status.HTTP_200_OK)
async def reschedule_apppointment_route(appt_id: int, doctor_id: int, patient_id: int, appt_reschedule: AppointmentReschedule, service: AppointmentService = Depends(get_appointment_service)) -> AppointmentResponse:
    try:
        appointment: Appointment = await service.reschedule_appointment(
            appt_id = appt_id,
            appt_date = appt_reschedule.appointment_date,
            appt_time = appt_reschedule.appointment_time,
            duration = appt_reschedule.duration,
            doctor_id = doctor_id,
            patient_id = patient_id,
            status = appt_reschedule.status,

        )
        return AppointmentResponse.model_validate(appointment)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# Cancel Route
@router.put('/cancel/{appt_id}', response_model=AppointmentResponse, status_code=status.HTTP_200_OK)
async def cancel_apppointment_route(appt_id: int, appt_date: date, doctor_id: int, patient_id: int, appt_cancel: AppointmentCancel, service: AppointmentService = Depends(get_appointment_service)) -> AppointmentResponse:
    try:
        appointment: Appointment = await service.cancel_appointment(
            appt_id = appt_id,
            appt_date = appt_date,
            doctor_id = doctor_id,
            patient_id = patient_id,
        )
        return AppointmentResponse.model_validate(appointment)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))



