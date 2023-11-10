from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
# from flask_mail import Mail, Message

db = SQLAlchemy()
DB_NAME = "database.db"
# emailS = Mail()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Hello From Hell! :D'

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)


    # mail_settings = {
    # "MAIL_SERVER": 'smtp.gmail.com',
    # "MAIL_PORT": 465,
    # "MAIL_USE_TLS": False,
    # "MAIL_USE_SSL": True,
    # "MAIL_USERNAME": 'GMAIL_USERNAME',
    # "MAIL_PASSWORD": 'GMAIL_PASSWORD'
    # }

    # app.config.update(mail_settings)
    # emailS.init_app(app)


    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/') 

    from .models import User, Note, Court, Match, Club, MatchPlayer
    from datetime import date
    from datetime import datetime, timedelta
    from sqlalchemy.sql import func

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    @app.template_global('nextGame')
    def nextGame(courtID):
        dt = datetime.now()
        # match = Match.query.filter_by(court_id=courtID, dt < Match.date_match).order_by(Match.date_match).first()
        match = Match.query.filter(Match.court_id==courtID, Match.date_match >= dt).order_by(Match.date_match).first()
        next_match = ''
        if match:
            next_match = str(match.date_match)
        else:
            next_match = 'None'

        return next_match

    @app.template_global('hoursToday')
    def hoursToday(courtID):
        # sum all match_duration where >=todayT00:00 and date_match<=todayT23:59 and match.court_id=courtID
        # matches = Match.query.filter_by(court_id=courtID).all()
        
        dt = date.today()
        min_dt = datetime.combine(dt, datetime.min.time())
        max_dt = datetime.combine(dt, datetime.max.time())
        matches = Match.query.filter(Match.court_id==courtID, Match.date_match>=min_dt, Match.date_match<=max_dt).all()
        minutes = 0
        for match in matches:
            if match.date_match>=min_dt and match.date_match<=max_dt:
                minutes = minutes + match.match_duration
        
        hours = round(minutes/60,1)
        return hours
    
    @app.template_global('hoursTomorrow')
    def hoursTomorrow(courtID):
        
        today = date.today()
        dt = today + timedelta(days = 1)
        min_dt = datetime.combine(dt, datetime.min.time())
        max_dt = datetime.combine(dt, datetime.max.time())
        matches = Match.query.filter(Match.court_id==courtID, Match.date_match>=min_dt, Match.date_match<=max_dt).all()
        minutes = 0
        for match in matches:
            if match.date_match>=min_dt and match.date_match<=max_dt:
                minutes = minutes + match.match_duration
        
        hours = round(minutes/60,1)
        return hours
    
    @app.template_global('averageCourtOccupation')
    def averageCourtOccupation(courtID):
        
        today = date.today()
        dt = today - timedelta(days = 7)
        min_dt = datetime.combine(dt, datetime.min.time())
        max_dt = datetime.combine(today, datetime.max.time())
        matches = Match.query.filter(Match.court_id==courtID, Match.date_match>=min_dt, Match.date_match<=max_dt).all()
        minutes = 0
        for match in matches:
            if match.date_match>=min_dt and match.date_match<=max_dt:
                minutes = minutes + match.match_duration
        
        hours = round(minutes/60,1)
        averageWeekC = (hours/105)*100
        averageWeek = round(averageWeekC,2)
        #105hours is 100%
        return averageWeek
    
    @app.template_global('getClubNameFromCourt')
    def getClubNameFromCourt(courtID):   
        # court = Court.query.filter_by(id=courtID).first()
        court = Court.query.filter(Court.id==courtID).first()
        club_name = ''
        if court:
            club = Club.query.filter(Club.id==court.club_id).first()
            if club:
                club_name = str(club.club_name)
            else:
                club_name = 'No Club Found'
        else:
            club_name = 'No Club Found'
        return club_name
        # club_id = court.club_id
        # club = Club.query.filter_by(id=club_id).first()
        # return str(club.club_name)

    @app.template_global('getCourtNameFromCourtID')
    def getCourtNameFromCourtID(courtID):   
        court = Court.query.filter(Court.id==courtID).first()
        court_name = ''
        if court:
            court_name = str(court.court_name)
        else:
            court_name = 'No name'
        return court_name
    
    @app.template_global('getStatusFromStatusID')
    def getStatusFromStatusID(statusID):   
        match_status = ''
        if statusID == 0:
            match_status='Cancelled'
        elif statusID == 1:
            match_status='Announced'
        elif statusID == 2:
            match_status='Accepting Players'  
        elif statusID == 3:
            match_status='Full'
        elif statusID == 4:
            match_status='Being Played'
        elif statusID == 5:
            match_status='Ended'
        else:
            pass  
        return match_status
    
    @app.template_global('getPlayerNameFromMatchInd')
    def getPlayerNameFromMatchInd(matchID, ind):   
        current_Match = Match.query.filter_by(id=matchID).first()
        playersRegistered = User.query.join(MatchPlayer, MatchPlayer.idPlayer == User.id).filter(MatchPlayer.idMatch==current_Match.id).all()
        i = 0
        playerName = ""
        if playersRegistered:
            for rp in playersRegistered:          
                if str(i) == str(ind):
                    playerName = rp.first_name
                i = i + 1
        return playerName
    
    @app.template_global('getPlayerELOFromMatchInd')
    def getPlayerELOFromMatchInd(matchID, ind):   
        current_Match = Match.query.filter_by(id=matchID).first()
        playersRegistered = User.query.join(MatchPlayer, MatchPlayer.idPlayer == User.id).filter(MatchPlayer.idMatch==current_Match.id).all()
        i = 0
        playerELO = 0
        if playersRegistered:
            for rp in playersRegistered:          
                if str(i) == str(ind):
                    playerELO = 1000
                i = i + 1
        return playerELO
    
    @app.template_global('getPlayerELOPercFromMatchInd')
    def getPlayerELOPercFromMatchInd(matchID, ind):   
        current_Match = Match.query.filter_by(id=matchID).first()
        playersRegistered = User.query.join(MatchPlayer, MatchPlayer.idPlayer == User.id).filter(MatchPlayer.idMatch==current_Match.id).all()
        i = 0
        playerELOPerc = 0
        if playersRegistered:
            for rp in playersRegistered:          
                if str(i) == str(ind):
                    playerELOPerc = 1000
                i = i + 1

        playerELOPerc = (playerELOPerc*50)/1000 
                     
        return playerELOPerc

    return app
