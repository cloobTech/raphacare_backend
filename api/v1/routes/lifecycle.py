from fastapi import APIRouter, Depends, status
from api.v1.utils.get_db_session import get_db_session
from schemas.default_response import DefaultResponse
from models.admin import Admin
from models.patient import Patient
from models.medical_practitioner import MedicalPractitioner


router = APIRouter(tags=['Lifecycle'], prefix='/api/v1/lifecycle')


@router.get('/', status_code=status.HTTP_200_OK, response_model=DefaultResponse)
async def lifecycle(storage=Depends(get_db_session)):
    """Get medical practitioner by id"""
    p = await storage.get(Patient, "ace42ace-5ca1-445d-8431-1b67031920e7")
    print(p)
    x = await storage.get(Admin, "e3ca984e-9c82-40ae-8159-925e0f5b4393")
    m = await storage.get(MedicalPractitioner, "ff67ff99-6788-4091-9650-def1c4c3c110")

    # print(x, m, p)
    # print("Print I git printed")
    # print(m)
    # print(x)
    # print(p.user)

    return DefaultResponse(
        message="success",
        status="s",
        data={

        }

    )
