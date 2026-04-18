from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.database import engine, Base, get_db
from app.models.imovel import Imovel
from app.models.inquilino import Inquilino
from app.models.pagamento import Pagamento
from app.models.usuario import Usuario
from app.routes import imoveis, inquilinos, pagamentos
from app.routes import auth
from app.scheduler import iniciar_scheduler, atualizar_pagamentos_atrasados
from app.auth import get_usuario_logado
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    atualizar_pagamentos_atrasados()
    scheduler = iniciar_scheduler()
    yield
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="app/templates")

app.include_router(auth.router)
app.include_router(imoveis.router)
app.include_router(inquilinos.router)
app.include_router(pagamentos.router)

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    usuario = get_usuario_logado(request)
    if not usuario:
        return RedirectResponse(url="/login", status_code=303)

    total_imoveis = db.query(Imovel).count()
    imoveis_alugados = db.query(Imovel).filter(Imovel.status == "alugado").count()
    imoveis_disponiveis = db.query(Imovel).filter(Imovel.status == "disponivel").count()
    total_inquilinos = db.query(Inquilino).count()
    total_pagamentos = db.query(Pagamento).count()
    pagamentos_pendentes = db.query(Pagamento).filter(Pagamento.status == "pendente").count()
    pagamentos_pagos = db.query(Pagamento).filter(Pagamento.status == "pago").count()
    pagamentos_atrasados = db.query(Pagamento).filter(Pagamento.status == "atrasado").count()

    return templates.TemplateResponse(request, "dashboard.html", {
        "total_imoveis": total_imoveis,
        "imoveis_alugados": imoveis_alugados,
        "imoveis_disponiveis": imoveis_disponiveis,
        "total_inquilinos": total_inquilinos,
        "total_pagamentos": total_pagamentos,
        "pagamentos_pendentes": pagamentos_pendentes,
        "pagamentos_pagos": pagamentos_pagos,
        "pagamentos_atrasados": pagamentos_atrasados,
        "usuario": usuario,
    })