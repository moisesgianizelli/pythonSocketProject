import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='activity_log')

def callback(ch, method, properties, body):
    print(f"Received message: {body}")

channel.basic_consume(queue='activity_log', on_message_callback=callback, auto_ack=True)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()