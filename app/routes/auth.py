from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario
from app.auth import hash_senha, verificar_senha, criar_token

router = APIRouter(tags=["auth"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/login", response_class=HTMLResponse)
def form_login(request: Request):
    return templates.TemplateResponse(request, "auth/login.html", {"erro": None})

@router.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario or not verificar_senha(senha, usuario.senha_hash):
        return templates.TemplateResponse(request, "auth/login.html", {"erro": "Email ou senha inválidos."})

    token = criar_token({"sub": usuario.email, "nome": usuario.nome})
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie("access_token", token, httponly=True, max_age=60*60*8)
    return response

@router.get("/logout")
def logout():
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie("access_token")
    return response

@router.get("/registro", response_class=HTMLResponse)
def form_registro(request: Request):
    return templates.TemplateResponse(request, "auth/registro.html", {"erro": None})

@router.post("/registro")
def registro(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(get_db)
):
    existe = db.query(Usuario).filter(Usuario.email == email).first()
    if existe:
        return templates.TemplateResponse(request, "auth/registro.html", {"erro": "Email já cadastrado."})

    usuario = Usuario(nome=nome, email=email, senha_hash=hash_senha(senha))
    db.add(usuario)
    db.commit()
    return RedirectResponse(url="/login", status_code=303)