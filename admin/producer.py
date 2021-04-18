import pika, os

url = os.environ.get('CLOUDAMQP_URL',
                        'amqps://oohvqrza:qabN5LAF9yQyv_9bwaMh-VXRzMts5Dpe@jaguar.rmq.cloudamqp.com/oohvqrza')

params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='admin')
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello CloudAMQP!')

print(" [x] Sent 'Hello World!'")
connection.close()

