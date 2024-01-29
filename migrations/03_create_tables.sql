-- Usar o banco de dados 'pedido'
USE pedido;

-- Criação da tabela Produto
CREATE TABLE Produto (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    code VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL,
    price FLOAT NOT NULL,
    category VARCHAR(255) NOT NULL
);

-- Criação da tabela ItemCarrinho
CREATE TABLE ItemCarrinho (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    product_id INTEGER,
    cart_id INTEGER,
    count INTEGER NOT NULL,
    observation TEXT
);

-- Criação da tabela Carrinho
CREATE TABLE Carrinho (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    order_id INTEGER
);

-- Criação da tabela Cliente
CREATE TABLE Cliente (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    cpf VARCHAR(11) NOT NULL,
    email VARCHAR(255) NOT NULL
);

-- Criação da tabela Pedido
CREATE TABLE Pedido (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    cart_id INTEGER,
    client_id INTEGER,
    observation TEXT,
    totalPrice FLOAT NOT NULL,
    payment_status INTEGER,
    order_status INTEGER
);