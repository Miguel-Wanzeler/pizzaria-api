# uvicorn main:app --reload - Parte que inicia o servidor e executa o arquivo main
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext # Para Criptografar a senha do usuario
from dotenv import load_dotenv # Para carregar as variáveis de ambiente
import os # Para acessar as variáveis de ambiente

load_dotenv() # Carregando as variáveis de ambiente

SECRET_KEY = os.getenv("SECRET_KEY") # Acessando a variável de ambiente SECRET_KEY
ALGORITM = os.getenv("ALGORITM") # Acessando a variável de ambiente ALGORITM
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")) # Acessando a variável de ambiente ACCESS_TOKEN_EXPIRE_MINUTES e convertendo para inteiro

app =  FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # Criando o contexto de senha, acessar a senha e conseguir verificar se a senha é válida

OAuth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form") 

from auth_routes import auth_router # Importando as rotas de autenticação
from order_routes import order_router # Importando as rotas de pedidos

app.include_router(auth_router) # Incluindo as rotas de autenticação no app
app.include_router(order_router) # Incluindo as rotas de pedidos no app

