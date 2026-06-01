from fastapi import APIRouter, HTTPException, status, Request
from typing import List, Optional
from ..db import get_db
from bson import ObjectId
from ..models.inquiry import InquiryIn, InquiryOut
from datetime import datetime

router = APIRouter(prefix="/api/v1/inquiries", tags=["inquiries"])


def _serialize(doc: dict) -> dict:
    if not doc:
        return doc
    doc["id"] = str(doc.get("_id"))
    doc.pop("_id", None)
    return doc


from fastapi import Depends
from ..main import limiter


@router.post("/submit", response_model=InquiryOut)
@limiter.limit("5/minute")
async def submit_inquiry(request: Request, payload: InquiryIn):
    db = get_db()
    doc = payload.dict()
    doc["status"] = "new"
    doc["created_at"] = datetime.utcnow()
    res = await db.inquiries.insert_one(doc)
    out = _serialize({**doc, "_id": res.inserted_id})
    return out


@router.get("/", response_model=List[InquiryOut])
async def list_inquiries(status: Optional[str] = None):
    db = get_db()
    q = {}
    if status:
        q["status"] = status
    cur = db.inquiries.find(q).sort([("created_at", -1)])
    items = []
    async for d in cur:
        items.append(_serialize(d))
    return items


@router.patch("/{id}")
async def update_inquiry(id: str, status: Optional[str] = None, note: Optional[str] = None):
    db = get_db()
    update = {}
    if status:
        update["status"] = status
    if note:
        update.setdefault("notes", []).append({"text": note, "at": datetime.utcnow()})
    if not update:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nothing to update")
    try:
        obj = ObjectId(id)
        res = await db.inquiries.update_one({"_id": obj}, {"$set": update, "$push": {"notes": {"$each": []}}})
    except Exception:
        res = await db.inquiries.update_one({"_id": id}, {"$set": update})
    if res.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inquiry not found")
    return {"status": "ok"}
