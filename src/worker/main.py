import time
import pika
import json
from .container import WorkerContainer
from ..contexts.users.application.commands import CreateUserCommand

def callback(ch, method, properties, body, container):
    print(f" [x] Received command routing key: {method.routing_key}")
    data = json.loads(body.decode("utf-8"))
    
    print(f" [DEBUG] Mensaje recibido: {data}")
    
    if method.routing_key == "user_events":
        try:
            command = CreateUserCommand(**data)
            print(f" [DEBUG] Comando creado: {command}")
            user_creator = container.user_creator()
            try:
                user_creator.handle(command)
                print(f" [✔] User {command.email} created successfully.")
            except ValueError as e:
                print(f" [!] Error creating user: {e}")
        except Exception as e:
            print(f" [!] Error procesando comando: {e}")
    else:
        print(f" [WARNING] Routing key desconocido: {method.routing_key}. Ignorando mensaje.")
    
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    print(" [INFO] Iniciando el worker...")
    container = WorkerContainer()
    container.wire(modules=[__name__])
    print(f" [INFO] Container configurado con RABBITMQ_HOST={container.config.RABBITMQ_HOST()}")

    credentials = pika.PlainCredentials(
        username=container.config.RABBITMQ_USER(),
        password=container.config.RABBITMQ_PASS()
    )
    print(f" [INFO] Credenciales configuradas: usuario={container.config.RABBITMQ_USER()}")

    while True:
        try:
            print(" [INFO] Intentando conectar a RabbitMQ...")
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=container.config.RABBITMQ_HOST(),
                    credentials=credentials,
                    heartbeat=600,
                    blocked_connection_timeout=300
                )
            )
            print(" [INFO] Conexión a RabbitMQ establecida")
            
            channel = connection.channel()
            queue_name = "user_events"
            channel.queue_declare(queue=queue_name, durable=True)
            print(f" [INFO] Cola {queue_name} declarada")
            
            channel.basic_consume(
                queue=queue_name,
                on_message_callback=lambda ch, method, properties, body: callback(ch, method, properties, body, container)
            )
            
            print(' [*] Waiting for commands. To exit press CTRL+C')
            channel.start_consuming()
            
        except pika.exceptions.AMQPConnectionError as e:
            print(f" [ERROR] Error de conexión a RabbitMQ: {e}. Reintentando en 5 segundos...")
            time.sleep(5)
        except pika.exceptions.ChannelError as e:
            print(f" [ERROR] Error en el canal: {e}. Reintentando en 5 segundos...")
            time.sleep(5)
        except Exception as e:
            print(f" [ERROR] Error inesperado: {e}. Reintentando en 5 segundos...")
            time.sleep(5)
        finally:
            if 'connection' in locals() and connection.is_open:
                print(" [INFO] Cerrando conexión a RabbitMQ")
                connection.close()

if __name__ == '__main__':
    print(" [INFO] Ejecutando el script principal...")
    try:
        main()
    except KeyboardInterrupt:
        print(' [INFO] Interrumpido por el usuario')