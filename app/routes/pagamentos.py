from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.pagamento import Pagamento
from app.models.inquilino import Inquilino
from app.models.imovel import Imovel
from app.auth import get_usuario_logado
from typing import Optional
from datetime import date

router = APIRouter(prefix="/pagamentos", tags=["pagamentos"])
templates = Jinja2Templates(directory="app/templates")

def checar_login(request: Request):
    if not get_usuario_logado(request):
        return RedirectResponse(url="/login", status_code=303)
    return None

@router.get("/", response_class=HTMLResponse)
def listar(request: Request, db: Session = Depends(get_db), status: str = ""):
    redirect = checar_login(request)
    if redirect: return redirect
    query = db.query(Pagamento)
    if status:
        query = query.filter(Pagamento.status == status)
    pagamentos = query.all()
    return templates.TemplateResponse(request, "pagamentos/listar.html", {
        "pagamentos": pagamentos,
        "status": status
    })

@router.get("/novo", response_class=HTMLResponse)
def form_novo(request: Request, db: Session = Depends(get_db)):
    redirect = checar_login(request)
    if redirect: return redirect
    inquilinos = db.query(Inquilino).all()
    return templates.TemplateResponse(request, "pagamentos/form.html", {"pagamento": None, "inquilinos": inquilinos})

@router.post("/novo")
def criar(
    request: Request,
    inquilino_id: int = Form(...),
    valor: float = Form(...),
    data_vencimento: date = Form(...),
    db: Session = Depends(get_db)
):
    redirect = checar_login(request)
    if redirect: return redirect
    inquilino = db.query(Inquilino).filter(Inquilino.id == inquilino_id).first()
    pagamento = Pagamento(
        inquilino_id=inquilino_id,
        imovel_id=inquilino.imovel_id,
        valor=valor,
        data_vencimento=data_vencimento,
        status="pendente"
    )
    db.add(pagamento)
    db.commit()
    return RedirectResponse(url="/pagamentos/", status_code=303)

@router.post("/{id}/pagar")
def pagar(id: int, request: Request, db: Session = Depends(get_db)):
    redirect = checar_login(request)
    if redirect: return redirect
    pagamento = db.query(Pagamento).filter(Pagamento.id == id).first()
    pagamento.status = "pago"
    pagamento.data_pagamento = date.today()
    db.commit()
    return RedirectResponse(url="/pagamentos/", status_code=303)

@router.post("/{id}/deletar")
def deletar(id: int, request: Request, db: Session = Depends(get_db)):
    redirect = checar_login(request)
    if redirect: return redirect
    pagamento = db.query(Pagamento).filter(Pagamento.id == id).first()
    db.delete(pagamento)
    db.commit()
    return RedirectResponse(url="/pagamentos/", status_code=303)