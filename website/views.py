from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, User, Court, Club, Match, MatchPlayer
from . import db
import json, os
from datetime import datetime, date, timedelta

views =  Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            # flash('Note added!', category='success')
    else:
        if current_user.is_authenticated:
            user = User.query.filter_by(email=current_user.email).first()
            user_type = user.user_type
            if user.user_type == 'User':
                dt = date.today()
                min_dt = datetime.combine(dt, datetime.min.time())
                open_matches = Match.query.filter(Match.date_match>=min_dt).order_by(Match.date_match.asc())
                return render_template("home.html", user=current_user, type=user_type, matches=open_matches)
            else:
                club = Club.query.filter_by(email=current_user.email).first()
                if club:
                    return render_template("club.html", club=club, user=current_user)
        else:
            dt = date.today()
            min_dt = datetime.combine(dt, datetime.min.time())
            open_matches = Match.query.filter(Match.date_match>=min_dt).order_by(Match.date_match.asc())
            return render_template("index.html", user=current_user, matches=open_matches)

    return render_template("home.html", user=current_user, type=user_type)

@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/club', methods=['GET', 'POST'])
@login_required
def club():
    if request.method == 'POST': 
        pass
    
    currentClub = Club.query.filter_by(email=current_user.email).first()
    return render_template("club.html", club=currentClub, user=current_user)

@views.route('/create_court', methods=['GET', 'POST'])
@login_required
def create_court():
    club = Club.query.filter_by(email=current_user.email).first()
    user_type = 'Club'
    if request.method == 'POST':
        court_name = request.form.get('court_name') 
        court_sport = request.form.get('court_sport') 
        new_court = Court(court_name=court_name, court_sport=court_sport, club_id=club.id)
        db.session.add(new_court) #add new match
        db.session.commit() 
        # Submit da foto do court com o id new_court.id
        image = request.files['court_photo']
        if image:
            # path = 'website/static/photos/courts/'+str(new_court.id)+'/'
            path = str(os.path.abspath(os.path.dirname(__file__)))+'/static/photos/courts/'+str(new_court.id)+'/'
            pathRelative = 'static\\photos\\courts\\'+str(new_court.id)+'\\'
            filePath = str(os.path.abspath(os.path.dirname(__file__)))+'/static/photos/courts/'+str(new_court.id)+'/main.jpg'
                    
            # Check if directory exists, if not, create it.
            if os.path.exists(path) == False:
                print('Dir path not found')
                os.mkdir(path)
            # Check if main.jpg exists, if exists delete it
            if os.path.exists(filePath) == True:
                os.remove(filePath)
            
            # Upload image to directory
            fileName = 'main.jpg'
            basedir = os.path.abspath(os.path.dirname(__file__))
            newPath = os.path.join(basedir, pathRelative, fileName)
            # image.save(newPath)
            image.save(filePath)

        currentClub = Club.query.filter_by(id=current_user.id).first()
        return redirect(url_for('views.club'))

    return render_template("add_court.html", user=current_user, type=user_type, club=club)

