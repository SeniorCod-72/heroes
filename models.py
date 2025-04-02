from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    super_name = db.Column(db.String, nullable=False)

    hero_powers = db.relationship('HeroPower', backref='hero', cascade='all, delete-orphan')
    

    serialize_rules = ('-hero_powers.hero',)
    
    def to_dict(self, include_powers=False):
        if include_powers:
            return {
                'id': self.id,
                'name': self.name,
                'super_name': self.super_name,
                'hero_powers': [hp.to_dict(include_hero=False, include_power=True) for hp in self.hero_powers]
            }
        return {
            'id': self.id,
            'name': self.name,
            'super_name': self.super_name
        }
    
 
    def get_powers(self):
        return [hero_power.power for hero_power in self.hero_powers]

class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    
    hero_powers = db.relationship('HeroPower', backref='power', cascade='all, delete-orphan')
    
    serialize_rules = ('-hero_powers.power',)
    
    @validates('description')
    def validate_description(self, key, description):
        if not description or len(description) < 20:
            raise ValueError("Description must be present and at least 20 characters long")
        return description
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
    
    def get_heroes(self):
        return [hero_power.hero for hero_power in self.hero_powers]

class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)
    
    serialize_rules = ('-hero.hero_powers', '-power.hero_powers')
    
    @validates('strength')
    def validate_strength(self, key, strength):
        valid_strengths = ['Strong', 'Weak', 'Average']
        if strength not in valid_strengths:
            raise ValueError("Strength must be one of the following values: 'Strong', 'Weak', 'Average'")
        return strength
    
    def to_dict(self, include_hero=True, include_power=True):
        result = {
            'id': self.id,
            'hero_id': self.hero_id,
            'power_id': self.power_id,
            'strength': self.strength
        }
        
        if include_hero:
            result['hero'] = {
                'id': self.hero.id,
                'name': self.hero.name,
                'super_name': self.hero.super_name
            }
            
        if include_power:
            result['power'] = {
                'id': self.power.id,
                'name': self.power.name,
                'description': self.power.description
            }
            
        return result
