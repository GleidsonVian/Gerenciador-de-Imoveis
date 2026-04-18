from fastapi import Request
from fastapi.responses import RedirectResponse
from app.auth import get_usuario_logado

def login_required(request: Request):
    usuario = get_usuario_logado(request)
    if not usuario:
        return RedirectResponse(url="/login", status_code=303)
    return usuario