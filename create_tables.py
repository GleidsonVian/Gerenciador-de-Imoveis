from dotenv import load_dotenv
load_dotenv()

from app.database import engine, Base
from app.models.imovel import Imovel
from app.models.inquilino import Inquilino
from app.models.pagamento import Pagamento

print("Criando tabelas...")
Base.metadata.create_all(bind=engine)
print("✅ Tabelas criadas com sucesso!")