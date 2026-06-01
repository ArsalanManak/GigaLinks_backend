from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Optional
from ..db import get_db
from bson import ObjectId
from ..models.project import ProjectIn, ProjectOut
from .deps import get_current_user

router = APIRouter(prefix="/api/v1/projects", tags=["projects"])


def _serialize(doc: dict) -> dict:
    if not doc:
        return doc
    doc["id"] = str(doc.get("_id"))
    doc.pop("_id", None)
    return doc


@router.post("/", response_model=ProjectOut)
async def create_project(payload: ProjectIn, user: dict = Depends(get_current_user)):
    db = get_db()
    doc = payload.dict()
    res = await db.projects.insert_one(doc)
    doc_out = _serialize({**doc, "_id": res.inserted_id})
    return doc_out


@router.get("/", response_model=List[ProjectOut])
async def list_projects(service_type: Optional[str] = None, city: Optional[str] = None, featured: Optional[bool] = None):
    db = get_db()
    q = {}
    if service_type:
        q["service_type"] = service_type
    if city:
        q["city"] = city
    if featured is not None:
        q["featured"] = featured
    cur = db.projects.find(q).sort([("_id", -1)])
    items = []
    async for d in cur:
        items.append(_serialize(d))
    return items


@router.get("/{id}", response_model=ProjectOut)
async def get_project(id: str):
    db = get_db()
    try:
        obj = ObjectId(id)
        doc = await db.projects.find_one({"_id": obj})
    except Exception:
        # fallback to string id
        doc = await db.projects.find_one({"_id": id})
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return _serialize(doc)


@router.put("/{id}", response_model=ProjectOut)
async def update_project(id: str, payload: ProjectIn, user: dict = Depends(get_current_user)):
    db = get_db()
    data = payload.dict()
    try:
        obj = ObjectId(id)
        res = await db.projects.update_one({"_id": obj}, {"$set": data})
    except Exception:
        res = await db.projects.update_one({"_id": id}, {"$set": data})
    if res.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    doc = await db.projects.find_one({"_id": obj if 'obj' in locals() else id})
    return _serialize(doc)


@router.delete("/{id}")
async def delete_project(id: str, user: dict = Depends(get_current_user)):
    db = get_db()
    try:
        obj = ObjectId(id)
        res = await db.projects.delete_one({"_id": obj})
    except Exception:
        res = await db.projects.delete_one({"_id": id})
    if res.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return {"status": "deleted"}
