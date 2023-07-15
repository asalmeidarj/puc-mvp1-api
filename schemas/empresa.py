from pydantic import BaseModel
from typing import Optional, List

from share.utils.date import formatDatetime

class EmpresaBodySchema(BaseModel):
    nome: str = "NOME DA EMPRESA"
    cnpj: str = "CNPJ DA EMPRESA"
    descricao: Optional[str] = "DESCRIÇÃO DA EMPRESA"
    logradouro: Optional[str] = "LOGRADOURO DA EMPRESA"
    numero: Optional[str] = "NÚMERO DO ENDEREÇO DA EMPRESA"
    complemento: Optional[str] = "COMPLEMENTO DO ENDEREÇO DA EMPRESA"
    bairro: Optional[str] = "BAIRRO DA EMPRESA"
    cidade: Optional[str] = "CIDADE QUE EMPRESA ESTÁ LOCALIZADA"
    estado: Optional[str] = "ESTADO QUE EMPRESA ESTÁ LOCALIZADA"

class EmpresaBuscaSchema(BaseModel):
    cnpj: Optional[str] = "CNPJ DA EMPRESA"

class EmpresaDeletarSchema(BaseModel):
    id: int = 1

class EmpresaViewSchema(BaseModel):
    id: int = 1
    nome: str = "NOME DA EMPRESA"
    cnpj: str = "CNPJ DA EMPRESA"
    descricao: Optional[str] = "DESCRIÇÃO DA EMPRESA"
    logradouro: Optional[str] = "LOGRADOURO DA EMPRESA"
    numero: Optional[str] = "NÚMERO DO ENDEREÇO DA EMPRESA"
    complemento: Optional[str] = "COMPLEMENTO DO ENDEREÇO DA EMPRESA"
    bairro: Optional[str] = "BAIRRO DA EMPRESA"
    cidade: Optional[str] = "CIDADE QUE EMPRESA ESTÁ LOCALIZADA"
    estado: Optional[str] = "ESTADO QUE EMPRESA ESTÁ LOCALIZADA"
    data_insercao: str = "DESCRIÇÃO DA EMPRESA"


class EmpresaDelSchema(BaseModel):
    message: str
    id: int

def apresenta_empresa(empresa):

    return {
        "id": empresa.id,
        "nome": empresa.nome,
        "cnpj": empresa.cnpj,
        "descricao": empresa.descricao,
        "logradouro": empresa.logradouro,
        "numero": empresa.numero,
        "complemento": empresa.complemento,
        "bairro": empresa.bairro,
        "cidade": empresa.cidade,
        "estado": empresa.estado,
        "data_insercao": formatDatetime(empresa.data_insercao)
    }


class EmpresaListaViewSchema(BaseModel):
    empresas: List[EmpresaViewSchema]


def apresenta_lista_empresa(empresas):
    result = []
    for empresa in empresas:
        result.append(apresenta_empresa(empresa))
    return {"empresas": result}