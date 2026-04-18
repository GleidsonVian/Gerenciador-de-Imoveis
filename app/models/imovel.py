from sqlalchemy import Column, Integer, String, Float, Enum
from sqlalchemy.orm import relationship
from app.database import Base

class Imovel(Base):
    __tablename__ = "imoveis"

    id = Column(Integer, primary_key=True, index=True)
    endereco = Column(String(255), nullable=False)
    tipo = Column(Enum("casa", "apartamento", "comercial"), nullable=False)
    valor_aluguel = Column(Float, nullable=False)
    status = Column(Enum("disponivel", "alugado"), default="disponivel")
    descricao = Column(String(500), nullable=True)

    inquilinos = relationship("Inquilino", back_populates="imovel")
    pagamentos = relationship("Pagamento", back_populates="imovel")