#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

@app.route('/')
def home():
    return "Hello, World!"

class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        plants_list = [{"id": plant.id, "name": plant.name, "image": plant.image, "price": plant.price} for plant in plants]
        return jsonify(plants_list)

    def post(self):
        data = request.get_json()
        new_plant = Plant(name=data['name'], image=data['image'], price=data['price'])
        db.session.add(new_plant)
        db.session.commit()
        return jsonify({"id": new_plant.id, "name": new_plant.name, "image": new_plant.image, "price": new_plant.price})

class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.get_or_404(id)
        return jsonify({"id": plant.id, "name": plant.name, "image": plant.image, "price": plant.price})

    def delete(self, id):
        plant = Plant.query.get_or_404(id)
        db.session.delete(plant)
        db.session.commit()
        return '', 204

api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
