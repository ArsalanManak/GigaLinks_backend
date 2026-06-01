from fastapi import APIRouter, UploadFile, File, HTTPException
from ..core import config
import cloudinary
import cloudinary.uploader

router = APIRouter(prefix="/api/v1/media", tags=["media"])


def _configure():
    cloudinary.config(
        cloud_name=config.CLOUDINARY_CLOUD,
        api_key=config.CLOUDINARY_API_KEY,
        api_secret=config.CLOUDINARY_API_SECRET,
        secure=True,
    )


@router.post("/upload")
async def upload_media(file: UploadFile = File(...)):
    if not (config.CLOUDINARY_CLOUD and config.CLOUDINARY_API_KEY and config.CLOUDINARY_API_SECRET):
        raise HTTPException(status_code=500, detail="Cloudinary not configured")
    _configure()
    try:
        # cloudinary.uploader.upload can accept file.file (a file-like object)
        result = cloudinary.uploader.upload(file.file, folder="gigalinks")
        return {"url": result.get("secure_url"), "public_id": result.get("public_id"), "raw": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
