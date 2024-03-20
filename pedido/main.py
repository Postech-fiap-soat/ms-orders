from fastapi import FastAPI
from adapter.http_api import PedidoHTTPAPIAdapter
from domain.services import PedidoService
from adapter.mysql_adapter import PedidoMySQLAdapter
from adapter.rabbitmq_adapter import RabbitMQAdapter

DATABASE_URL = "mysql+mysqlconnector://pedido_user:Mudar123!@db-servicos:3306/pedido"

RABBITMQ_HOST = 'rabbitmq'
RABBITMQ_PORT = 5672
RABBITMQ_USERNAME = 'guest'
RABBITMQ_PASSWORD = 'guest'
RABBITMQ_QUEUE_NAME = 'key_pedidos'

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    pedido_mysql_adapter = PedidoMySQLAdapter(DATABASE_URL)
    rabbitmq_adapter = RabbitMQAdapter(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        username=RABBITMQ_USERNAME,
        password=RABBITMQ_PASSWORD,
        queue_name=RABBITMQ_QUEUE_NAME
    )
    pedido_service = PedidoService(pedido_mysql_adapter, rabbitmq_adapter)
    http_api_adapter = PedidoHTTPAPIAdapter(pedido_service)
    app.include_router(http_api_adapter.router)