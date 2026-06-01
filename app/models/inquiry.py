from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class InquiryIn(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    customer_id: Optional[str] = None
    service_type: str
    city: str
    message: Optional[str] = None


class InquiryOut(InquiryIn):
    id: Optional[str]
    status: Optional[str] = "new"
    created_at: Optional[datetime] = None
