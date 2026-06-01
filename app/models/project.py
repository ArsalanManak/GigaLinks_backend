from pydantic import BaseModel
from typing import List, Optional


class ProjectIn(BaseModel):
    title: str
    service_type: str
    city: str
    cloudinary_urls: List[str] = []
    youtube_url: Optional[str] = None
    description: Optional[str] = None
    featured: Optional[bool] = False


class ProjectOut(ProjectIn):
    id: Optional[str]
