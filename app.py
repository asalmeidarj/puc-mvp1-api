from sqlalchemy.exc import IntegrityError
from flask_openapi3 import Info, Tag
from flask_openapi3 import OpenAPI
from flask_cors import CORS
from flask import redirect
from model import Session, Empresa
from logger import logger
from schemas import *


info = Info(title="API de controle de contratos terceirizados", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
empresa_tag = Tag(name="Empresa", description="Adição, visualização e remoção de empresas à base")


@app.get('/')
def home():
    return redirect('/openapi')


@app.post('/empresa', tags=[empresa_tag],
          responses={"200": EmpresaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_empresa(body: EmpresaBodySchema):
    """Adiciona um novo Empresa à base de dados

    Retorna uma representação da empresa.
    """
    session = Session()
    empresa = Empresa(
        nome=body.nome.upper(),
        cnpj=body.cnpj,
        cidade=body.cidade.upper(),
        bairro=body.bairro.upper(),
        complemento=body.complemento.upper(),
        estado=body.estado.upper(),
        logradouro=body.logradouro.upper(),
        numero=body.numero,    
        descricao=body.descricao
    )
     
    logger.debug(f"Adicionando empresa de nome: '{empresa.nome}'")
    try:
        # adicionando empresa
        session.add(empresa)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado empresa de nome: '{empresa.nome}'")
        return apresenta_empresa(empresa), 200
    except IntegrityError as e:
        error_msg = "Empresa de mesmo cnpj já salvo na base :/"
        logger.warning(f"Erro ao adicionar empresa '{empresa.nome}', {error_msg}")
        return {"mesage": error_msg}, 409
    except Exception as e:
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar empresa '{empresa.nome}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/empresa', tags=[empresa_tag],
         responses={"200": EmpresaViewSchema, "404": ErrorSchema})
def get_empresa(query: EmpresaBuscaSchema):
    """Faz a busca por um Empresa a partir do cnpj da empresa

    Retorna uma representação dos empresas.
    """
    empresa_cnpj = query.cnpj
    logger.debug(f"Coletando dados sobre empresa #{empresa_cnpj}")
    session = Session()
    empresa = session.query(Empresa).filter(Empresa.cnpj == empresa_cnpj).first()

    if not empresa:
        error_msg = "Empresa não encontrada na base :/"
        logger.warning(f"Erro ao buscar empresa '{empresa_cnpj}', {error_msg}")
        return {"mesage": error_msg}, 400
    else:
        logger.debug(f"Empresa econtrado: '{empresa.nome}'")
        return apresenta_empresa(empresa), 200


@app.get('/empresas', tags=[empresa_tag],
         responses={"200": EmpresaListaViewSchema, "404": ErrorSchema})
def get_empresas():
    """Lista todos os empresas cadastrados na base

    Retorna uma lista de representações de empresas.
    """
    logger.debug(f"Coletando lista de empresas")
    session = Session()
    empresas = session.query(Empresa).all()
    print(empresas)
    if not empresas:
        error_msg = "Empresa não encontrada na base :/"
        logger.warning(f"Erro ao buscar por lista de empresas. {error_msg}")
        return {"mesage": error_msg}, 400
    else:
        logger.debug(f"Retornando lista de empresas")
        return apresenta_lista_empresa(empresas), 200


@app.delete('/empresa', tags=[empresa_tag],
            responses={"200": EmpresaDelSchema, "404": ErrorSchema})
def del_empresa(query: EmpresaDeletarSchema):
    """Deleta um Empresa a partir do id informado

    Retorna uma mensagem de confirmação da remoção.
    """
    empresa_id = query.id

    logger.debug(f"Deletando dados sobre empresa #{empresa_id}")
    session = Session()

    if empresa_id:
        count = session.query(Empresa).filter(Empresa.id == empresa_id).delete()

    session.commit()
    if count:
        logger.debug(f"Deletado empresa #{empresa_id}")
        return {"mesage": "Empresa removida", "id": empresa_id}
    else: 
        error_msg = "Empresa não encontrado na base :/"
        logger.warning(f"Erro ao deletar empresa #'{empresa_id}', {error_msg}")
        return {"mesage": error_msg}, 400
