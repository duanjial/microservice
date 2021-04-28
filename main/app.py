from dataclasses import dataclass
from producer import publish
from publisher import PubSubPublisher
import requests
from flask import Flask, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import UniqueConstraint
from downloader import Downloader

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:root@db/main'
CORS(app)

db = SQLAlchemy(app)
PROJECT_ID = "microservice-311821"
TOPIC = "download"
publisher = PubSubPublisher(PROJECT_ID)
if not publisher.is_topic_exist(TOPIC):
    publisher.create_topic(TOPIC)


@dataclass
class Product(db.Model):
    id: int
    title: str
    image: str
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))


@dataclass
class User(db.Model):
    id: int
    user_id: int
    product_id: int
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    UniqueConstraint('user_id', 'product_id', name='user_product_unique')


@app.route('/api/products')
def index():
    return jsonify(Product.query.all())


@app.route('/api/products/<int:id>/like', methods=['POST'])
def like(id):
    req = requests.get('http://docker.for.mac.localhost:7000/api/user')
    data = req.json()
    try:
        product_user = User(user_id=data['id'], product_id=id)
        db.session.add(product_user)
        db.session.commit()
        publish('product_liked', id)
    except:
        abort(400, 'You already liked this product')

    return jsonify({
        'message': 'success'
    })


@app.route('/api/download', methods=['POST'])
def download():
    request_data = request.get_json()
    url = request_data['url']
    Downloader.download(url=url)
    publisher.publish_message(f"new mp4 SUCCESSFULLY downloaded from {url}")
    return jsonify({
        'message': f'download success, published msg to {PROJECT_ID} - {TOPIC}'
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
