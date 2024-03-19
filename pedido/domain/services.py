from typing import List, Optional
from domain.models import Produto,Pedido
from domain.exceptions import *
from port.repositories import PedidoRepository
from adapter.rabbitmq_adapter import RabbitMQAdapter
import pika.exceptions
from fastapi.encoders import jsonable_encoder
import json

class PedidoService:
    def __init__(self, pedido_repository: PedidoRepository, pedido_rabbitmq_adapter: RabbitMQAdapter):
        self.__pedido_repository = pedido_repository
        self.__pedido_rabbitmq_adapter = pedido_rabbitmq_adapter

        
    def validar_id(self, id: int):
        if id is None or id == "":
            raise IdInvalido("Campo ID é obrigatório")
        
    def validar_status_order(self, id: int):
        if id is None or id == "":
            raise IdInvalido("Campo status é obrigatório")
        
    def validar_produto(self, produto: Produto):
        if produto.description is None or produto.description == "":
            raise DescricaoInvalido("Campo Descrição é obrigatório")
        if produto.code is None or produto.code == "":
            raise CodigoInvalido("Campo Código é obrigatório")
        if produto.category is None or produto.category == "":
            raise CategoriaInvalido("Campo Categoria é obrigatório")
        if produto.price is None or produto.price <=0:
            raise ValorInvalido("Campo Valor é obrigatório")
        
    #PRODUTO

    def criar_produto(self, novo_produto: Produto):
        try:
            self.__pedido_repository.inserirProduto(novo_produto, on_duplicate_sku=ProdutoJaExiste("Produto já existente"))
        except Exception as e:
            raise ErroAoCriarProduto(f"Erro ao criar produto: {e}")

    def obter_produto(self, id: int) -> Produto:
        try:
            produto = self.__pedido_repository.buscarProdutoPorID(id, on_not_found=ProdutoNaoEncontrado("Produto não encontrado"))
            return produto
        except Exception as e:
            raise ErroAoObterProduto(f"Erro ao obter produto: {e}")
        
    def obter_produtos(self) -> List[Produto]:
        try:
            produtos = self.__pedido_repository.buscarProdutos(on_not_found=ProdutoNaoEncontrado("Produtos não encontrados"))
            return produtos
        except Exception as e:
            raise ErroAoObterProduto(f"Erro ao obter produtos: {e}")
    
    def atualizar_produto(self, id: int, produto: Produto):
        try:
            produto.id = id
            self.__pedido_repository.atualizarProduto(produto, on_not_found=ProdutoNaoEncontrado("Produto não encontrado"))
        except Exception as e:
            raise ErroAoAtualizarProduto(f"Erro ao atualizar produto: {e}")
    
    def deletar_produto(self, id: int):
        try:
            self.__pedido_repository.excluirProduto(id, on_not_found=ProdutoNaoEncontrado("Produto não encontrado"))
            return {"message": "Produto deletado com sucesso"}
        except Exception as e:
            raise ErroAoDeletarProduto(f"Erro ao deletar produto: {e}")
    
    #PEDIDO
    
    def criar_pedido(self, novo_pedido: Pedido):
        try:
            self.__pedido_repository.inserirPedido(novo_pedido, on_duplicate_sku=PedidoJaExistente("Pedido já existente"))
        except Exception as e:
            raise ErroAoCriarPedido(f"Erro ao criar pedido: {e}")
        
        # Tente conectar ao RabbitMQ e publicar a mensagem
        try:
            novo_pedido_dict = jsonable_encoder(novo_pedido)
            pedido_json = json.dumps(novo_pedido_dict)
            self.__pedido_rabbitmq_adapter.connect()
            self.__pedido_rabbitmq_adapter.publish_message(pedido_json)
            self.__pedido_rabbitmq_adapter.close_connection()
        except pika.exceptions.AMQPConnectionError as e:
            print(str(e)+str(Exception))
            raise ErroAoCriarPedido(f"Erro ao conectar ao Rabbit: {e}")
        except pika.exceptions.AMQPError as e:
            print(str(e))
            raise ErroAoCriarPedido(f"Erro ao publicar mensagem no RabbitMQ: {e}")

        
            
            
        
    def obter_pedido(self, order_id: int) -> Pedido:
        try:
            pedido = self.__pedido_repository.buscarPedidoPorID(order_id, on_not_found=PedidoNaoEncontrado("Pedido não encontrado"))
            return pedido
        except Exception as e:
            raise ErroAoObterPedido(f"Erro ao obter pedido: {e}")
        
    def obter_pedido_por_status(self, status: int) -> List[Pedido]:
        try:
            pedido = self.__pedido_repository.buscarPedidoPorStatus(status, on_not_found=PedidoNaoEncontrado("Não existem pedidos com esse status"))
            return pedido
        except (PedidoIDInvalido, PedidoNaoEncontrado):
            raise
        except Exception as e:
            raise ErroAoObterPedido(f"Erro ao obter pedido: {e}")
        
    def obter_pedido_incompleto(self) -> List[Pedido]:
        try:
            pedido = self.__pedido_repository.buscarPedidoIncompleto(on_not_found=PedidoNaoEncontrado("Não existem pedidos com esse status"))
            return pedido
        except Exception as e:
            raise ErroAoObterPedido(f"Erro ao obter pedido: {e}")
        
    def atualizar_status_pedido(self, order_id: int, new_order_status: Optional[int] = None, new_payment_status: Optional[int] = None) -> None:
        try:
            pedido = self.__pedido_repository.buscarPedidoPorID(order_id, on_not_found=PedidoNaoEncontrado("Pedido não encontrado"))

            if new_order_status is not None:
                pedido.order_status = new_order_status
            
            if new_payment_status is not None:
                pedido.payment_status = new_payment_status
            
            self.__pedido_repository.atualizarStatusPedido(order_id, new_order_status,new_payment_status, on_not_found=PedidoNaoEncontrado("Pedido não encontrado"))
        except Exception as e:
            raise ErroAoAtualizarPedido(f"Erro ao atualizar pedido: {e}")
        
    def checkout_pedido(self, order_id: int) -> Pedido:
        try:

            pedido = self.__pedido_repository.buscarPedidoPorID(order_id, on_not_found=PedidoNaoEncontrado("Pedido não encontrado"))
            if pedido is None:
                raise PedidoNaoEncontrado(f"Pedido não encontrado")

            self.__pedido_repository.efetuarCheckoutPedido(order_id, on_not_found=PedidoNaoEncontrado("Pedido não encontrado"))
            
            return {"message": "Pedido deletado com sucesso"}
        except Exception as e:
            raise ErroAoDeletarPedido(f"Erro ao deletar pedido: {e}")
        
    
    
        
    