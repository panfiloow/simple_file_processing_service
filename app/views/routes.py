from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from app.services.auth_service import AuthService
from app.dependencies import get_auth_service

# Настройка Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

view_router = APIRouter()

async def get_current_user_from_token(request: Request, auth_service: AuthService = Depends(get_auth_service)):
    """Получение текущего пользователя для шаблонов"""
    token = request.cookies.get("access_token") or None
    if token:
        user = await auth_service.get_current_user(token)
        return user
    return None

@view_router.get("/")
async def home(request: Request, current_user = Depends(get_current_user_from_token)):
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "current_user": current_user}
    )

@view_router.get("/login")
async def login_page(request: Request, current_user = Depends(get_current_user_from_token)):
    if current_user:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/dashboard")
    
    return templates.TemplateResponse(
        "login.html", 
        {"request": request, "current_user": current_user}
    )

@view_router.get("/register")
async def register_page(request: Request, current_user = Depends(get_current_user_from_token)):
    if current_user:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/dashboard")
    
    return templates.TemplateResponse(
        "register.html", 
        {"request": request, "current_user": current_user}
    )

@view_router.get("/dashboard")
async def dashboard_page(request: Request, current_user = Depends(get_current_user_from_token)):
    if not current_user:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/login")
    
    return templates.TemplateResponse(
        "dashboard.html", 
        {"request": request, "current_user": current_user}
    )

@view_router.get("/upload")
async def upload_page(request: Request, current_user = Depends(get_current_user_from_token)):
    if not current_user:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/login")
    
    return templates.TemplateResponse(
        "upload.html", 
        {"request": request, "current_user": current_user}
    )