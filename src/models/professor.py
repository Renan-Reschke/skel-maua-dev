from pydantic import BaseModel, validator
from typing import Optional

from src.enum.codigo_disciplina import CodigoDisciplina
from src.enum.tronco import Tronco
from src.enum.nome_curso import NomeCurso
from src.enum.roles import Roles

from src.models.usuario import Usuario


class Professor(Usuario, BaseModel):
    ID: str
    troncos: list[Tronco]
    cursos: list[NomeCurso]
    disciplinas: Optional[list[CodigoDisciplina]]
    roles: list[Roles] = [Roles.Professor]
    
    @validator('ID')
    def ID_is_not_empty(cls, v):
        if len(v.replace(' ', '')) == 0 or v == None:
            raise ValueError('ID esta vazio')
        return v
    
    @validator('troncos', check_fields=False)
    def troncos_is_not_empty(cls, v):
        if len(v) == 0:
            raise ValueError('troncos is empty')
        return v
    
    @validator('cursos', check_fields=False)
    def cursos_is_not_empty(cls, v):
        if len(v) == 0:
            raise ValueError('cursos is empty')
        return v
    
    @validator('disciplinas', check_fields=False)
    def disciplinas_is_not_empty(cls, v):
        if len(v) == 0:
            raise ValueError('disciplinas is empty')
        return v