from abc import ABC, abstractmethod
from typing import Optional,List
from domain.models import *

class PedidoRepository(ABC): # pragma: no cover
    #PEDIDO
    @abstractmethod
    def inserirPedido(self, pedido: Pedido, on_duplicate_sku: Exception):
        pass

    @abstractmethod
    def buscarPedidoPorID(self, id: int, on_not_found: Exception) -> Pedido:
        pass

    @abstractmethod
    def buscarPedidoPorStatus(self, status: int, on_not_found: Exception) -> Optional[List[Pedido]]:
        pass

    @abstractmethod
    def buscarPedidoIncompleto(self, on_not_found: Exception) -> Optional[List[Pedido]]:
        pass

    @abstractmethod
    def atualizarStatusPedido(self, id: int, new_order_status: Optional[int] = None, new_payment_status: Optional[int] = None, on_not_found: Exception = None):
        pass

    @abstractmethod
    def efetuarCheckoutPedido(self, id: int, on_not_found: Exception) -> Pedido:
        pass


    #PRODUTO

    @abstractmethod
    def inserirProduto(self, produto: Produto, on_duplicate_sku: Exception):
        pass

    @abstractmethod
    def buscarProdutoPorID(self, id: int, on_not_found: Exception) -> Produto:
        pass
    
    @abstractmethod
    def atualizarProduto(self, produto: Produto, on_not_found: Exception):
        pass

    @abstractmethod
    def excluirProduto(self, id: int, on_not_found: Exception):
        pass