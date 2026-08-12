from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.user import UserRegister, UserLogin
from app.auth.auth_service import (
    register_user,
    login_user
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(user: UserRegister):

    user_id, error = register_user(user)

    if error:
        raise HTTPException(
            status_code=400,
            detail=error
        )

    return {
        "message": "User registered successfully",
        "user_id": user_id
    }


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):

    user = UserLogin(
        username=form_data.username,
        password=form_data.password
    )

    result, error = login_user(user)

    if error:
        raise HTTPException(
            status_code=401,
            detail=error
        )

    return result