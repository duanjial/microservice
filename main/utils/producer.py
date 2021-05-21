import pika
import os
import json

url = os.environ.get('CLOUDAMQP_URL',
                        'amqps://oohvqrza:qabN5LAF9yQyv_9bwaMh-VXRzMts5Dpe@jaguar.rmq.cloudamqp.com/oohvqrza')

params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='admin', body=json.dumps(body), properties=properties)

