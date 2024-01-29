import boto3
from domain.models import Pedido, Produto
from port.event_publishers import PedidoEventPublisher
from adapter.exceptions import SqsException

class SQSAdapter(PedidoEventPublisher): # pragma: no cover
    def __init__(self, queue_name, aws_access_key_id, aws_secret_access_key, endpoint_url, region_name):
        self.__queue_name = queue_name
        self.__sqs = boto3.client('sqs',
                                endpoint_url=endpoint_url,
                                region_name=region_name,
                                aws_access_key_id=aws_access_key_id,
                                aws_secret_access_key=aws_secret_access_key)
    
    def __get_queue_url(self):
        try:
            response = self.__sqs.get_queue_url(QueueName=self.__queue_name)
            return response['QueueUrl']
        except Exception as e:
            raise SqsException({
                "code": "sqs.error.queue.unavailable",
                "message": f"Fila SQS não encontrada {e}",
            })
        
    def publicar(self, pedido: Pedido):
        queue_url = self.__get_queue_url()     
        try:
            self.__sqs.send_message(QueueUrl=queue_url, MessageBody=pedido.json())
        except Exception as e:
            raise SqsException({
                "code": "sqs.error.queue.send_message",
                "message": f"Problema ao enviar mensagem para fila SQS: {e}",
            })
        
    def publicarProduto(self, produto: Produto):
        queue_url = self.__get_queue_url()     
        try:
            self.__sqs.send_message(QueueUrl=queue_url, MessageBody=produto.json())
        except Exception as e:
            raise SqsException({
                "code": "sqs.error.queue.send_message",
                "message": f"Problema ao enviar mensagem para fila SQS: {e}",
            })