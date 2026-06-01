from fastapi import Request, HTTPException, status
from typing import Optional
from ..auth import jwt as jwt_utils
from ..db import get_db


async def get_current_user(request: Request) -> dict:
    token: Optional[str] = None
    # First check cookies
    if "access_token" in request.cookies:
        token = request.cookies.get("access_token")
    else:
        # Fallback to Authorization header
        auth: Optional[str] = request.headers.get("Authorization")
        if auth and auth.startswith("Bearer "):
            token = auth.split(" ", 1)[1]

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        payload = jwt_utils.decode_token(token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    db = get_db()
    user = await db.users.find_one({"_id": user_id})
    if not user:
        # try ObjectId string match
        user = await db.users.find_one({"_id": {"$toString": user_id}})
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    user["id"] = str(user.get("_id"))
    return user
