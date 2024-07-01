from flask_sqlalchemy import SQLAlchemy # type: ignore
 

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
   
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    FavoritePlanets=db.relationship('FavoritePlanets',backref='user',lazy=True)
    FavoritePeople=db.relationship('FavoritePeople',backref='user',lazy=True)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class People(db.Model):
    __tablename__ = 'people'  
    id = db.Column(db.Integer, primary_key=True)   
    name = db.Column(db.String(30), nullable = False, unique = False )
    FavoritePeople=db.relationship('FavoritePeople',backref='people',lazy=True)


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }
    
class Planets(db.Model): 
    __tablename__ = 'planets' 
    id = db.Column(db.Integer, primary_key=True)   
    name = db.Column(db.String(30), nullable = False, unique = False )
    FavoritePlanets=db.relationship('FavoritePlanets',backref='planets',lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        } 

class FavoritePlanets(db.Model):  
    id = db.Column(db.Integer, primary_key=True)   
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable = False )
    planets_id = db.Column(db.Integer,db.ForeignKey('planets.id'), nullable = False )
   


    def serialize(self):
        return {
            "id": self.id
        } 
     
class FavoritePeople(db.Model):  
    id = db.Column(db.Integer, primary_key=True)   
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable = False )
    people_id = db.Column(db.Integer,db.ForeignKey('people.id'), nullable = False )
   

    def serialize(self):
        return {
            "id": self.id
        }      