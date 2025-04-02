
from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///superheroes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

# GET /heroes
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    heroes_dict = [hero.to_dict() for hero in heroes]
    return jsonify(heroes_dict)

# GET /heroes/:id
@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({"error": "Hero not found"}), 404
    
    return jsonify(hero.to_dict(include_powers=True))

# GET /powers
@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    powers_dict = [power.to_dict() for power in powers]
    return jsonify(powers_dict)

# GET /powers/:id
@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404
    
    return jsonify(power.to_dict())

# PATCH /powers/:id
@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404
    
    data = request.get_json()
    
    try:
        if 'description' in data:
            power.description = data['description']
        
        db.session.commit()
        return jsonify(power.to_dict())
    
    except ValueError as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 400

# POST /hero_powers
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    
    try:
        hero = Hero.query.get(data.get('hero_id'))
        power = Power.query.get(data.get('power_id'))
        
        if not hero or not power:
            return jsonify({"errors": ["Hero or Power not found"]}), 404
        
        hero_power = HeroPower(
            strength=data.get('strength'),
            hero_id=data.get('hero_id'),
            power_id=data.get('power_id')
        )
        
        db.session.add(hero_power)
        db.session.commit()
        
        return jsonify(hero_power.to_dict())
    
    except ValueError as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 400


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(port=5555, debug=True)