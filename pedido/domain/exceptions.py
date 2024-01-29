#-----------DEFAULT----------
class ValorInvalido(Exception):
    pass
class IdInvalido(Exception):
    pass
class PrecoInvalido(Exception):
    pass

#----------PRODUTO----------
class ErroAoCriarProduto(Exception):
    pass
        
class ProdutoNaoEncontrado(Exception):
    pass

class ErroAoDeletarProduto(Exception):
    pass

class ProdutoInvalido(Exception):
    pass

class ProdutoJaExiste(Exception):
    pass

class ErroAoObterProduto(Exception):
    pass

class ErroAoAtualizarProduto(Exception):
    pass

class CodigoInvalido(Exception):
    pass

class DescricaoInvalido(Exception):
    pass

class CategoriaInvalido(Exception):
    pass

#----------PEDIDO-------------

class StatusInvalido(Exception):
    pass
class PedidoNaoEncontrado(Exception):
    pass

class PedidoJaExistente(Exception):
    pass

class PedidoInvalido(Exception):
    pass

class ErroAoCriarPedido(Exception):
    pass

class PedidoIDInvalido(Exception):
    pass

class ErroAoObterPedido(Exception):
    pass

class ErroAoAtualizarPedido(Exception):
    pass

class ErroAoDeletarPedido(Exception):
    pass



#----------Carrinho--------------

class CarrinhoInvalido(Exception):
    pass

#Item Carrinho

class ItemCarrinhoInvalido(Exception):
    pass

#CLiente

class ClienteInvalido(Exception):
    pass