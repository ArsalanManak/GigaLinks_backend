from fastapi import APIRouter, HTTPException, status, Depends, Response, Cookie
import bcrypt
from ..models.user import UserIn, LoginIn, UserOut, Token
from ..db import get_db
from ..auth.jwt import create_access_token
from bson import ObjectId
from .deps import get_current_user

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False


@router.post("/register", response_model=UserOut)
async def register(user_in: UserIn):
    db = get_db()
    existing = await db.users.find_one({"email": user_in.email})
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    doc = user_in.dict()
    doc["password_hash"] = hash_password(doc.pop("password"))
    res = await db.users.insert_one(doc)
    return UserOut(id=str(res.inserted_id), name=doc["name"], email=doc["email"])


@router.post("/login", response_model=Token)
async def login(user_in: LoginIn, response: Response):
    db = get_db()
    user = await db.users.find_one({"email": user_in.email})
    if not user or not verify_password(user_in.password, user.get("password_hash", "")):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(str(user["_id"]))
    # Set as httpOnly cookie
    response.set_cookie(key="access_token", value=token, httponly=True, secure=False, samesite="lax")
    return Token(access_token=token)



@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "ok"}


@router.get("/me")
async def me(current_user: dict = Depends(get_current_user)):
    return {"id": str(current_user.get("_id")), "name": current_user.get("name"), "email": current_user.get("email")}


@router.post("/refresh", response_model=Token)
async def refresh(current_user: dict = Depends(get_current_user), response: Response = None):
    # issue a fresh access token
    token = create_access_token(str(current_user.get("_id")))
    if response is not None:
        response.set_cookie(key="access_token", value=token, httponly=True, secure=False, samesite="lax")
    return Token(access_token=token)
