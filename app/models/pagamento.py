from sqlalchemy import Column, Integer, Float, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Pagamento(Base):
    __tablename__ = "pagamentos"

    id = Column(Integer, primary_key=True, index=True)
    inquilino_id = Column(Integer, ForeignKey("inquilinos.id"), nullable=False)
    imovel_id = Column(Integer, ForeignKey("imoveis.id"), nullable=False)
    valor = Column(Float, nullable=False)
    data_vencimento = Column(Date, nullable=False)
    data_pagamento = Column(Date, nullable=True)
    status = Column(Enum("pendente", "pago", "atrasado"), default="pendente")

    inquilino = relationship("Inquilino", back_populates="pagamentos")
    imovel = relationship("Imovel", back_populates="pagamentos")