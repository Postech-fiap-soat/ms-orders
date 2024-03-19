from sqlalchemy import create_engine, Table, MetaData, select, update, insert, Column, String, Text, Integer, Float, ForeignKey, delete
from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy.exc import NoResultFound, IntegrityError
from typing import Optional, List 
from domain.models import Produto,Pedido
from adapter.exceptions import DatabaseException
from port.repositories import PedidoRepository

class PedidoMySQLAdapter(PedidoRepository): # pragma: no cover
    def __init__(self, database_url: str):
        self.__engine = create_engine(database_url)
        self.__metadata = MetaData()

        # Tabela de Pedido
        self.__pedido_table = Table(
            'Pedido', self.__metadata,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('client_id', Integer),
            Column('cart_id', Integer),
            Column('observation', String(255)),
            Column('totalPrice', Float),
            Column('payment_status', Integer, default=1),
            Column('order_status', Integer, default=1)
        )

        # Tabela Cliente
        self.__cliente_table = Table(
            'Cliente', self.__metadata,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('name', String(255)),
            Column('cpf', String(14)),
            Column('email', String(255)),
        )

        # Tabela Carrinho
        self.__carrinho_table = Table(
            'Carrinho', self.__metadata,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('order_id', Integer, ForeignKey('Pedido.id')),
            
        )

        # Tabela ItemCarrinho
        self.__item_carrinho_table = Table(
            'ItemCarrinho', self.__metadata,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('product_id', Integer, ForeignKey('Produto.id')),
            Column('cart_id', Integer, ForeignKey('Carrinho.id')),
            Column('count', Integer),
            Column('observation', String(255)),
        )

        # Tabela Produto
        self.__produto_table = Table(
            'Produto', self.__metadata,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('code', String(50)),
            Column('description', String(255)),
            Column('price', Float),
            Column('category', String(50)),
        )

        # Configuração da sessão
        self.__session = sessionmaker(autocommit=False, autoflush=False, bind=self.__engine)

    #PEDIDO

    def inserirPedido(self, pedido: Pedido, on_duplicate_sku: Exception):
        session = self.__session()
        try:

            # Iniciar transação
            session.begin()
            
            # Criar um novo pedido na tabela 'Pedido'
            insert_query_pedido = insert(self.__pedido_table).values(
                client_id=pedido.client.id,
                cart_id=pedido.cart.id,
                observation=pedido.observation,
                totalPrice=pedido.totalPrice,
                payment_status=1,  # Valor padrão
                order_status=1  # Valor padrão
            )
            result_pedido = session.execute(insert_query_pedido)

            # Obter o ID do pedido recém-inserido
            pedido_id = result_pedido.inserted_primary_key[0]

            # Criar um novo carrinho na tabela 'Carrinho'
            insert_query_carrinho = insert(self.__carrinho_table).values(order_id=pedido_id)
            result_carrinho = session.execute(insert_query_carrinho)

            # Obter o ID do carrinho recém-inserido
            carrinho_id = result_carrinho.inserted_primary_key[0]

            # Criar itens do carrinho na tabela 'ItemCarrinho'
            for item in pedido.cart.items:
                insert_query_item_carrinho = insert(self.__item_carrinho_table).values(
                    product_id=item.product.id,
                    cart_id=carrinho_id,
                    count=item.count,
                    observation=item.observation
                )
                session.execute(insert_query_item_carrinho)

            # Confirmar as mudanças
            session.commit()
        except IntegrityError as e:
            session.rollback()
            raise DatabaseException({
                "code": "database.error.integrity",
                "message": f"Integridade do banco de dados violada: {e}",
            })
        except Exception as e:
            session.rollback()
            
            raise DatabaseException({
                "code": "database.error.insert",
                "message": f"Problema ao inserir pedido no banco de dados: {e}",
            })
        finally:
            session.close()
   
    def buscarPedidoPorID(self, pedido_id: int, on_not_found: Exception) -> Pedido:
        query = select(self.__pedido_table).where(self.__pedido_table.c.id == pedido_id)

        with self.__engine.connect() as connection:
            try:
                result = connection.execute(query).fetchone()
                if result is None:
                    raise on_not_found
        
                # Mapear valores para nomes de colunas
                pedido_column_names = [column.name for column in self.__pedido_table.c]
                pedido_dict = dict(zip(pedido_column_names, result))

                
                return pedido_dict
            except NoResultFound:
                raise on_not_found

    def buscarPedidoPorStatus(self, status: int, on_not_found: Exception) -> List[Pedido]:
        query = select(self.__pedido_table).where(self.__pedido_table.c.order_status == status)

        with self.__engine.connect() as connection:
            try:
                result = connection.execute(query).fetchone()
                if result is None:
                    raise on_not_found
        
                # Mapear valores para nomes de colunas
                pedido_column_names = [column.name for column in self.__pedido_table.c]
                pedido_dict = dict(zip(pedido_column_names, result))

                
                return pedido_dict
            except NoResultFound:
                raise on_not_found
            
    def buscarPedidoIncompleto(self, on_not_found: Exception) -> List[Pedido]:
        query = select(self.__pedido_table).where(self.__pedido_table.c.order_status != 4)

        with self.__engine.connect() as connection:
            try:
                result = connection.execute(query).fetchone()
                if result is None:
                    raise on_not_found
        
                # Mapear valores para nomes de colunas
                pedido_column_names = [column.name for column in self.__pedido_table.c]
                pedido_dict = dict(zip(pedido_column_names, result))

                
                return pedido_dict
            except NoResultFound:
                raise on_not_found

    def atualizarStatusPedido(self, pedido_id: int, new_order_status: Optional[int] = None, new_payment_status: Optional[int] = None, on_not_found: Exception = None):
        session = self.__session()
        try:
            session.begin()

            # Verificar se o pedido existe
            pedido_query = select(self.__pedido_table.c.id).where(self.__pedido_table.c.id == pedido_id)
            pedido_exists = session.execute(pedido_query).scalar()

            if not pedido_exists:
                raise on_not_found

            # Atualizar status do pedido, se fornecido
            if new_order_status is not None:
                update_order_query = update(self.__pedido_table).where(self.__pedido_table.c.id == pedido_id).values(order_status=new_order_status)
                session.execute(update_order_query)

            # Atualizar status de pagamento, se fornecido
            if new_payment_status is not None:
                update_payment_query = update(self.__pedido_table).where(self.__pedido_table.c.id == pedido_id).values(payment_status=new_payment_status)
                session.execute(update_payment_query)

            session.commit()
        except Exception as e:
            session.rollback()
            if type(e) is type(on_not_found):
                raise

            raise DatabaseException({
                "code": "database.error.update",
                "message": f"Problema ao atualizar pedido no banco de dados: {e}",
            })
        finally:
            session.close()

    def efetuarCheckoutPedido(self, pedido_id: int,on_not_found: Exception) -> Pedido:
        session = self.__session()
        try:
            session.begin()

            # Verificar se o pedido existe
            pedido_query = select(self.__pedido_table.c.id).where(self.__pedido_table.c.id == pedido_id)
            pedido_exists = session.execute(pedido_query).scalar()

            if not pedido_exists:
                raise on_not_found

            checkout_query = update(self.__pedido_table).where(self.__pedido_table.c.id == pedido_id).values(payment_status=2)
            session.execute(checkout_query)

            session.commit()
        except Exception as e:
            session.rollback()
            if type(e) is type(on_not_found):
                raise

            raise DatabaseException({
                "code": "database.error.update",
                "message": f"Problema ao atualizar pedido no banco de dados: {e}",
            })
        finally:
            session.close()

    #PRODUTO
    
    def inserirProduto(self, produto: Produto, on_duplicate_sku: Exception):
        session = self.__session()
        try:
            session.begin()

            # Verificar se já existe um produto com o mesmo ID
            id_exists = session.execute(select(self.__produto_table.c.id).where(self.__produto_table.c.id == produto.id)).scalar()
            if id_exists:
                raise on_duplicate_sku

            # Inserir o novo produto
            insert_query = insert(self.__produto_table).values(
                code=produto.code,
                description=produto.description,
                price=produto.price,
                category=produto.category
            )
            session.execute(insert_query)

            session.commit()
        except IntegrityError as e:
            session.rollback()
            if type(e) is type(on_duplicate_sku):
                raise

            raise DatabaseException({
                "code": "database.error.insert",
                "message": f"Problema ao inserir produto no banco de dados: {e}",
            })
        finally:
            session.close()

    def buscarProdutoPorID(self, produto_id: int, on_not_found: Exception) -> Produto:
        
        query = select(self.__produto_table).where(self.__produto_table.c.id == produto_id)

        with self.__engine.connect() as connection:
            try:
                result = connection.execute(query).fetchone()
                if result is None:
                    raise on_not_found
        
                # Mapear valores para nomes de colunas
                produto_column_names = [column.name for column in self.__produto_table.c]
                produto_dict = dict(zip(produto_column_names, result))

                # Criar objeto Pedido diretamente
                produto = Produto(**produto_dict)

                
                return produto
            except NoResultFound:
                raise on_not_found
            
    def buscarProdutos(self, on_not_found: Exception) -> List[Produto]:
        query = select(self.__produto_table)

        with self.__engine.connect() as connection:
            try:
                result = connection.execute(query).fetchone()
                if result is None:
                    raise on_not_found
        
                # Mapear valores para nomes de colunas
                produto_column_names = [column.name for column in self.__produto_table.c]
                produto_dict = dict(zip(produto_column_names, result))

                
                return produto_dict
            except NoResultFound:
                raise on_not_found

    def excluirProduto(self, produto_id: int, on_not_found: Exception):
        session = self.__session()
        try:
            session.begin()

            # Verificar se o produto existe
            produto_exists = session.execute(select(self.__produto_table.c.id).where(self.__produto_table.c.id == produto_id)).scalar()
            if not produto_exists:
                raise on_not_found

            # Excluir o produto
            delete_query = delete(self.__produto_table).where(self.__produto_table.c.id == produto_id)
            session.execute(delete_query)

            session.commit()
        except Exception as e:
            session.rollback()
            if type(e) is type(on_not_found):
                raise

            raise DatabaseException({
                "code": "database.error.delete",
                "message": f"Problema ao excluir produto no banco de dados: {e}",
            })
        finally:
            session.close()

    def atualizarProduto(self, produto: Produto, on_not_found: Exception):
        session = self.__session()
        try:
            session.begin()

            # Verificar se o produto existe
            produto_exists = session.execute(select(self.__produto_table.c.id).where(self.__produto_table.c.id == produto.id)).scalar()
            if not produto_exists:
                raise on_not_found

            # Atualizar informações do produto na tabela
            update_query = update(self.__produto_table).where(self.__produto_table.c.id == produto.id).values(
                description=produto.description,
                price=produto.price
            )
            session.execute(update_query)

            session.commit()
        except Exception as e:
            session.rollback()
            if type(e) is type(on_not_found):
                raise

            raise DatabaseException({
                "code": "database.error.update",
                "message": f"Problema ao atualizar produto no banco de dados: {e}",
            })
        finally:
            session.close()