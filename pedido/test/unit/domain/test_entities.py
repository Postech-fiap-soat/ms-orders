from unittest import TestCase
import unittest
from unittest.mock import patch, Mock
from domain.services import PedidoService
from domain.models import Produto
from domain.exceptions import *
from adapter.exceptions import *
from port.repositories import *
from port.event_publishers import *

class TestPedidoService(unittest.TestCase):

    def setUp(self):
        self.pedido_repository = Mock()
        self.pedido_event_publisher = Mock()
        self.pedido_service = PedidoService(self.pedido_repository, self.pedido_event_publisher)

    @patch('domain.services.Pedido')
    def testCriarPedidoComSucesso(self, MockPedidoRequest):
        mockPedidoRequest = Mock()
        
        mockPedidoRequest.id = 1
        mockPedidoRequest.cart = 1
        mockPedidoRequest.client = 1
        mockPedidoRequest.observation = "teste"
        mockPedidoRequest.totalPrice = 5.99
        mockPedidoRequest.payment_status = 1
        mockPedidoRequest.order_status = 1

        MockPedidoRequest.return_value = mockPedidoRequest
        
        self.pedido_service.criar_pedido(mockPedidoRequest)
    
    @patch('domain.services.Pedido')
    def testObterPedidoComSucesso(self, MockPedidoRequest):
        mockPedidoRequest = Mock()
        
        mockPedidoRequest.id = 1

        MockPedidoRequest.return_value = mockPedidoRequest
        
        self.pedido_service.obter_pedido(mockPedidoRequest)

    @patch('domain.services.Pedido')
    def testAtualizarStatusPedidoComSucesso(self, MockPedidoRequest):
        mockPedidoRequest = Mock()
        
        mockPedidoRequest.id = 1
        mockPedidoRequest.order_status = 2

        MockPedidoRequest.return_value = mockPedidoRequest
        
        self.pedido_service.atualizar_status_pedido(mockPedidoRequest)

    @patch('domain.services.Pedido')
    def testObterPedidoPorStatusComSucesso(self, MockPedidoRequest):
        mockPedidoRequest = Mock()
        
        mockPedidoRequest.order_status = 2

        MockPedidoRequest.return_value = mockPedidoRequest
        
        self.pedido_service.obter_pedido_por_status(mockPedidoRequest)

    @patch('domain.services.Pedido')
    def testObterPedidoIncompletoComSucesso(self, MockPedidoRequest):
        mockPedidoRequest = Mock()
        
        MockPedidoRequest.return_value = mockPedidoRequest
        
        self.pedido_service.obter_pedido_incompleto()

    @patch('domain.services.Pedido')
    def testCheckoutPedidoComSucesso(self, MockPedidoRequest):
        mockPedidoRequest = Mock()
        
        mockPedidoRequest.id = 1

        MockPedidoRequest.return_value = mockPedidoRequest
        
        self.pedido_service.checkout_pedido(mockPedidoRequest)

    def testValidarStatusInvalido(self):
        with self.assertRaises(IdInvalido):
            self.pedido_service.validar_status_order("")
    
    #PRODUTO

    @patch('domain.services.Produto')
    def testCriarProdutoComSucesso(self, MockProdutoRequest):
        mockProdutoRequest = Mock()
        
        mockProdutoRequest.id = 1
        mockProdutoRequest.code = "123"
        mockProdutoRequest.description = "Descrição Teste"
        mockProdutoRequest.price = 5.99
        mockProdutoRequest.category = "Lanche"

        MockProdutoRequest.return_value = mockProdutoRequest
        
        self.pedido_service.criar_produto(mockProdutoRequest)

    @patch('domain.services.Produto')
    def testObterProdutoComSucesso(self, MockProdutoRequest):
        mockProdutoRequest = Mock()
        
        mockProdutoRequest.id = 1

        MockProdutoRequest.return_value = mockProdutoRequest
        
        self.pedido_service.obter_produto(mockProdutoRequest)

    @patch('domain.services.Produto')
    def testAtualizarProdutoComSucesso(self, MockProdutoRequest):
        mockProdutoRequest = Mock()
        
        mockProdutoRequest.id = 1
        mockProdutoRequest.code = "1234"
        mockProdutoRequest.description = "Descrição Teste"
        mockProdutoRequest.price = 5.99
        mockProdutoRequest.category = "Lanche"

        MockProdutoRequest.return_value = mockProdutoRequest
        
        self.pedido_service.atualizar_produto(1, mockProdutoRequest)
    
    @patch('domain.services.Produto')
    def testDeletarProdutoComSucesso(self, MockProdutoRequest):
        mockProdutoRequest = Mock()
        
        mockProdutoRequest.id = 1

        MockProdutoRequest.return_value = mockProdutoRequest
        
        self.pedido_service.deletar_produto(mockProdutoRequest)
    
    def testValidarIDInvalido(self):
        with self.assertRaises(IdInvalido):
            self.pedido_service.validar_id("")
    
    def testValidarCodeInvalido(self):
        with self.assertRaises(CodigoInvalido):
            produto = Produto(id=1, code="", description="Desc", price=5.99, category="Lanche")
            self.pedido_service.validar_produto(produto)

    def testValidarPriceInvalido(self):
        with self.assertRaises(ValorInvalido):
            produto =Produto(id=1, code="Cod", description="Desc", price=0, category="Lanche")
            self.pedido_service.validar_produto(produto)

    def testValidarCategoryInvalido(self):
        with self.assertRaises(CategoriaInvalido):
            produto =Produto(id=1, code="Cod", description="Desc", price=5.99, category="")
            self.pedido_service.validar_produto(produto)

    def testValidarDescricaoInvalido(self):
        with self.assertRaises(DescricaoInvalido):
            produto =Produto(id=1, code="Cod", description="", price=5.99, category="")
            self.pedido_service.validar_produto(produto)


if __name__ == "__main__":
    unittest.main()