from fastapi import Response
from app.core.config import settings


def set_auth_cookies(
    response: Response,
    access_token: str,
    refresh_token: str,
    access_token_expire_minutes: int = None,
    refresh_token_expire_days: int = None
) -> None:
    """
    Устанавливает access и refresh токены в cookies
    """
    access_token_expire = access_token_expire_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    refresh_token_expire = refresh_token_expire_days or settings.REFRESH_TOKEN_EXPIRE_DAYS
    
    # Access token cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=access_token_expire * 60,  
        httponly=False,
        secure=False, 
        samesite="lax",
        path="/"
    )
    
    # Refresh token cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=refresh_token_expire * 24 * 60 * 60,  
        httponly=True,
        secure=False,
        samesite="lax",
        path="/auth/refresh"  
    )

def clear_auth_cookies(response: Response) -> None:
    """
    Удаляет auth cookies (для logout)
    """
    response.delete_cookie(key="access_token", path="/")
    response.delete_cookie(key="refresh_token", path="/auth/refresh")

def get_token_from_cookie(cookies: dict, token_type: str = "access") -> str:
    """
    Извлекает токен из cookies
    """
    cookie_key = f"{token_type}_token"
    return cookies.get(cookie_key)