from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Inquilino(Base):
    __tablename__ = "inquilinos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False)
    cpf = Column(String(14), unique=True, nullable=False)
    email = Column(String(150), nullable=True)
    telefone = Column(String(20), nullable=True)
    imovel_id = Column(Integer, ForeignKey("imoveis.id"), nullable=True)

    imovel = relationship("Imovel", back_populates="inquilinos")
    pagamentos = relationship("Pagamento", back_populates="inquilino")