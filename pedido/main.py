from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import create_engine, Table, MetaData, select, update, insert, Column, String, Float, Integer
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker, Session
from requests import post
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
    Column('total_price', Float)
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
            total_price=order.totalPrice
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