from unittest import TestCase
from unittest.mock import patch, Mock
from adapter.exceptions import *
from adapter.http_api import PedidoHTTPAPIAdapter
from domain.exceptions import IdInvalido,CategoriaInvalido
from domain.models import *
from fastapi import HTTPException
from adapter.sqs_adapter import *
from adapter.mysql_adapter import *
import unittest


class TestPedidoHTTPAPIAdapter(TestCase): 
    def setUp(self):
        self.pedido_service = Mock()
        self.httpAdapter = PedidoHTTPAPIAdapter(pedido_service=self.pedido_service)

    @patch('adapter.http_api.Pedido')
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
        
        response = self.httpAdapter.criar_pedido(mockPedidoRequest)
        
        self.assertEqual(response, {"message": "Pedido criado com sucesso"})
        self.pedido_service.criar_pedido.assert_called()
    
    @patch('adapter.http_api.Produto')
    def testCriarProdutoComSucesso(self, MockProdutoRequest):
        mockProdutoRequest = Mock()
        
        mockProdutoRequest.id = 1
        mockProdutoRequest.code = "123"
        mockProdutoRequest.description = "Descrição Teste"
        mockProdutoRequest.price = 5.99
        mockProdutoRequest.category = "Lanche"

        MockProdutoRequest.return_value = mockProdutoRequest
        
        response = self.httpAdapter.criar_produto(mockProdutoRequest)
        
        self.assertEqual(response, {"message": "Produto criado com sucesso"})
        self.pedido_service.criar_produto.assert_called()

    @patch('adapter.http_api.Produto')
    def testCriarProdutoComErro400(self, MockProdutoRequest):
        mockProdutoRequest = Mock()
        
        mockProdutoRequest.id = 1
        mockProdutoRequest.code = "123"
        mockProdutoRequest.description = "Descrição Teste"
        mockProdutoRequest.price = 5.99
        mockProdutoRequest.category = ""

        MockProdutoRequest.return_value = mockProdutoRequest
        
        
        # Configurando o mock para lançar uma exceção CategoriaInvalido quando criar_produto for chamado
        self.pedido_service.criar_produto.side_effect = IdInvalido("ID é obrigatório")
        
        # Verificando se a exceção HTTP 400 é lançada
        with self.assertRaises(HTTPException) as context:
            print(context)
            self.httpAdapter.criar_produto(mockProdutoRequest)
            # Verificando o código de status da exceção
            self.assertEqual(context.exception.status_code, 500)
            self.assertTrue("Erro ao criar produto: ID é obrigatório" in str(context.exception.detail))

    @patch('adapter.http_api.Produto')
    def testCriarProdutoComErro500(self, MockProdutoRequest):
        mockProdutoRequest = Mock()
        
        mockProdutoRequest.id = ""
        mockProdutoRequest.code = "123"
        mockProdutoRequest.description = "Descrição Teste"
        mockProdutoRequest.price = 5.99
        mockProdutoRequest.category = "asd"

        MockProdutoRequest.return_value = mockProdutoRequest
        
        
        # Configurando o mock para lançar uma exceção CategoriaInvalido quando criar_produto for chamado
        self.pedido_service.criar_produto.side_effect = CategoriaInvalido("Campo Categoria é obrigatório")
        
        # Verificando se a exceção HTTP 400 é lançada
        with self.assertRaises(HTTPException) as context:
            print(context)
            self.httpAdapter.criar_produto(mockProdutoRequest)
            # Verificando o código de status da exceção
            self.assertEqual(context.exception.status_code, 400)
            self.assertTrue("Erro ao criar produto: Campo Categoria é obrigatório" in str(context.exception.detail))

    @patch('adapter.http_api.Produto')
    def testObterPedidoComSucesso(self, MockPedidoRequest):
        mockPedidoRequest = Mock()
        
        mockPedidoRequest.id = 1

        MockPedidoRequest.return_value = mockPedidoRequest
        
        self.httpAdapter.obter_pedido(mockPedidoRequest)
        
        # Verificando se a função obter_produto foi chamada corretamente
        self.pedido_service.obter_pedido.assert_called_once_with(mockPedidoRequest)

    @patch('adapter.http_api.Produto')
    def testObterProdutoComSucesso(self, MockProdutoRequest):
        mockProdutoRequest = Mock()
        
        mockProdutoRequest.id = 1

        MockProdutoRequest.return_value = mockProdutoRequest
        
        self.httpAdapter.obter_produto(mockProdutoRequest)
        
        # Verificando se a função obter_produto foi chamada corretamente
        self.pedido_service.obter_produto.assert_called_once_with(mockProdutoRequest)

    @patch('adapter.http_api.Pedido')
    def testAtualizarStatusPedidoComSucesso(self, MockPedidoRequest):
        mockPedidoRequest = Mock()
        
        mockPedidoRequest.id = 1
        mockPedidoRequest.order_status = 2

        MockPedidoRequest.return_value = mockPedidoRequest
        
        self.httpAdapter.atualizar_status_pedido(mockPedidoRequest)

    @patch('adapter.http_api.Pedido')
    def testObterPedidoPorStatusComSucesso(self, MockPedidoRequest):
        mockPedidoRequest = Mock()
        
        mockPedidoRequest.order_status = 2

        MockPedidoRequest.return_value = mockPedidoRequest
        
        self.httpAdapter.obter_pedidos_por_status(mockPedidoRequest)

    @patch('adapter.http_api.Pedido')
    def testObterPedidoIncompletoComSucesso(self, MockPedidoRequest):
        mockPedidoRequest = Mock()
        
        MockPedidoRequest.return_value = mockPedidoRequest
        
        self.httpAdapter.obter_pedidos_nao_concluidos()

    @patch('adapter.http_api.Pedido')
    def testCheckoutPedidoComSucesso(self, MockPedidoRequest):
        mockPedidoRequest = Mock()
        
        mockPedidoRequest.id = 1

        MockPedidoRequest.return_value = mockPedidoRequest
        
        self.httpAdapter.checkout_pedido(mockPedidoRequest)

    @patch('adapter.http_api.Produto')
    def testAtualizarProdutoComSucesso(self, MockProdutoRequest):
        mockProdutoRequest = Mock()
        
        mockProdutoRequest.id = 1
        mockProdutoRequest.code = "1234"
        mockProdutoRequest.description = "Descrição Teste"
        mockProdutoRequest.price = 5.99
        mockProdutoRequest.category = "Lanche"

        MockProdutoRequest.return_value = mockProdutoRequest
        
        self.httpAdapter.atualizar_produto(1, mockProdutoRequest)
    
    @patch('adapter.http_api.Produto')
    def testDeletarProdutoComSucesso(self, MockProdutoRequest):
        mockProdutoRequest = Mock()
        
        mockProdutoRequest.id = 1

        MockProdutoRequest.return_value = mockProdutoRequest
        
        self.httpAdapter.deletar_produto(mockProdutoRequest)


if __name__ == "__main__":
    unittest.main()