@views.route('/create_match/<courtID>', methods=['GET', 'POST'])
@login_required
def create_match(courtID):
    if request.method == 'POST':
        date_match = datetime.strptime( request.form.get('date_match'), '%Y-%m-%dT%H:%M') 
        match_duration = request.form.get('match_duration') 
        match_type = request.form.get('match_type') 
        court_id = courtID
        num_player_total = request.form.get('num_player_total') 
        num_player_enrolled = 0 
        match_status = request.form.get('match_status') 

        # check if there already is a match for the same court at the same time
        date_start = date_match
        date_end = date_start + timedelta(minutes = int(match_duration))
        matches = Match.query.filter(Match.court_id==court_id).all()
        overlap = ''
        for match in matches:
            existingMatchEndTime = match.date_match + timedelta(minutes = int(match.match_duration))
            if (date_start>=match.date_match and date_start<=existingMatchEndTime) or (date_end>=match.date_match and date_end<=existingMatchEndTime):
                overlap = 'yes'
        # otherMatch = Match.query.filter(Match.date_match>=date_start, Match.date_match<=date_end, Match.court_id==court_id).all()
        if overlap=='yes':
            flash('There is already a match occuring in that slot.', category='error')
        else:
            if courtID:
                new_match = Match(date_match=date_match, match_duration=match_duration, match_type=match_type, court_id=court_id, num_player_total=num_player_total, num_player_enrolled=num_player_enrolled, match_status=match_status)
                db.session.add(new_match) #add new match
                db.session.commit() 
                current_Court = Court.query.filter_by(id=courtID).first()
                # return render_template("court_detail.html", court=courtID, user=current_user, currentCourt=current_Court)    
            
                return redirect(url_for('views.court_detail', courtID=courtID, type='Club'))

    current_Court = Court.query.filter_by(id=courtID).first()
    current_Club = Club.query.filter(Club.id == current_Court.club_id).first()
    return render_template("create_match.html", court_ID=courtID, user=current_user, club=current_Club, type='Club')

@views.route('/delete-court', methods=['POST'])
def delete_court():  
    court = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    courtId = court['courtId']
    court = Court.query.get(courtId)
    if court:
        if court.club_id == current_user.id:
            # Check for photo if exists, delete folder
            filePath = str(os.path.abspath(os.path.dirname(__file__)))+'/static/photos/courts/'+str(court.id)+'/main.jpg'
            if os.path.exists(filePath) == True:
                os.remove(filePath)
                
            db.session.delete(court)
            db.session.commit()

    return jsonify({})


@views.route('/delete-match', methods=['POST'])
def delete_match():  
    match = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    matchId = match['matchId']
    match = Match.query.get(matchId)
    db.session.delete(match)
    db.session.commit()

    return jsonify({})



@views.route('/userInfo', methods=['GET', 'POST'])
@login_required
def userInfo():
    if request.method == 'POST': 
        current_user.first_name = request.form.get('first_name')
        current_user.postal_code = request.form.get('postal_code')
        current_user.birth_date = datetime.strptime( request.form.get('birth_date'), '%Y-%m-%d')

        if request.form.get('email_notification'):
            current_user.email_notification = True
        else:
            current_user.email_notification = False
        
        if request.form.get('sms_notification'):
            current_user.sms_notification = True
        else:
            current_user.sms_notification = False

        if request.form.get('app_notification'):
            current_user.app_notification = True
        else:
            current_user.app_notification = False
            
        if request.form.get('wts_notification'):
            current_user.wts_notification = True
        else:
            current_user.wts_notification = False

        current_user.mon_notification = request.form.get('mon_notification')
        current_user.tue_notification = request.form.get('tue_notification')
        current_user.wed_notification = request.form.get('wed_notification')  
        current_user.thu_notification = request.form.get('thu_notification')
        current_user.fri_notification = request.form.get('fri_notification')
        current_user.sat_notification = request.form.get('sat_notification')
        current_user.sun_notification = request.form.get('sun_notification')

        current_user.main_category = request.form.get('main_category')
        current_user.mix_category = request.form.get('mix_category')
        db.session.commit()

        
                 
        # User Profile Part
        # Only update if file is uploaded
        # print(request.files)
        image = request.files['profile_photo']
        if image:
            # path = 'website/static/photos/users/'+str(current_user.id)+'/'
            path = str(os.path.abspath(os.path.dirname(__file__)))+'/static/photos/users/'+str(current_user.id)+'/'
            pathRelative = 'static\\photos\\users\\'+str(current_user.id)+'\\'
            filePath = str(os.path.abspath(os.path.dirname(__file__)))+'/static/photos/users/'+str(current_user.id)+'/main.jpg'
                    
            # Check if directory exists, if not, create it.
            if os.path.exists(path) == False:
                print('Dir path not found')
                os.mkdir(path)
            # Check if main.jpg exists, if exists delete it
            if os.path.exists(filePath) == True:
                os.remove(filePath)
            
            # Upload image to directory
            fileName = 'main.jpg'
            basedir = os.path.abspath(os.path.dirname(__file__))
            newPath = os.path.join(basedir, pathRelative, fileName)
            # image.save(newPath)
            image.save(filePath)

    else:
        user = User.query.filter_by(id=current_user.id).first()
        if user and user.postal_code != '':
            #Mostrar o ecrã geral do cliente
            pass
        else:
            #Mostrar o ecrã com os dados adicionais
            pass



    return render_template("user_info.html", user=current_user, type='User')

