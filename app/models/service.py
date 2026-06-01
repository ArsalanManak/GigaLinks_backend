from pydantic import BaseModel
from typing import List, Optional


class ServiceIn(BaseModel):
    slug: str
    title: str
    description: str
    icon: Optional[str] = None
    hero_image: Optional[str] = None
    image_url: Optional[str] = None
    youtube_url: Optional[str] = None
    sub_services: List[str] = []


class ServiceOut(ServiceIn):
    id: Optional[str]
