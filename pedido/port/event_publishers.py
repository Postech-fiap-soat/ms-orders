from abc import ABC, abstractmethod
from domain.models import *

class PedidoEventPublisher(ABC): # pragma: no cover
    @abstractmethod
    def publicar(self, pedido: Pedido):
        pass

    @abstractmethod
    def publicarProduto(self, produto: Produto):
        pass