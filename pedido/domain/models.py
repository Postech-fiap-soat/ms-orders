from pydantic import BaseModel
from typing import Optional, List

class Produto(BaseModel):
    id: int
    code: str
    description: str
    price: float
    category: str

class ItemCarrinho(BaseModel):
    id: int
    count: int
    product:Produto
    observation: Optional[str]


class Carrinho(BaseModel):
    id: int
    items: Optional[List[ItemCarrinho]] = [] 

class Cliente(BaseModel):
    id: int
    name: str
    cpf: str
    email: str

class Pedido(BaseModel):
    cart: Carrinho
    client: Cliente
    observation: Optional[str]
    totalPrice: float
    payment_status: int=1
    order_status: int=1