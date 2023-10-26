from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Club
from werkzeug.security import generate_password_hash, check_password_hash
# from . import db, emailS
from . import db
from flask_login import login_user, login_required, logout_user, current_user
# from flask_mail import Mail, Message
# from itsdangerous import URLSafeTimedSerializer, SignatureExpired


auth =  Blueprint('auth', __name__)
# s = URLSafeTimedSerializer('Thisisasecret123!')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if user.ustatus == 'V':
                if check_password_hash(user.password, password):
                    # flash('Logged in successfully!', category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('views.home'))
                else:
                    flash('Incorrect password, try again.', category='error')
            else:
                flash('User not active yet, check your emal.', category='error')
        else:
            club = Club.query.filter_by(email=email).first()
            if club:
                if check_password_hash(club.password, password):
                    # flash('Logged in successfully!', category='success')
                    login_user(club, remember=True)
                    return redirect(url_for('views.club'))
                else:
                    flash('Incorrect password, try again.', category='error')
            else:
                flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        mobileNumber = request.form.get('mobileNumber')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(first_name) < 2:
            flash('Name must be greater than 1 character.', category='error')
        elif len(mobileNumber) < 2:
            flash('Mobile number must be greater than 9 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be greater than 6 characters.', category='error')
        else:
            # token = s.dumps(email, salt='email-confirm')
            # link = url_for('auth.confirm_email', token=token, _external=True)
            #new_user = User(email=email, first_name=first_name, mobileNumber=mobileNumber, password=generate_password_hash(password1, method='sha256'), ustatus='A')
            new_user = User(email=email, first_name=first_name, mobileNumber=mobileNumber, password=generate_password_hash(password1, method='sha256'), ustatus='V')
            db.session.add(new_user)
            db.session.commit()
            # Send confirmation email
            # msg = Message('Confirm Email', sender='luciano8.oliveira@gmail.com', recipients=[email])
            # msg.body = 'Welcome to NetSports. To activate your account go to this link {}'.format(link)
            # emailS.send(msg)
            # flash('User created successfully, check Email for verification!', category='success')
            
            login_user(new_user, remember=True)
            # flash('User created successfully!', category='success')
            return redirect(url_for('views.home'))


    return render_template("sign_up.html", user=current_user)

@auth.route('/sign-up-club', methods=['GET', 'POST'])
def sign_up_club():
    if request.method == 'POST':
        email = request.form.get('email')
        club_name = request.form.get('club_name')
        mobileNumber = request.form.get('mobileNumber')
        club_address = request.form.get('club_address')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        club = Club.query.filter_by(email=email).first()
        if club:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(club_name) < 2:
            flash('Name must be greater than 1 character.', category='error')
        elif len(mobileNumber) < 2:
            flash('Mobile number must be greater than 9 characters.', category='error')
        elif len(club_address) < 2:
            flash('Club address must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be greater than 6 characters.', category='error')
        else:
            new_club = Club(email=email, club_name=club_name, mobileNumber=mobileNumber, club_address=club_address, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_club)
            db.session.commit()
            login_user(new_club, remember=True)
            # flash('Club signed up successfully', category='success')
            return redirect(url_for('views.club'))


    return render_template("sign_up_club.html", user=current_user)


# @auth.route('/confirm_email/<token>')
# def confirm_email(token):
#     try:
#         email = s.loads(token, salt='email-confirm', max_age=3600)
#         user = User.query.filter_by(email=email).first()
#         if user:
#             user.ustatus = 'V'
#             db.session.commit()
#             login_user(user, remember=True)
#             return redirect(url_for('views.home'))
#     except SignatureExpired:
#         return '<h1>The token is expired!</h1>'
#     return '<h1>The token worked!</h1>'
        
        
