import pika
import os


url = os.environ.get('CLOUDAMQP_URL', 'amqps://oohvqrza:qabN5LAF9yQyv_9bwaMh-VXRzMts5Dpe@jaguar.rmq.cloudamqp.com/oohvqrza')
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='admin')


def callback(ch, method, properties, body):
    print(" [x] Received from admin")
    print(body)


channel.basic_consume(queue='admin',
                      on_message_callback=callback,
                      auto_ack=True)

print(' [*] Waiting for messages:')
channel.start_consuming()
connection.close()
