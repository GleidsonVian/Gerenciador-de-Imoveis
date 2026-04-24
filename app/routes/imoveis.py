from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.imovel import Imovel
from app.auth import get_usuario_logado
from typing import Optional

router = APIRouter(prefix="/imoveis", tags=["imoveis"])
templates = Jinja2Templates(directory="app/templates")

def checar_login(request: Request):
    if not get_usuario_logado(request):
        return RedirectResponse(url="/login", status_code=303)
    return None

@router.get("/", response_class=HTMLResponse)
@router.get("/", response_class=HTMLResponse)
def listar(request: Request, db: Session = Depends(get_db), busca: str = "", status: str = ""):
    redirect = checar_login(request)
    if redirect: return redirect
    query = db.query(Imovel)
    if busca:
        query = query.filter(Imovel.endereco.ilike(f"%{busca}%"))
    if status:
        query = query.filter(Imovel.status == status)
    imoveis = query.all()
    return templates.TemplateResponse(request, "imoveis/listar.html", {
        "imoveis": imoveis,
        "busca": busca,
        "status": status
    })

@router.get("/novo", response_class=HTMLResponse)
def form_novo(request: Request):
    redirect = checar_login(request)
    if redirect: return redirect
    return templates.TemplateResponse(request, "imoveis/form.html", {"imovel": None})

@router.post("/novo")
def criar(
    request: Request,
    endereco: str = Form(...),
    tipo: str = Form(...),
    valor_aluguel: float = Form(...),
    status: str = Form("disponivel"),
    descricao: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    redirect = checar_login(request)
    if redirect: return redirect
    imovel = Imovel(endereco=endereco, tipo=tipo, valor_aluguel=valor_aluguel, status=status, descricao=descricao)
    db.add(imovel)
    db.commit()
    return RedirectResponse(url="/imoveis/", status_code=303)

@router.get("/{id}/editar", response_class=HTMLResponse)
def form_editar(id: int, request: Request, db: Session = Depends(get_db)):
    redirect = checar_login(request)
    if redirect: return redirect
    imovel = db.query(Imovel).filter(Imovel.id == id).first()
    return templates.TemplateResponse(request, "imoveis/form.html", {"imovel": imovel})

@router.post("/{id}/editar")
def editar(
    id: int,
    request: Request,
    endereco: str = Form(...),
    tipo: str = Form(...),
    valor_aluguel: float = Form(...),
    status: str = Form(...),
    descricao: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    redirect = checar_login(request)
    if redirect: return redirect
    imovel = db.query(Imovel).filter(Imovel.id == id).first()
    imovel.endereco = endereco
    imovel.tipo = tipo
    imovel.valor_aluguel = valor_aluguel
    imovel.status = status
    imovel.descricao = descricao
    db.commit()
    return RedirectResponse(url="/imoveis/", status_code=303)

@router.post("/{id}/deletar")
def deletar(id: int, request: Request, db: Session = Depends(get_db)):
    redirect = checar_login(request)
    if redirect: return redirect
    imovel = db.query(Imovel).filter(Imovel.id == id).first()
    db.delete(imovel)
    db.commit()
    return RedirectResponse(url="/imoveis/", status_code=303)