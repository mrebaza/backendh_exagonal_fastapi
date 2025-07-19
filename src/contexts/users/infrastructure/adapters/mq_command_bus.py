import pika
from pika.exceptions import AMQPConnectionError

class RabbitMQCommandBus:
        
    def __init__(self, host: str, user: str, password: str):
        self.host = host
        self.user = user
        self.password = password
        self.connection = self.connect_to_rabbitmq()

    def connect_to_rabbitmq(self):

        """Implementa la conexión a RabbitMQ usando los parámetros."""
        try:
            credentials = pika.PlainCredentials(self.user, self.password)
            parameters = pika.ConnectionParameters(host=self.host, credentials=credentials)
            return pika.BlockingConnection(parameters)
        except AMQPConnectionError as e:
            # Es una buena práctica manejar los errores de conexión
            print(f"Error al conectar con RabbitMQ: {e}")
            # Podrías levantar una excepción personalizada o reintentar.
            return None
        
    def publish(self, routing_key: str, message: str):
        """
        Publica un mensaje en RabbitMQ.
        """
        if not self.connection or self.connection.is_closed:
            print("Error: No se puede publicar porque no hay conexión a RabbitMQ.")
            # En una aplicación real, podrías intentar reconectar o lanzar una excepción.
            return

        try:
            # Cada publicación usa su propio canal para ser thread-safe con BlockingConnection
            channel = self.connection.channel()
            # Declaramos la cola para asegurarnos que exista.
            channel.queue_declare(queue='user_events', durable=True)
            channel.basic_publish(
                exchange='',  # Usamos el exchange por defecto
                routing_key=routing_key,
                body=message
            )
            channel.close()
        except Exception as e:
            print(f"Error al publicar mensaje en RabbitMQ: {e}")
        