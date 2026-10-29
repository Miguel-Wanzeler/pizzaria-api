from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from schemas import PedidoSchema, ItemPedidoSchema, ListaPedidosSchema
from models import ItemPedido, Pedido, Usuario


order_router = APIRouter(
    prefix="/pedidos",
    tags=["pedidos"],
    dependencies=[Depends(verificar_token)],
)


@order_router.get("/")
async def pedidos():
    return {"mensagem": "Você acessou a rota de pedidos"}


@order_router.post("/pedido")
async def criar_pedido(
    pedido_schema: PedidoSchema,  # mantido por compatibilidade; o usuário agora vem do token
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token),
):
    novo_pedido = Pedido(usuario=usuario.id)
    session.add(novo_pedido)
    session.commit()
    session.refresh(novo_pedido)
    return {
        "mensagem": f"Pedido criado com sucesso! ID do pedido: {novo_pedido.id}",
        "id_pedido": novo_pedido.id,
    }


@order_router.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(
    id_pedido: int,
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token),
):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    elif not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa ação")

    pedido.status = "CANCELADO"
    session.commit()
    return {
        "mensagem": f"Pedido número {pedido.id} cancelado com sucesso",
        "id_pedido": pedido.id,
        "status": "CANCELADO",
    }


@order_router.get("/listar")
async def listar_pedidos(
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token),
):
    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Você não tem autorização para essa ação")
    pedidos = session.query(Pedido).all()
    return {"pedidos": pedidos}


@order_router.post("/pedido/adicionar-item/{id_pedido}")
async def adicionar_item_pedido(
    id_pedido: int,
    item_pedido_schema: ItemPedidoSchema,
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token),
):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não existe")
    elif not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa ação")

    item_pedido = ItemPedido(
        item_pedido_schema.quantidade,
        item_pedido_schema.sabor,
        item_pedido_schema.tamanho,
        item_pedido_schema.preco_unitario,
        id_pedido,
    )
    session.add(item_pedido)
    session.flush()  # gera o id do item e inclui ele em pedido.itens
    pedido.calcular_preco()
    session.commit()
    return {
        "mensagem": "Item criado com sucesso",
        "item_id": item_pedido.id,
        "preco_pedido": pedido.preco,
    }


@order_router.post("/pedido/remover-item/{id_item_pedido}")
async def remover_item_pedido(
    id_item_pedido: int,
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token),
):
    item_pedido = session.query(ItemPedido).filter(ItemPedido.id == id_item_pedido).first()
    if not item_pedido:
        raise HTTPException(status_code=400, detail="Item no pedido não existe")

    pedido = session.query(Pedido).filter(Pedido.id == item_pedido.pedido).first()
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa ação")

    session.delete(item_pedido)
    session.flush()
    session.refresh(pedido)  # recarrega pedido.itens sem o item removido
    pedido.calcular_preco()
    session.commit()
    return {
        "mensagem": "Item retirado com sucesso",
        "quantidade_itens_pedido": len(pedido.itens),
        "preco_pedido": pedido.preco,
    }


@order_router.post("/pedido/finalizar/{id_pedido}")
async def finalizar_pedido(
    id_pedido: int,
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token),
):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    elif not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa ação")

    pedido.status = "FINALIZADO"
    session.commit()
    return {
        "mensagem": f"Pedido número {pedido.id} finalizado com sucesso",
        "id_pedido": pedido.id,
        "status": "FINALIZADO",
    }


@order_router.get("/pedido/{id_pedido}")
async def visualizar_pedido(
    id_pedido: int,
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token),
):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    elif not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa ação")
    return {
        "quantidade_itens": len(pedido.itens),
        "pedido": pedido,
    }


@order_router.get("/listar/pedidos-usuario", response_model=ListaPedidosSchema)
async def listar_pedidos_usuario(
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token),
):
    pedidos = session.query(Pedido).filter(Pedido.usuario == usuario.id).all()
    return {"pedidos": pedidos}