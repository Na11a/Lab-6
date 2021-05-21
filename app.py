from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://test:123456@localhost/pill'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Pillow(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100), unique=True)
  description = db.Column(db.String(200))
  price = db.Column(db.Float)
  width = db.Column(db.Integer)
  height = db.Column(db.Integer)


  def __init__(self, title, description, price, width,height):
    self.title = title
    self.description = description
    self.price = price
    self.width = width
    self.height = height


class PillowSchema(ma.Schema):
  class Meta:
    fields = ('id', 'title', 'description', 'price', 'width','height')

pillow_schema = PillowSchema()
pillows_schema = PillowSchema(many=True)

@app.route('/pillow', methods=['POST'])
def add_pillow():
  print(request.json)

  title = request.json['title']
  description = request.json['description']
  price = request.json['price']
  width = request.json['width']
  height = request.json['height']

  new_pillow = Pillow(title, description, price, width,height)

  db.session.add(new_pillow)
  db.session.commit()

  return pillow_schema.jsonify(new_pillow)

@app.route('/pillow', methods=['GET'])
def get_pillows():
  all_pillows = Pillow.query.all()
  result = pillows_schema.dump(all_pillows)
  return jsonify(result)

@app.route('/pillow/<id>', methods=['GET'])
def get_pillow(id):
  pillow = Pillow.query.get(id)
  return pillow_schema.jsonify(pillow)

@app.route('/pillow/<id>', methods=['PUT'])
def update_pillow(id):
  pillow = Pillow.query.get(id)
  title = request.json['title']
  description = request.json['description']
  price = request.json['price']
  width = request.json['width']
  height = request.json['height']

  pillow.title = title
  pillow.description = description
  pillow.price = price
  pillow.width = width
  pillow.height = height

  db.session.commit()

  return pillow_schema.jsonify(pillow)

@app.route('/pillow/<id>', methods=['DELETE'])
def delete_pillow(id):
  pillow = Pillow.query.get(id)
  db.session.delete(pillow)
  db.session.commit()

  return pillow_schema.jsonify()

if __name__ == '__main__':
  app.run(debug=True)