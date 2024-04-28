import os
from flask_app import app, bcrypt
from flask_app.models.user import Users
from flask_app.models.photocard import Photocards
from flask import render_template, redirect, request, session, flash
from werkzeug.utils import secure_filename

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
    return redirect('/dashboard')

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

#route for displaying dashboard
@app.route('/dashboard')
def dashboard():
    if "user_id" not in session:
        return redirect('/')
    user=Users.get_one_by_id(session["user_id"])
    photocards = Photocards.get_all_photocards_with_users()
    return render_template('dashboard.html', user=user, all_photocards=photocards)

#route for displaying view page
@app.route('/photocards/<int:id>')
def viewphotocard(id):
    if "user_id" not in session:
        return redirect('/')
    user=Users.get_one_by_id(session["user_id"])
    photocard = Photocards.get_one_photocard_with_user(id)
    return render_template('view.html', photocard=photocard, user=user)

#route for displaing edit page
@app.route('/photocards/edit/<int:id>')
def editphotocard(id):
    user=Users.get_one_by_id(session["user_id"])
    if "user_id" not in session:
        return redirect('/')
    photocard = Photocards.get_one_photocard_with_user(id)
    return render_template('edit.html', photocard=photocard, user=user)

#route for processing edits
@app.post('/update')
def updatephotocard():
    file = request.files['photo']
    if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    if not Photocards.validate_pc(request.form):
            return redirect(f"/photocards/edit/{id}")
    Photocards.update_pc(request.form)
    id = request.form["id"]
    return redirect(f"/photocards/{id}")

#route for displaying create page
@app.route('/photocards/new')
def createpc():
    user=Users.get_one_by_id(session["user_id"])
    if "user_id" not in session:
        return redirect('/')
    return render_template("create.html", user=user)

#route for processing creates
@app.post('/process')
def newpc():
    if "photo" in request.files:
        photos.save(request.files["photo"])
    if not Photocards.validate_pc(request.form):
            return redirect('/photocards/new')
    Photocards.save_new_pc(request.form)
    return redirect('/dashboard')

#route for processing deletes
@app.route('/delete/<int:id>')
def deletepc(id):
    Photocards.delete_pc(id)
    return redirect('/dashboard')