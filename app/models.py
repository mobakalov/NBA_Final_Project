from app import db, login
from flask_login import UserMixin #This is just for the user model 
from datetime import datetime as dt 
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship



class Usersplayers(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.main_id'), primary_key=True)

    def __repr__(self):
        return f'<User: {self.user_id} | {self.player_id}>'

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(200))
    created_on = db.Column(db.DateTime, default = dt.utcnow)
    squad = db.relationship(
        'Player',
        secondary = 'usersplayers',
        backref ='user',
        lazy ='dynamic',
    )

    def __repr__(self):
        return f'<User: {self.id} | {self.email}>'
    
    def hash_password(self, original_password):
        return generate_password_hash(original_password)
    
    def check_hashed_password(self, login_password):
        return check_password_hash(self.password, login_password)

    def team_full(self):
        print(self.squad.count())
        return self.squad.count() < 5
    
    def add_to_team(self, obj):
            self.squad.append(obj)
            self.save()
    
    def inteam(self, thisid):
        if self.squad.query.filter_by(player_id=thisid).first() != None:
            return True
        else:
            return False
    
    def getme(self, thisid):
        return self.squad.query.filter_by(player_id=thisid).first()
        
    

    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = self.hash_password(data['password'])

    def save(self):
        db.session.add(self)
        db.session.commit()

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Player (db.Model):
    main_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(200))
    last_name = db.Column(db.String(200))
    full_name = db.Column(db.String(250))
    position = db.Column(db.String(50))
    team = db.Column(db.String(100))
    height = db.Column(db.String(50))
    weight = db.Column(db.String(50))

    def __repr__(self):
        return f'<Post: {self.main_id} | {self.full_name}>'

    def from_dict(self, data):
        self.main_id = data['main_id']
        self.full_name = data['full_name']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.position = data['position']
        self.team = data['team']
        self.height = data['height']
        self.weight = data['weight']


    def exists(name):
        return Player.query.filter_by(full_name=name).first()

    def existsid(self, id):
        return Player.query.filter_by(main_id=id).first()
    
    def existsids(id):
        return Player.query.filter_by(main_id=id).first()
    
    def save(self):
        db.session.add(self) 
        db.session.commit() 


class Stats (db.Model):
    stat_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    main_id = db.Column(db.Integer)
    season= db.Column(db.Integer)
    ppg = db.Column(db.String(20))
    rpg = db.Column(db.String(20))
    apg = db.Column(db.String(250))
    mpg = db.Column(db.String(50))
    spg = db.Column(db.String(100))
    bpg= db.Column(db.String(50))
    tpg = db.Column(db.String(50))
    pf = db.Column(db.String(50))
    fgpct = db.Column(db.String(50))
    fgtpct = db.Column(db.String(50))
    ftpct = db.Column(db.String(50))
    games = db.Column(db.Integer)

    def from_dict(self, data):
        self.main_id = data['main_id']
        self.user_id=data['user_id']
        self.season = data['season']
        self.ppg = data['ppg']
        self.rpg = data['rpg']
        self.apg = data['apg']
        self.mpg = data['mpg']
        self.spg = data['spg']
        self.bpg=data['bpg']
        self.tpg=data['tpg']
        self.pf=data['pf']
        self.fgpct=data['fgpct']
        self.fgtpct=data['fgtpct']
        self.ftpct=data['ftpct']
        self.games=data['games']
    
    def existsid(self,id):
        return Stats.query.filter_by(main_id=id).first()
    
    def save(self):
        db.session.add(self) 
        db.session.commit() 
    