@views.route('/display_user_image/<userID>')
def display_user_image(userID):
    filePath = str(os.path.abspath(os.path.dirname(__file__)))+'/static/photos/users/'+str(userID)+'/main.jpg'
    if os.path.isfile(filePath):
        return redirect(url_for('static', filename='photos/users/'+ str(userID)+'/main.jpg'), code=301)
    else:
        return redirect(url_for('static', filename='photos/users/nophoto.jpg'), code=301)
    
@views.route('/display_court_image/<courtID>')
def display_court_image(courtID):
    filePath = str(os.path.abspath(os.path.dirname(__file__)))+'/static/photos/courts/'+str(courtID)+'/main.jpg'
    if os.path.isfile(filePath):
        return redirect(url_for('static', filename='photos/courts/'+ str(courtID)+'/main.jpg'), code=301)
    else:
        return redirect(url_for('static', filename='photos/courts/nophoto.jpg'), code=301)    
    
@views.route('/display_club_image/<clubID>')
def display_club_image(clubID):
    filePath = str(os.path.abspath(os.path.dirname(__file__)))+'/static/photos/clubs/'+str(clubID)+'/main.jpg'
    if os.path.isfile(filePath):
        return redirect(url_for('static', filename='photos/clubs/'+ clubID+'/main.jpg'), code=301)
    else:
        return redirect(url_for('static', filename='photos/clubs/nophoto.jpg'), code=301)    


@views.route('/display_club_image_fromCourt/<courtID>')
def display_club_image_fromCourt(courtID):
    current_Court = Court.query.filter_by(id=courtID).first()
    clubID = current_Court.club_id
    filePath = str(os.path.abspath(os.path.dirname(__file__)))+'/static/photos/clubs/'+str(clubID)+'/main.jpg'
    if os.path.isfile(filePath):
        return redirect(url_for('static', filename='photos/clubs/'+str(clubID)+'/main.jpg'), code=301)
    else:
        return redirect(url_for('static', filename='photos/clubs/nophoto.jpg'), code=301) 
          
    

@views.route('/court_detail/<courtID>')
@login_required
def court_detail(courtID):
    current_Court = Court.query.filter_by(id=courtID).first()
    current_Club = Club.query.filter(Club.id == current_Court.club_id).first()
    return render_template("court_detail.html", court=courtID, user=current_user, currentCourt=current_Court, club=current_Club, type='Club')   

@views.route('/court_details/<courtID>', methods=['GET', 'POST'])
def court_details(courtID):
    print('Hello from court_details '+str(courtID))
    return 8

