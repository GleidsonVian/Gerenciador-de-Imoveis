from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.inquilino import Inquilino
from app.models.imovel import Imovel
from typing import Optional

router = APIRouter(prefix="/inquilinos", tags=["inquilinos"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
def listar(request: Request, db: Session = Depends(get_db)):
    inquilinos = db.query(Inquilino).all()
    return templates.TemplateResponse(request, "inquilinos/listar.html", {"inquilinos": inquilinos})

@router.get("/novo", response_class=HTMLResponse)
def form_novo(request: Request, db: Session = Depends(get_db)):
    imoveis = db.query(Imovel).filter(Imovel.status == "disponivel").all()
    return templates.TemplateResponse(request, "inquilinos/form.html", {"inquilino": None, "imoveis": imoveis})

@router.post("/novo")
def criar(
    nome: str = Form(...),
    cpf: str = Form(...),
    email: Optional[str] = Form(None),
    telefone: Optional[str] = Form(None),
    imovel_id: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    inquilino = Inquilino(nome=nome, cpf=cpf, email=email, telefone=telefone, imovel_id=imovel_id)
    db.add(inquilino)
    if imovel_id:
        imovel = db.query(Imovel).filter(Imovel.id == imovel_id).first()
        if imovel:
            imovel.status = "alugado"
    db.commit()
    return RedirectResponse(url="/inquilinos/", status_code=303)

@router.get("/{id}/editar", response_class=HTMLResponse)
def form_editar(id:int, request: Request, db: Session = Depends(get_db)):
    inquilino = db.query(Inquilino).filter(Inquilino.id == id).first()
    imoveis = db.query(Imovel).all()
    return templates.TemplateResponse(request, "inquilinos/form.html", {"inquilino": inquilino, "imoveis": imoveis})

@router.post("/{id}/editar")
def editar(
    id: int,
    nome: str = Form(...),
    cpf: str = Form(...),
    email: Optional[str] = Form(None),
    telefone: Optional[str] = Form(None),
    imovel_id: Optional[int] = Form(None),
    db: Session = Depends(get_db)
):
    inquilino = db.query(Inquilino).filter(Inquilino.id == id).first()
    inquilino.nome = nome
    inquilino.cpf = cpf
    inquilino.email = email
    inquilino.telefone = telefone
    inquilino.imovel_id = imovel_id
    db.commit()
    return RedirectResponse(url="/inquilinos/", status_code=303)

@router.post("/{id}/deletar")
def deletar(id: int, db: Session = Depends(get_db)):
    inquilino = db.query(Inquilino).filter(Inquilino.id == id).first()
    if inquilino.imovel_id:
        imovel = db.query(Imovel).filter(Imovel.id == inquilino.imovel_id).first()
        if imovel:
            imovel.status = "disponivel"
    db.delete(inquilino)
    db.commit()
    return RedirectResponse(url="/inquilinos/", status_code=303)