import pika
import os
import django
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
django.setup()

from products.models import Product

url = os.environ.get('CLOUDAMQP_URL', 'amqps://oohvqrza:qabN5LAF9yQyv_9bwaMh-VXRzMts5Dpe@jaguar.rmq.cloudamqp.com/oohvqrza')
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='admin')


def callback(ch, method, properties, body):
    print(" [x] Received from admin")
    product_id = json.loads(body)
    print(product_id)
    product = Product.objects.get(id=product_id)
    product.likes = product.likes + 1
    product.save()
    print('Product likes increased')


channel.basic_consume(queue='admin',
                      on_message_callback=callback,
                      auto_ack=True)

print(' [*] Waiting for messages:')
channel.start_consuming()
connection.close()
