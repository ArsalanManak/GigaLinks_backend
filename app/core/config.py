import os
from typing import Any
from dotenv import load_dotenv

load_dotenv(override=True)

def get_env(key: str, default: Any = None) -> Any:
    return os.environ.get(key, default)


MONGO_URI = get_env("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME = get_env("DATABASE_NAME", "gigalinks")

SECRET_KEY = get_env("SECRET_KEY", "changeme")
ALGORITHM = get_env("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(get_env("ACCESS_TOKEN_EXPIRE_MINUTES", 60 * 24))

# Cloudinary
CLOUDINARY_CLOUD = get_env("CLOUDINARY_CLOUD", None)
CLOUDINARY_API_KEY = get_env("CLOUDINARY_API_KEY", None)
CLOUDINARY_API_SECRET = get_env("CLOUDINARY_API_SECRET", None)
CLOUDINARY_UPLOAD_PRESET = get_env("CLOUDINARY_UPLOAD_PRESET", None)
ALLOWED_ORIGINS = get_env("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
RATE_LIMIT = get_env("RATE_LIMIT", "10/minute")
