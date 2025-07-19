import pika

# Conexión

# 1. Usar la configuración del contenedor para la conexión
credentials = pika.PlainCredentials(
    username="admin",
    password="admin"
)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', credentials=credentials))
channel = connection.channel()

# Declarar la cola
queue_name = 'user_events'
channel.queue_declare(queue=queue_name, durable=True)

# Función de callback para procesar mensajes
def callback(ch, method, properties, body):
    print(f" [x] Recibido {body.decode()}")
    # Puedes procesar el mensaje aquí
    ch.basic_ack(delivery_tag=method.delivery_tag) # Confirmar recepción

# Consumir mensajes
channel.basic_consume(queue=queue_name, on_message_callback=callback)

print(' [*] Esperando mensajes.  Presiona CTRL+C para salir')
channel.start_consuming()