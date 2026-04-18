from pydantic import BaseModel
from typing import Optional

class ImovelCreate(BaseModel):
    endereco : str
    tipo : str
    valor_aluguel : float
    status : str = "disponivel"
    descricao : Optional[str] = None