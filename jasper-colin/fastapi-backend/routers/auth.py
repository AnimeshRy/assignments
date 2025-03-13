from fastapi import APIRouter, HTTPException, Depends, status, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from models import UserCreate, UserInDB
from auth_utils import get_password_hash, verify_password, create_access_token
from datetime import timedelta
from config import settings

router = APIRouter()

@router.post("/register")
async def register(user: UserCreate):
    # Check if user exists
    if await router.app.mongodb["users"].find_one({"email": user.email}):
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Create new user
    user_dict = user.dict()
    user_dict["password"] = get_password_hash(user_dict["password"])
    result = await router.app.mongodb["users"].insert_one(user_dict)

    return {"message": "User created successfully"}

@router.post("/login")
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await router.app.mongodb["users"].find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user["_id"])},
        expires_delta=access_token_expires
    )

    # Set cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,  # True in production
        samesite=settings.COOKIE_SAMESITE,  # 'lax' in production
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/"
    )

    return {"message": "Successfully logged in"}

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        path="/",
        secure=settings.COOKIE_SECURE,
        httponly=True,
        samesite=settings.COOKIE_SAMESITE
    )
    return {"message": "Successfully logged out"}
