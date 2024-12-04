from pydantic import BaseModel
from typing import Optional
from models.medical_service import ServiceApprovalStatus


class ServiceModel(BaseModel):
    """Pydantic Service Model"""
    name: str
    description: str
    price: float = 0.0
    medical_practitioner_id: Optional[str] = None
    admin_id: Optional[str] = None
    is_admin_defined: bool = False
    approval_status: ServiceApprovalStatus = ServiceApprovalStatus.pending

    class Config:
        use_enum_values = True


class AddServices(BaseModel):
    """medical practitioner services"""
    services: list[str] = []
