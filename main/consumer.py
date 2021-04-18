import pika
import os
import json
from app import Product, db

url = os.environ.get('CLOUDAMQP_URL', 'amqps://oohvqrza:qabN5LAF9yQyv_9bwaMh-VXRzMts5Dpe@jaguar.rmq.cloudamqp.com/oohvqrza')
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='main')


def callback(ch, method, properties, body):
    print(" [x] Received from main")
    data = json.loads(body)
    print(data)
    if properties.content_type == 'product_created':
        product = Product(id=data['id'], title=data['title'], image=data['image'])
        db.session.add(product)
        db.session.commit()
    elif properties.content_type == 'product_updated':
        product = Product.query.get(data['id'])
        print(product)
        product.title = data['title']
        product.image = data['image']
        db.session.commit()
    elif properties.content_type == 'product_deleted':
        product = Product.query.get(data)
        db.session.delete(product)
        db.session.commit()


channel.basic_consume(queue='main',
                      on_message_callback=callback,
                      auto_ack=True)

print(' [*] Waiting for messages:')
channel.start_consuming()
connection.close()
