from pydantic import BaseModel, root_validator, validator
from typing import Optional
from datetime import datetime

from src.enum.tipo_atividade import TipoAtividade
from src.enum.status_avaliacao import StatusAvaliacao

from src.models.aluno import Aluno

class Atividade(BaseModel):
    tipo: TipoAtividade
    entregue: bool = False
    prazo: datetime
    alunos: list[Aluno]
    tipoDeArquivo: list[str] = []
    dataEnvio: datetime = None
    numeroDeEnvios: int = 0
    tentativasPermitidas: int
    status: StatusAvaliacao = StatusAvaliacao.NaoEnviado
    nota: Optional[float]
    
    @root_validator
    def entrega_is_valid(cls, v):
        entrega = v.get('dataEnvio')
        prazo = v.get('prazo')
        envios = v.get('numeroDeEnvios')
        tentativasPermitidas = v.get('tentativasPermitidas')
        entregue = v.get('entregue')
        status = v.get('status')
        if (entrega != None) and (entrega > prazo):
            raise ValueError('data de entrega apos o prazo final')
        if envios > tentativasPermitidas:
            raise ValueError('numero de envios excede a quantidade permitida')
        if ((entregue == True) and (status == StatusAvaliacao.NaoEnviado)) or ((entregue == False) and (status != StatusAvaliacao.NaoEnviado)):
            raise ValueError('status de entrega invalido')
        return v
    
    @validator('alunos', check_fields=False)
    def alunos_is_not_empty(cls, v):
        if len(v) == 0:
            raise ValueError('alunos is empty')
        return v
    
    def set_nota(self, nota:float):
        self.nota = nota
        
    def nota_decimal(self):
        return self.nota/10
    
    def _status(self):
        return self.status.value
    
    def _entrega(self):
        self.status = StatusAvaliacao.Enviado
        self.numeroDeEnvios += 1
        self.dataEnvio = datetime.now()