@views.route('/match_detail/<matchID>', methods=['GET', 'POST'])
@login_required
def match_detail(matchID):
    if request.method == 'GET':
        current_Match = Match.query.filter_by(id=matchID).first()
        current_Court = Court.query.filter(Court.id==current_Match.court_id).first()
        matchID = current_Match.id

        len = current_Match.num_player_total
        match_status = ''
        if current_Match.match_status == 0:
            match_status='Cancelled'
        elif current_Match.match_status == 1:
            match_status='Announced'
        elif current_Match.match_status == 2:
            match_status='Accepting Players'  
        elif current_Match.match_status == 3:
            match_status='Full'
        elif current_Match.match_status == 4:
            match_status='Being Played'
        elif current_Match.match_status == 5:
            match_status='Ended'
        else:
            pass  

        #all_players_list =  MatchPlayer.query.with_entities(MatchPlayer.idPlayer).filter(MatchPlayer.idMatch==current_Match.id).all()
        playersRegistered = User.query.join(MatchPlayer, MatchPlayer.idPlayer == User.id).filter(MatchPlayer.idMatch==current_Match.id).all()

    
    elif request.method == 'POST':
        current_Match = Match.query.filter_by(id=matchID).first()
        current_Court = Court.query.filter(Court.id==current_Match.court_id).first()
        matchID = current_Match.id
        len = current_Match.num_player_total
        match_status = ''
        if current_Match.match_status == 0:
            match_status='Cancelled'
        elif current_Match.match_status == 1:
            match_status='Announced'
        elif current_Match.match_status == 2:
            match_status='Accepting Players'  
        elif current_Match.match_status == 3:
            match_status='Full'
        elif current_Match.match_status == 4:
            match_status='Being Played'
        elif current_Match.match_status == 5:
            match_status='Ended'
        else:
            pass  

        
        # delete every record in MatchPlayers where matchID is that one
        # write new players for the matchid
        mps = MatchPlayer.query.filter(MatchPlayer.idMatch == matchID).all()
        if mps:
            for mp in mps:
                mp.idPlayer = 0
                db.session.commit()  
            i = 0
            for mp in mps:
                player_id = request.form.get('player_id'+str(i))  
                if  (player_id != '0' and player_id != ' ') and matchID>0:
                    mp.idPlayer = player_id
                    db.session.commit() 
                i = i + 1
        else:
            for i in range(0, len):
                player_id = request.form.get('player_id'+str(i))
                if  matchID>0:
                    new_match_player = MatchPlayer(idMatch=matchID, idPlayer=player_id)
                    db.session.add(new_match_player)
                    db.session.commit()

        playersRegistered = User.query.join(MatchPlayer, MatchPlayer.idPlayer == User.id).filter(MatchPlayer.idMatch==current_Match.id).all()


    mps = MatchPlayer.query.filter(MatchPlayer.idMatch == matchID).all() 
    match_players_list = []
    for mp in mps:
        player = User.query.filter(User.id == mp.idPlayer).first()  
        if player:
            new_item = {"name": player.first_name, "contact": player.mobileNumber, "id": player.id}  
            match_players_list.append(new_item)   
    # Get players already in game
    # get list of ids of players already in game
    # use the not_in() function inside the filter to exclude those ids from the search of players for autocomlete

    # Get players and contact for autocomplete
    all_players_obj = User.query.filter(User.ustatus=='V', User.user_type=='User').all()
    list_players = []
    for player in all_players_obj:
        list_players.append(player.first_name)

    multiarray = []
    for player in all_players_obj:
        new_player = {"name": player.first_name, "contact": player.mobileNumber, "id": player.id}
        multiarray.append(new_player)

    return render_template("match_detail.html", user=current_user, match=current_Match, currentCourt=current_Court, len=len, match_status=match_status, list_players=list_players, multiarray=multiarray, playersRegistered=playersRegistered) 


@views.route('/testing')
def testing():
    # return 'test correct'
    return redirect(url_for('static', filename='photos/courts/nophoto.jpg'), code=301)

@views.route('/paises', methods=['GET'])
def paises():
    paises = ["COLOMBIA", "MEXICO", "NICARAGUA", "BRASIL", "ARGENTINA", "PERU", "GUATEMALA"]
    return jsonify({"paises":paises})

def exampleFunctions(itemID):
        return 'tests correct' + str(itemID)


# with entities examples
# players_name_phone = User.query.with_entities(User.first_name, User.mobileNumber).filter(User.ustatus=='V', User.user_type=='User').all()
# players_name = User.query.with_entities(User.first_name).filter(User.ustatus=='V', User.user_type=='User').all()