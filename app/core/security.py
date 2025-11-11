from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.core.exceptions import InvalidTokenException

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash using Argon2"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password using Argon2"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token(data: dict) -> str:
    """Create JWT refresh token"""
    to_encode = data.copy()
    expire = datetime.now() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def verify_token(token: str) -> Optional[dict]:
    """Verify JWT token and return payload"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        if datetime.fromtimestamp(payload["exp"]) < datetime.now():
            return None
            
        return payload
    except JWTError:
        return None

def get_token_payload(token: str) -> dict:
    """Get token payload or raise custom exception if invalid"""
    payload = verify_token(token)
    if payload is None:
        raise InvalidTokenException()  
    return payload

def generate_tokens(user_id: str, email: str) -> dict:
    """Generate both access and refresh tokens"""
    access_token = create_access_token({"sub": email, "user_id": user_id})
    refresh_token = create_refresh_token({"sub": email, "user_id": user_id})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

def get_user_id_from_token(token: str) -> str:
    """Extract user_id from token payload"""
    payload = get_token_payload(token)
    user_id = payload.get("user_id")
    if not user_id:
        raise InvalidTokenException()
    return user_id

def get_user_email_from_token(token: str) -> str:
    """Extract email from token payload"""
    payload = get_token_payload(token)
    email = payload.get("sub")
    if not email:
        raise InvalidTokenException()
    return email