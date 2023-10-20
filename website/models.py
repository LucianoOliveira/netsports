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


class Club(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    mobileNumber = db.Column(db.Integer, unique=True)
    password = db.Column(db.String(150))
    club_name = db.Column(db.String(150))
    club_address = db.Column(db.String(150))
    # auth_users = db.relationship('User')
    courts = db.relationship('Court')

class Court(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    court_name = db.Column(db.String(150))
    court_sport = db.Column(db.String(150))
    club_id = db.Column(db.Integer, db.ForeignKey('club.id'))


class Category(db.Model):  
    id = db.Column(db.Integer, primary_key=True)
    category_code = db.Column(db.String(3)) 
    category_desc = db.Column(db.String(150))
