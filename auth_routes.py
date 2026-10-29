from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import  pegar_sessao, verificar_token
from main import bcrypt_context
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session, session
from jose import jwt, JWTError
from main import SECRET_KEY, ALGORITM, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone

auth_router = APIRouter(prefix='/auth', tags=["auth"])

def criar_token(id_usuario, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)): # Criando o Token de acesso, duracao_token é o tempo de expiração do token
    # JWT TOKEN
    data_expiracao = datetime.now(timezone.utc) + duracao_token # Data de expiração do token
    dic_info = {"sub": str(id_usuario), "exp": data_expiracao} # Dicionário com as informações do token
    encoded_jwt = jwt.encode(dic_info, SECRET_KEY, algorithm=ALGORITM)
    return encoded_jwt

def autenticar_usuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email==email).first() # Verificando se o usuario existe

    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False
    else:
        return usuario


@auth_router.get("/")
async def autenticar():
    return {"mensagem":"Você acesso a rota padrão de autenticação", "autenticação": False}


@auth_router.post("/criar_conta")
async def criar_conta(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)): # Criar padronização na entrada de dados para quando o site estiver em produção ir rápido
    # validar o tamanho da senha
    if len(usuario_schema.senha) < 6:
        raise HTTPException(status_code=400, detail="A senha deve ter pelo menos 6 caracteres") # Retornando um erro caso a senha tenha menos de 6 caracteres
    if len(usuario_schema.senha.encode('utf-8')) > 72:
        raise HTTPException(status_code=400, detail="A senha deve ter no máximo 72 caracteres") # Retornando um erro caso a senha tenha mais de 72 caracteres          
    usuario = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first()# Realizando uma query no banco de dados
    if usuario:
        raise HTTPException(status_code=400, detail="Já existe um usuario com esse email")
        # ja existe usuario
    else:
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha) # criptografando a senha
        novo_usuario = Usuario(nome=usuario_schema.nome, email=usuario_schema.email, senha=senha_criptografada, ativo=usuario_schema.ativo, admin=usuario_schema.admin) # adicionando um novo usuario caso ele não exista
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": "Usuario cadastrado com sucesso!"}


@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session) # Buscando na tabela se tem um usuario com o email informado
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou a senha está incorreta!")
    else:# JWT TOKEN Bearer é o tipo de token que é usado para autenticação
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7)) # Criando o token de refresh, 7 dias
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer" # Token tipo Bearer não pode ser enviado como parametro, tem qu ser enviado como header, como parametro Access Token - OAuth2
         }

@auth_router.post("/login-form")
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session) # Buscando na tabela se tem um usuario com o email informado
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou a senha está incorreta!")
    else:# JWT TOKEN Bearer é o tipo de token que é usado para autenticação
        access_token = criar_token(usuario.id)
        return {
            "access_token": access_token,
            "token_type": "Bearer" # Token tipo Bearer não pode ser enviado como parametro, tem qu ser enviado como header, como parametro Access Token - OAuth2
         }

@auth_router.get("/refresh")
async def use_refresh_token(usuario: Usuario = Depends(verificar_token)): # Token é o token de refresh
    # Verificar o Token
    access_token = criar_token(usuario.id)
    return {"access_token": access_token, "token_type": "Bearer"}