from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.database.session import AsyncSessionLocal
from app.repositories.user_repository import UserRepository
from app.repositories.token_repository import TokenRepository
from app.services.auth_service import AuthService
from app.schemas.user import UserResponse


security = HTTPBearer()

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
    

async def get_user_repository(db = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

async def get_token_repository(db = Depends(get_db)) -> TokenRepository:
    return TokenRepository(db)

async def get_auth_service(
    user_repo: UserRepository = Depends(get_user_repository),
    token_repo: TokenRepository = Depends(get_token_repository)
) -> AuthService:
    return AuthService(user_repo, token_repo)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service)
) -> UserResponse:
    token = credentials.credentials
    user = await auth_service.get_current_user(token)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


###################TODO: Другие зависимости
async def get_current_active_user(
    current_user: UserResponse = Depends(get_current_user)
) -> UserResponse:
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user