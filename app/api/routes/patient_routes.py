from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import patient_crud
from app.crud.patient_crud import PatientCrud
from app.database.database import get_db
from app.exceptions.database_exception import DatabaseException
from app.models.patient import Patient
from app.schemas.patient_schema import PatientCreate, PatientResponse
from app.services.patient_service import PatientService

# Create patient router
router = APIRouter(prefix='/patient', tags=['Patients'])


# Dependency builder
def get_patient_service(db: AsyncSession = Depends(get_db)) -> PatientService:
    patient_crud: PatientCrud = PatientCrud(db)
    return PatientService(patient_crud)


# Create Route
@router.post('/', response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
async def create_patient_route(patient_create: PatientCreate, service: PatientService = Depends(get_patient_service)) -> PatientResponse:
    try:
        patient: Patient = Patient(
            fname = patient_create.first_name,
            lname = patient_create.last_name,
            dob = patient_create.date_of_birth,
            email = patient_create.email,
            phone = patient_create.phone,
       )
        return PatientResponse.model_validate(patient)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# Get Route
@router.get('/{patient_id}', status_code=status.HTTP_200_OK)
async def cget_patient_route(patient_id: int, service: PatientService = Depends(get_patient_service)) -> PatientResponse:
    try:
        patient: Patient = await service.patient_crud.get_patient(patient_id)
        return PatientResponse.model_validate(patient)
    except DatabaseException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# Delete Route
@router.delete('/{patient_id}')
async def delete_patient_route(patient_id: int, service: PatientService = Depends(get_patient_service)) -> None:
    try:
        await service.patient_crud.delete_patient(patient_id)
    except DatabaseException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

