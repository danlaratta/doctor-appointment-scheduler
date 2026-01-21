from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.doctor_crud import DoctorCrud
from app.database.database import get_db
from app.exceptions.database_exception import DatabaseException
from app.models.doctor import Doctor
from app.schemas.doctor_schema import DoctorCreate, DoctorResponse
from app.services.doctor_service import DoctorService


# Create doctor router
router = APIRouter(prefix='/doctor', tags=['Doctors'])

# Dependency builder that wires Route → Service → Crud → DB Session
def get_doctor_service(db: AsyncSession = Depends(get_db)) -> DoctorService:
    doctor_crud: DoctorCrud = DoctorCrud(db)
    return DoctorService(doctor_crud)


# Create Route
@router.post('/', response_model=DoctorResponse, status_code=status.HTTP_201_CREATED)
async def create_doctor(doctor_create: DoctorCreate, service: DoctorService = Depends(get_doctor_service)) -> DoctorResponse:
    try:
        doctor: Doctor = await service.register_new_doctor(
            fname = doctor_create.first_name,
            lname = doctor_create.last_name,
            email = doctor_create.first_name,
        )
        return DoctorResponse.model_validate(doctor)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# Get Route
@router.get('/{doctor_id}', response_model=DoctorResponse, status_code=status.HTTP_200_OK)
async def get_doctor(doctor_id: int, service: DoctorService = Depends(get_doctor_service)) -> DoctorResponse:
    try:
        doctor: Doctor = await service.doctor_crud.get_doctor(doctor_id)
        return DoctorResponse.model_validate(doctor)
    except DatabaseException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    

# Delete Route
@router.delete('/{doctor_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_doctor(doctor_id: int, service: DoctorService = Depends(get_doctor_service)) -> None:
    try:
        await service.doctor_crud.delete_doctor(doctor_id)
    except DatabaseException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

