from fastapi import FastAPI,HTTPException,Depends,Path
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import create_engine, Table, MetaData, select, update, insert, Column, String, Float, Integer,DateTime
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
import os

# Configuração do SQLAlchemy
DATABASE_URL = "mysql+mysqlconnector://user:password@db:3306/pedido"
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Criar tabela de pedido se não existir
pedido = Table(
    'pedido', metadata,
    Column('id', Integer, primary_key=True),
    Column('cart_id', Integer),  # Referência ao carrinho
    Column('client_id', Integer),  # Referência ao cliente
    Column('observation', String(255)),
    Column('total_price', Float),
    Column('creation_datetime', DateTime, default=datetime.utcnow),
    Column('payment_status', Integer, default=1),
    Column('order_status', Integer, default=1)
)
metadata.create_all(engine)

# Gerenciamento de sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

'''
def self_register():    
    url = "http://kong:8001/upstreams/pedido/targets"
    payload = {
        "target": os.environ['HOSTNAME'] + ":8080",
        "weight": 10,
        "tags": [ "pedido" ]
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    response = post(url, json=payload, headers=headers )
    return response

status_register = self_register()
print(status_register)
'''
class Product(BaseModel):
    id: int
    code: str
    description: str
    price: float
    category: str

class CartItem(BaseModel):
    id: int
    product: Product
    count: int
    observation: Optional[str]

class Cart(BaseModel):
    id: int
    items: List[CartItem]

class Client(BaseModel):
    id: int
    name: str
    cpf: str
    email: str

class Order(BaseModel):
    cart: Cart
    client: Client
    observation: Optional[str]
    totalPrice: float

#Criar pedido
@app.post("/create_order")
async def create_order(order: Order):
    # Criar uma nova sessão
    session = SessionLocal()
    try:

        # Inserir o pedido na tabela 'pedido'
        insert_query = insert(pedido).values(
            cart_id=order.cart.id,
            client_id=order.client.id,
            observation=order.observation,
            total_price=order.totalPrice,
            creation_datetime=datetime.utcnow(),
            payment_status=1,  # Valor padrão
            order_status=1  # Valor padrão
        )
        result = session.execute(insert_query)

        # Confirmar as mudanças
        session.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=400, detail="Erro ao criar pedido")
        return {"message": "Pedido criado com sucesso"}
    except Exception as e:
        # Reverter as mudanças em caso de erro
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar pedido: {e}")
    finally:
        # Fechar a sessão
        session.close()

#Obter pedido pelo ID  
@app.get("/order/{order_id}")
async def obter_pedido(order_id: int):
    query = select(pedido).where(pedido.columns.id == order_id)
    with engine.connect() as connection:
        try:
            result = connection.execute(query).fetchone()
            if result is None:
                raise HTTPException(status_code=404, detail="Pedido não encontrado")
            
            # Mapear valores para nomes de colunas e retornar como JSON
            column_names = [column.name for column in pedido.c]
            result_dict = dict(zip(column_names, result))
            return result_dict
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")
        
#Obter todos os pedidos
@app.get("/orders", response_model=List[dict])
async def get_all_orders(skip: int = 0, limit: int = 10):
    query = select(pedido).offset(skip).limit(limit)
    with engine.connect() as connection:
        try:
            result = connection.execute(query).fetchall()
            orders = []
            column_names = [column.name for column in pedido.c]
            for row in result:
                order_dict = dict(zip(column_names, row))
                orders.append(order_dict)
            return orders       
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")
        
#Obter pedido pelo status
@app.get("/orders/status/{status}", response_model=List[dict])
async def get_orders_by_status(status: int = Path(..., title="Status do Pedido", description="Status do pedido a ser filtrado")):
    valid_statuses = {1, 2, 3, 4}
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Status de pedido inválido")

    query = select(pedido).where(pedido.columns.order_status == status)
    with engine.connect() as connection:
        try:
            result = connection.execute(query).fetchall()
            orders = []
            column_names = [column.name for column in pedido.c]
            for row in result:
                order_dict = dict(zip(column_names, row))
                orders.append(order_dict)
            return orders
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Nenhum pedido com status informado")
        
#Obter pedidos nao concluidos
@app.get("/orders/uncompleted", response_model=List[dict])
async def get_uncompleted_orders():
    uncompleted_status = {1, 2, 3}  # Status que são considerados não concluídos
    query = select(pedido).where(pedido.columns.order_status.in_(uncompleted_status))
    with engine.connect() as connection:
        try:
            result = connection.execute(query).fetchall()
            orders = []
            column_names = [column.name for column in pedido.c]
            for row in result:
                order_dict = dict(zip(column_names, row))
                orders.append(order_dict)
            return orders
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Nenhum pedido pendente")
        
#Atualizar pedido
@app.put("/order/update_status/{order_id}")
async def update_order_status(order_id: int, new_status: int):
    # Criar uma nova sessão
    session = SessionLocal()

    valid_statuses = {1, 2, 3, 4}  # Status válidos
    if new_status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Status de pedido inválido")
    
    try:

        # Verificar se o pedido existe
        existing_order = session.execute(select(pedido).where(pedido.columns.id == order_id)).fetchone()
        if existing_order is None:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")

        # Atualizar o status do pedido
        update_query = update(pedido).where(pedido.columns.id == order_id).values(order_status=new_status)
        session.execute(update_query)
        session.commit()

        return {"message": "Status do pedido atualizado com sucesso"}
    except Exception as e:
        # Reverter as mudanças em caso de erro
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar status do pedido: {e}")
    finally:
        # Fechar a sessão
        session.close()

#Checkout do pedido
@app.put("/order/checkout/{order_id}")
async def checkout_order(order_id: int):
    # Criar uma nova sessão
    session = SessionLocal()

    # Verificar se o pedido existe
    existing_order = session.execute(select(pedido).where(pedido.columns.id == order_id)).fetchone()
    if existing_order is None:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    # Verificar se o status de pagamento permite checkout
    if existing_order and existing_order[1] != 1:  # Verifique se o status de pagamento é NAO_REALIZADO (1)
        raise HTTPException(status_code=400, detail="Não é possível realizar o checkout, status de pagamento inválido")

    
    try:

        # Atualizar o status de pagamento para APROVADO (2) e o status de pedido para EM_PREPARACAO (2)
        update_query = update(pedido).where(pedido.columns.id == order_id).values(payment_status=2, order_status=2)
        session.execute(update_query)
        session.commit()

        return {"message": "Checkout do pedido realizado com sucesso"}

    except Exception as e:
        # Reverter as mudanças em caso de erro
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao realizar checkout do pedido: {e}")
    finally:
        # Fechar a sessão
        session.close()
        