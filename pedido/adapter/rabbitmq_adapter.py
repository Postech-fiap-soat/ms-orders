import pika

class RabbitMQAdapter:
    def __init__(self, host, port, username, password, queue_name):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.queue_name = queue_name
        self.connection = None
        self.channel = None

    def connect(self):
        try:
            print("Connecting to RabbitMQ...")
            credential = pika.PlainCredentials(self.username, self.password)
            parameter = pika.ConnectionParameters(host=self.host, port=self.port, virtual_host="/",credentials=credential)
            self.connection = pika.BlockingConnection(parameters=parameter)
            print("Successfully connected to RabbitMQ")
        except Exception as e:
            print(e)

    def publish_message(self, message):
        if self.connection is None or self.connection.is_closed:
            raise RuntimeError("Connection is not established or is closed")
        
        if self.channel is None or self.channel.is_closed:
            self.channel = self.connection.channel()

        self.channel.basic_publish(exchange='ex_pedidos', routing_key=self.queue_name, body=message)


    def close_connection(self):
        if self.connection:
            self.connection.close()