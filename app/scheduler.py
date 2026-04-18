from apscheduler.schedulers.background import BackgroundScheduler
from app.database import SessionLocal
from app.models.pagamento import Pagamento
from datetime import date

def atualizar_pagamentos_atrasados():
    db = SessionLocal()
    try:
        hoje = date.today()
        pagamentos = db.query(Pagamento).filter(
            Pagamento.status == "pendente",
            Pagamento.data_vencimento < hoje
        ).all()

        total = len(pagamentos)
        for pagamento in pagamentos:
            pagamento.status = "atrasado"

        db.commit()
        if total > 0:
            print(f"[Scheduler] {total} pagamento(s) marcado(s) como atrasado.")
        else:
            print("[Scheduler] Nenhum pagamento atrasado encontrado")
    except Exception as e:
        print(f"[Scheduler] Erro: {e}")
        db.rollback()
    finally:
        db.close()

def iniciar_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        atualizar_pagamentos_atrasados,
        trigger="interval",
        hours=1, #roda a cada 1h
        id="check_atrasados",
        replace_existing=True
    )
    scheduler.start()
    print("[Scheduler] Iniciado - verificando pagamentos a cada 1 hora")
    return scheduler