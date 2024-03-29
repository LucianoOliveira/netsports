from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    mobileNumber = db.Column(db.Integer, unique=True)
    user_type = db.Column(db.String(10)) #'User', 'Club', 'Admin'
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    birth_date = db.Column(db.Date)
    ustatus = db.Column(db.String(1))
    postal_code = db.Column(db.String(10))
    main_category = db.Column(db.Integer)
    mix_category = db.Column(db.Integer)
    notification_radius = db.Column(db.Integer)
    email_notification = db.Column(db.Boolean) #0:No 1:Yes
    sms_notification = db.Column(db.Boolean) #0:No 1:Yes
    app_notification = db.Column(db.Boolean) #0:No 1:Yes
    wts_notification = db.Column(db.Boolean) #0:No 1:Yes
    mon_notification = db.Column(db.Integer) #0:No 1:9-12 2:12-18 3:18-23 4:all-day
    tue_notification = db.Column(db.Integer) #0:No 1:9-12 2:12-18 3:18-23 4:all-day
    wed_notification = db.Column(db.Integer) #0:No 1:9-12 2:12-18 3:18-23 4:all-day
    thu_notification = db.Column(db.Integer) #0:No 1:9-12 2:12-18 3:18-23 4:all-day
    fri_notification = db.Column(db.Integer) #0:No 1:9-12 2:12-18 3:18-23 4:all-day
    sat_notification = db.Column(db.Integer) #0:No 1:9-12 2:12-18 3:18-23 4:all-day
    sun_notification = db.Column(db.Integer) #0:No 1:9-12 2:12-18 3:18-23 4:all-day
    notes = db.relationship('Note')

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_match = db.Column(db.DateTime(timezone=True))
    match_duration = db.Column(db.Integer)
    match_type = db.Column(db.String(100))
    court_id = db.Column(db.Integer, db.ForeignKey('court.id'))
    num_player_total = db.Column(db.Integer)
    num_player_enrolled = db.Column(db.Integer)
    match_status = db.Column(db.Integer) #0:Cancelled 1:Announced 2:AcceptingPlayers 3:Full 4:BeingPlayed 5:Ended

class Court(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    court_name = db.Column(db.String(150))
    court_sport = db.Column(db.String(150))
    club_id = db.Column(db.Integer, db.ForeignKey('club.id'))
    matches = db.relationship('Match')

class Club(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    mobileNumber = db.Column(db.Integer, unique=True)
    password = db.Column(db.String(150))
    club_name = db.Column(db.String(150))
    club_address = db.Column(db.String(150))
    courts = db.relationship('Court')

class Category(db.Model):  
    id = db.Column(db.Integer, primary_key=True)
    category_code = db.Column(db.String(3)) 
    category_desc = db.Column(db.String(150))

class MatchPlayer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idMatch = db.Column(db.Integer, db.ForeignKey('match.id'))
    idPlayer = db.Column(db.Integer, db.ForeignKey('user.id'))


class NonStop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_NonStop = db.Column(db.DateTime(timezone=True))
    date_Accepting = db.Column(db.DateTime(timezone=True))
    nonStop_duration = db.Column(db.Integer)
    nonStop_warmUp = db.Column(db.Integer)
    nonStop_halftime = db.Column(db.Integer)
    nonStop_type = db.Column(db.String(100))
    num_player_total = db.Column(db.Integer)
    num_player_enrolled = db.Column(db.Integer)
    nonStop_status = db.Column(db.Integer) #0:Cancelled 1:Announced 2:AcceptingPlayers 3:Full 4:BeingPlayed 5:Ended    
    namePlayerA1 = db.Column(db.String(100))
    namePlayerA2 = db.Column(db.String(100))
    namePlayerB1 = db.Column(db.String(100))
    namePlayerB2 = db.Column(db.String(100))
    namePlayerC1 = db.Column(db.String(100))
    namePlayerC2 = db.Column(db.String(100))
    namePlayerD1 = db.Column(db.String(100))
    namePlayerD2 = db.Column(db.String(100))
