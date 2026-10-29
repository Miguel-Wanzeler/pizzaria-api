from pydantic import BaseModel
from typing import Optional, List # Usuario Schema, Pessoa Schema, Endereço Schema

class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional 
    admin: Optional

    class Config:
        from_attributes = True # Para converter o modelo para um Tabela do banco de dados



class PedidoSchema(BaseModel):
    usuario: int

    class Config:
            from_attributes = True # Para converter o modelo para um Tabela do banco de dados


class LoginSchema(BaseModel):
    email: str
    senha: str

    class Config:
        from_attributes = True # Para converter o modelo para um Tabela do banco de dados

class ItemPedidoSchema(BaseModel):
    quantidade: int
    sabor: str
    tamanho: str
    preco_unitario: float
    id_pedido: int

    class Config:
        from_attributes = True

class ItemPedidoResponseSchema(BaseModel):
    quantidade: int
    sabor: str
    tamanho: str
    preco_unitario: float

    class Config:
        from_attributes = True

class ResponsePedidoSchema(BaseModel):
    id: int
    status: str
    preco: float
    itens: List[ItemPedidoResponseSchema] # Incluindo uma Lista dentro dentro da Obj que saira na resposta, vindo em formato Objetc

    class Config:
        from_attributes = True # Para converter o modelo para um Tabela do banco de dados


class ListaPedidosSchema(BaseModel):
    pedidos: List[ResponsePedidoSchema]

    class Config:
        from_attributes = True