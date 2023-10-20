from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, User
from . import db
import json
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
    
    return render_template("club.html", user=current_user)



@views.route('/userInfo', methods=['GET', 'POST'])
@login_required
def userInfo():
    if request.method == 'POST': 
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

    else:
        user = User.query.filter_by(id=current_user.id).first()
        if user and user.postal_code != '':
            #Mostrar o ecrã geral do cliente
            pass
        else:
            #Mostrar o ecrã com os dados adicionais
            pass



    return render_template("user_info.html", user=current_user)
