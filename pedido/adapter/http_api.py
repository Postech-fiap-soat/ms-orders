from fastapi import APIRouter, HTTPException
from domain.models import *
from domain.exceptions import *
from domain.services import PedidoService 

class PedidoHTTPAPIAdapter:
    def __init__(self, pedido_service: PedidoService):
        self.__pedido_service = pedido_service
        self.router = APIRouter()
        #pedido
        self.router.add_api_route("/pedido", self.criar_pedido, methods=["POST"])
        self.router.add_api_route("/pedido/{order_id}", self.obter_pedido, methods=["GET"])
        self.router.add_api_route("/pedido/status/{status}", self.obter_pedidos_por_status, methods=["GET"])
        self.router.add_api_route("/pedido_uncompleted", self.obter_pedidos_nao_concluidos, methods=["GET"])
        self.router.add_api_route("/pedido/update_status/{order_id}", self.atualizar_status_pedido, methods=["PUT"])
        self.router.add_api_route("/pedido/checkout/{order_id}", self.checkout_pedido, methods=["PUT"])
        #produto
        self.router.add_api_route("/produto", self.criar_produto, methods=["POST"])
        self.router.add_api_route("/produto/{produto_id}", self.obter_produto, methods=["GET"])
        self.router.add_api_route("/produto/{produto_id}", self.atualizar_produto, methods=["PUT"])
        self.router.add_api_route("/produto/{produto_id}", self.deletar_produto, methods=["DELETE"])



    #PRODUTO
    def criar_produto(self, novo_produto: Produto):
        try:
            self.__pedido_service.criar_produto(novo_produto)
            return {"message": "Produto criado com sucesso"}
        except (DescricaoInvalido,CodigoInvalido,CategoriaInvalido,ValorInvalido, PrecoInvalido, ProdutoJaExiste) as e:
            raise HTTPException(status_code=400, detail=f"Erro ao criar produto: {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao criar produto: {e}")

    def obter_produto(self, produto_id: int):
        try:
            return self.__pedido_service.obter_produto(produto_id)
        except PedidoNaoEncontrado as e:
            raise HTTPException(status_code=404, detail=f"Erro ao obter produto: {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao obter produto: {e}")
    
    def atualizar_produto(self, produto_id: int, produto_atualizado: Produto):
        try:
            self.__pedido_service.atualizar_produto(produto_id, produto_atualizado)
            return {"message": "Produto atualizado com sucesso"}
        except (IdInvalido, ProdutoInvalido, PrecoInvalido) as e:
            raise HTTPException(status_code=400, detail=f"Erro ao atualizar produto: {e}")
        except ProdutoNaoEncontrado as e:
            raise HTTPException(status_code=404, detail=f"Erro ao atualizar produto: {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao atualizar produto: {e}")
    
    def deletar_produto(self, produto_id: int):
        try:
            self.__pedido_service.deletar_produto(produto_id)
            return {"message": "Produto deletado com sucesso"}
        except IdInvalido as e:
            raise HTTPException(status_code=400, detail=f"Erro ao deletar produto: {e}")
        except ProdutoNaoEncontrado as e:
            raise HTTPException(status_code=404, detail=f"Erro ao deletar produto: {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao deletar produto: {e}")
    
    #PEDIDO

    def criar_pedido(self, novo_pedido: Pedido):
        try:
            self.__pedido_service.criar_pedido(novo_pedido)
            return {"message": "Pedido criado com sucesso"}
        except (PedidoInvalido, CarrinhoInvalido, ClienteInvalido, PedidoJaExistente) as e:
            raise HTTPException(status_code=400, detail=f"Erro ao criar pedido: {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao criar pedido: {e}")

    def obter_pedido(self, order_id: int):
        try:
            return self.__pedido_service.obter_pedido(order_id)
        except PedidoNaoEncontrado as e:
            raise HTTPException(status_code=404, detail=f"Erro ao obter pedido: {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao obter pedido: {e}")

    def obter_pedidos_por_status(self, status: int):
        try:
            return self.__pedido_service.obter_pedido_por_status(status)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao obter pedidos: {e}")

    def obter_pedidos_nao_concluidos(self):
        try:
            return self.__pedido_service.obter_pedido_incompleto()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao obter pedidos: {e}")

    def atualizar_status_pedido(self, order_id: int, new_order_status: Optional[int] = None, new_payment_status: Optional[int] = None):
        try:
            self.__pedido_service.atualizar_status_pedido(order_id, new_order_status, new_payment_status)
            return {"message": "Status do pedido atualizado com sucesso"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao atualizar status do pedido: {e}")

    def checkout_pedido(self, order_id: int):
        try:
            self.__pedido_service.checkout_pedido(order_id)
            return {"message": "Checkout do pedido realizado com sucesso"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao realizar checkout do pedido: {e}")