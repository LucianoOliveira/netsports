from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, User, Court, Club
from . import db
import json, os
from datetime import datetime, date

views =  Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

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
        court_name = request.form.get('court_name')#Gets the note from the HTML 
        court_sport = 'Padel' 

        if len(court_name) < 1:
            flash('Court Name is too short!', category='error') 
        else:
            new_court = Court(court_name=court_name, court_sport=court_sport, club_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_court) #adding the Court             
            db.session.commit()
            flash('Court added!', category='success')
    
    currentClub = Club.query.filter_by(id=current_user.id).first()
    return render_template("club.html", club=currentClub, user=current_user)

@views.route('/delete-court', methods=['POST'])
def delete_court():  
    court = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    courtId = court['courtId']
    court = Court.query.get(courtId)
    if court:
        if court.club_id == current_user.id:
            db.session.delete(court)
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



    return render_template("user_info.html", user=current_user)

@views.route('/display_user_image/<userID>')
def display_user_image(userID):
    filePath = str(os.path.abspath(os.path.dirname(__file__)))+'/static/photos/users/'+str(userID)+'/main.jpg'
    if os.path.isfile(filePath):
        return redirect(url_for('static', filename='photos/users/'+ userID+'/main.jpg'), code=301)
    else:
        return redirect(url_for('static', filename='photos/users/nophoto.jpg'), code=301)
    
@views.route('/display_court_image/<courtID>')
def display_court_image(courtID):
    filePath = str(os.path.abspath(os.path.dirname(__file__)))+'/static/photos/courts/'+str(courtID)+'/main.jpg'
    if os.path.isfile(filePath):
        return redirect(url_for('static', filename='photos/courts/'+ courtID+'/main.jpg'), code=301)
    else:
        return redirect(url_for('static', filename='photos/courts/nophoto.jpg'), code=301)    
    

@views.route('/court_detail/<courtID>')
@login_required
def court_detail(courtID):
    return render_template("court_detail.html", court=courtID, user=current_user)   
