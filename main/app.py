from dataclasses import dataclass
from utils.producer import publish
import requests
import settings
from flask import Flask, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import UniqueConstraint
from services.download_service import DownloadService
from services.pubsub_service import PubSubService

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = settings.DATABASE_URI
CORS(app)

db = SQLAlchemy(app)
download_service = DownloadService()
pubsub_service = PubSubService(settings.PROJECT_ID)


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
    downloaded = download_service.download_with_url(url=url)
    if downloaded:
        pubsub_service.create_topic(settings.TOPIC)
        pubsub_service.publish(f"new mp4 SUCCESSFULLY downloaded from {url}")
        return jsonify({
            'message': f'download success, published msg to {settings.PROJECT_ID} - {settings.TOPIC}'
        })
    else:
        return jsonify({
            'message': 'File already downloaded'
        })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
