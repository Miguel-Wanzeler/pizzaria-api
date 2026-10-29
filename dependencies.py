from sqlalchemy.orm import session, sessionmaker
from models import Usuario, db
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from main import ALGORITM, SECRET_KEY, OAuth2_schema
from jose import jwt, JWTError

def pegar_sessao():
    try: # Para tentar caso funcione tudo bem, se não 
        Session = sessionmaker(bind=db)
        session = Session()
        yield session # Ele coleta como o return mas, não encerra minha sessão como um return, mas pode gerar erro caso trave no meio do código 
    finally: # ir para o finally para encerrar e mesmo que de certo ele vai fazer a mesma coisa
        session.close()

def verificar_token(token: str =  Depends(OAuth2_schema), session: Session = Depends(pegar_sessao)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITM) # Verificar se o token é valido e extrair o ID do usuario
        id_usuario = dic_info.get("sub") # Pegar informação do usuario, dic_info
    except JWTError:
        raise HTTPException(status_code=401, detail="Acesso Negado")
    
    usuario = session.query(Usuario).filter(Usuario.id == id_usuario).first() # Verificando se o token é valido
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso Inválido")
    return usuario