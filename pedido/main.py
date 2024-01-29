from fastapi import FastAPI
from adapter.http_api import PedidoHTTPAPIAdapter
from domain.services import PedidoService
from adapter.mysql_adapter import PedidoMySQLAdapter
from adapter.sqs_adapter import SQSAdapter

DATABASE_URL = "mysql+mysqlconnector://pedido_user:Mudar123!@db-servicos:3306/pedido"
QUEUE_NAME = "pedido-atualizacao"
ENDPOINT_URL='http://localstack:4566'
REGION_NAME='us-east-1'
AWS_ACCESS_KEY_ID='LKIAQAAAAAAAEF5TP5ML'
AWS_SECRET_ACCESS_KEY='D/t43L7EiqM7JnY96oufhfsjL1+SFu8REWtxCi5d'

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    pedido_mysql_adapter = PedidoMySQLAdapter(DATABASE_URL)
    sqs_adapter = SQSAdapter(QUEUE_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, ENDPOINT_URL, REGION_NAME)
    pedido_service = PedidoService(pedido_mysql_adapter, sqs_adapter)
    http_api_adapter = PedidoHTTPAPIAdapter(pedido_service)
    app.include_router(http_api_adapter.router)