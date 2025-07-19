import pika
import json
from .container import WorkerContainer # Un contenedor de DI específico para el worker
# from ..contexts.users.application.commands import CreateUserCommand
from ..contexts.users.application.commands import CreateUserCommand


def main():
    container = WorkerContainer()
    container.wire(modules=[__name__])

    # connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    
    # 1. Usar la configuración del contenedor para la conexión
    credentials = pika.PlainCredentials(
        username=container.config.RABBITMQ_USER(),
        password=container.config.RABBITMQ_PASS()
    )
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=container.config.RABBITMQ_HOST(), credentials=credentials)
    )
    
    channel = connection.channel()

    # queue_name = "user_creation_queue"
    # 2. El nombre de la cola debe coincidir con el routing_key que usa el publicador
    #    con el exchange por defecto. En este caso es "user.create".
    queue_name = "user.create"
    
    channel.queue_declare(queue=queue_name, durable=True)

    def callback(ch, method, properties, body):
        print(f" [x] Received command routing key: {method.routing_key}")
        data = json.loads(body)
        
        if method.routing_key == "user.create":
            command = CreateUserCommand(**data)
            user_creator = container.user_creator()
            try:
                user_creator.handle(command)
                print(f" [✔] User {command.email} created successfully.")
            except ValueError as e:
                print(f" [!] Error creating user: {e}")

        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    print(' [*] Waiting for commands. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')