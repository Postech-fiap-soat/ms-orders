-- Create a user for the 'pedido' database
CREATE USER 'pedido_user'@'%' IDENTIFIED BY 'Mudar123!';
GRANT ALL PRIVILEGES ON pedido.* TO 'pedido_user'@'%';

-- Flush privileges to apply changes
FLUSH PRIVILEGES;