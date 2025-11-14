from fastapi import APIRouter, Depends, Response, status
from app.core.cookie import set_auth_cookies
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.dependencies import get_auth_service
from app.services.interfaces.auth_service import IAuthService

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate, auth_service: IAuthService = Depends(get_auth_service)):
    return await auth_service.register_user(user_data)

@auth_router.post("/login", response_model=UserResponse)
async def login_user(
    response: Response,
    login_data: UserLogin,
    auth_service: IAuthService = Depends(get_auth_service)
):
    """
    Аутентификация пользователя и установка токенов в cookies
    """
    tokens = await auth_service.authenticate_user(login_data)
    
    set_auth_cookies(
        response=response,
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token
    )
    
    user = await auth_service.get_current_user(tokens.access_token)
    return user