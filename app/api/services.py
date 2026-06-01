from fastapi import APIRouter, HTTPException, status
from typing import List
from ..db import get_db
from bson import ObjectId
from ..models.service import ServiceIn, ServiceOut

router = APIRouter(prefix="/api/v1/services", tags=["services"])


def _serialize(doc: dict) -> dict:
    if not doc:
        return doc
    doc["id"] = str(doc.get("_id"))
    doc.pop("_id", None)
    return doc


@router.post("/", response_model=ServiceOut)
async def create_service(payload: ServiceIn):
    db = get_db()
    doc = payload.dict()
    res = await db.services.insert_one(doc)
    return _serialize({**doc, "_id": res.inserted_id})


@router.get("/", response_model=List[ServiceOut])
async def list_services():
    db = get_db()
    cur = db.services.find({}).sort([("title", 1)])
    items = []
    async for d in cur:
        items.append(_serialize(d))
    return items


@router.get("/{id}", response_model=ServiceOut)
async def get_service(id: str):
    db = get_db()
    try:
        obj = ObjectId(id)
        doc = await db.services.find_one({"_id": obj})
    except Exception:
        doc = await db.services.find_one({"_id": id})
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    return _serialize(doc)


@router.put("/{id}", response_model=ServiceOut)
async def update_service(id: str, payload: ServiceIn):
    db = get_db()
    data = payload.dict()
    try:
        obj = ObjectId(id)
        res = await db.services.update_one({"_id": obj}, {"$set": data})
    except Exception:
        res = await db.services.update_one({"_id": id}, {"$set": data})
    if res.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    doc = await db.services.find_one({"_id": obj if 'obj' in locals() else id})
    return _serialize(doc)


@router.delete("/{id}")
async def delete_service(id: str):
    db = get_db()
    try:
        obj = ObjectId(id)
        res = await db.services.delete_one({"_id": obj})
    except Exception:
        res = await db.services.delete_one({"_id": id})
    if res.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    return {"status": "deleted"}
