from flask_app import app, bcrypt
from flask_app.models.user import Users
from flask_app.models.photocard import Photocards
from flask import render_template, redirect, request, session, flash

#route for displaying index
@app.route('/')
def index():
    return render_template('index.html')

#route for processing registration
@app.post('/create_user')
def create():
    if not Users.validate_user(request.form):
            return redirect('/')
    
    potential_user = Users.get_one_by_email(request.form["email"])
    if potential_user != None:
        flash("Account already exists with this email. Please log in.", "register")
        return redirect ('/')
    
    hashed_password = bcrypt.generate_password_hash(request.form["password"])
    
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": hashed_password
    }
    user_id = Users.save(data)
    session["user_id"] = user_id
    return redirect('/trips')

#route for processing login
@app.post('/login')
def login():
    if not Users.validate_login(request.form):
            return redirect('/')
    potential_user = Users.get_one_by_email(request.form["email"])
    if potential_user == None:
        flash("Invalid login information.", "login")
        return redirect ('/')
    
    user = potential_user
    if not bcrypt.check_password_hash(user.password, request.form["password"]):
        flash("Invalid login information.", "login")
        return redirect ('/')

    session["user_id"] = user.id
    return redirect('/dashboard')

#route for logging out
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')