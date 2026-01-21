from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.doctor_crud import DoctorCrud
from app.crud.doctor_schedule_crud import DoctorScheduleCrud
from app.database.database import get_db
from app.exceptions.database_exception import DatabaseException
from app.models.doctor_schedule import DoctorSchedule
from app.schemas.doctor_schedule_schema import DoctorScheduleCreate, DoctorScheduleUpdate, DoctorScheduleResponse
from app.services.doctor_schedule_service import DoctorScheduleService


# Create doctor schedule router
router = APIRouter(prefix='/doctor-schedule', tags=[''])


# Dependency builder that wires Route → Service → Crud → DB Session
def get_doctor_schedule_service(db: AsyncSession = Depends(get_db)) -> DoctorScheduleService:
    doctor_schedule_crud: DoctorScheduleCrud = DoctorScheduleCrud(db)
    doctor_crud: DoctorCrud = DoctorCrud(db)
    return DoctorScheduleService(doctor_schedule_crud, doctor_crud)


# Create Route
@router.post('/', response_model=DoctorScheduleResponse, status_code=status.HTTP_201_CREATED)
async def create_doctor_schedule_route(schedule_create: DoctorScheduleCreate, service: DoctorScheduleService = Depends(get_doctor_schedule_service)) -> DoctorScheduleResponse:
    try:
        schedule: DoctorSchedule = await service.create_doctor_schedule(
            doctor_id = schedule_create.doctor_id,
            weekday_start_time = schedule_create.weekday_start_time,
            weekday_end_time = schedule_create.weekday_end_time,
            weekend_start_time = schedule_create.weekend_start_time, 
            weekend_end_time = schedule_create.weekend_end_time,
        )
        return DoctorScheduleResponse.model_validate(schedule)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# Get Route
@router.get('/get/{schedule_id}', response_model=DoctorScheduleResponse, status_code=status.HTTP_200_OK)
async def get_doctor_schedule_route(schedule_id: int, doctor_id: int, service: DoctorScheduleService = Depends(get_doctor_schedule_service)) -> DoctorScheduleResponse:
    try:
        schedule: DoctorSchedule = await service.schedule_crud.get_schedule(schedule_id, doctor_id)
        return DoctorScheduleResponse.model_validate(schedule) 
    except DatabaseException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# Update Route
@router.put('/update', response_model=DoctorScheduleResponse, status_code=status.HTTP_200_OK)
async def update_doctor_schedule_route(schedule_id: int, doctor_id: int, schedule_update: DoctorScheduleUpdate, service: DoctorScheduleService = Depends(get_doctor_schedule_service)) -> DoctorScheduleResponse:
        try:
            schedule: DoctorSchedule = await service.update_doctor_schedule(
                schedule_id = schedule_id,
                doctor_id = doctor_id,
                weekday_start_time = schedule_update.weekday_start_time,
                weekday_end_time = schedule_update.weekday_end_time,
                weekend_start_time = schedule_update.weekend_start_time, 
                weekend_end_time = schedule_update.weekend_end_time,
            )
            return DoctorScheduleResponse.model_validate(schedule)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# Delete Route
@router.delete('/delete/{schedule_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_doctor_schedule_route(schedule_id: int, doctor_id: int, service: DoctorScheduleService = Depends(get_doctor_schedule_service)) -> None:
    try:
        await service.schedule_crud.delete_schedule(schedule_id, doctor_id)
    except DatabaseException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

