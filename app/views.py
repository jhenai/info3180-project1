"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, session, abort, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from forms import LoginForm
from models import UserProfile
import time, json 
import os


###
# Routing for your application.
###



@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')

@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')
    
@app.route('/view_profiles/',  methods=["GET"])
def view_profiles():
    return render_template('view_profiles.html', users= UserProfile.query.all())

@app.route('/profile/', methods=["GET"])
def profile():
    return render_template('profile.html', pic =str(request.args.get('pic')), date=request.args.get('date'), username=request.args.get('username'), userid=request.args.get('userid'), firstname=request.args.get('firstname'), lastname=request.args.get('lastname'), age=request.args.get('age'), bio=request.args.get('bio'), gender=request.args.get('gender'))

@app.route('/profile/<userid>')
def show_user(userid):
    user = UserProfile.query.filter_by(userid=userid).first_or_404()
    return render_template('show_user.html', user=user)

@app.route('/profiles/', methods=["GET", "POST"])
def profile_post():
    b= UserProfile.query.all()
    users=[]
    for user in b:
        #users= {'userid': user.userid}
        users.append({'userid': user.userid, 'username': user.username})
    return jsonify (users= users ) 
    
    

@app.route('/profiles/<userid>', methods=["GET", "POST"])
def post_user(userid):
    if request.headers['Content-Type'] == 'application/json':
        user = UserProfile.query.filter_by(userid=userid).first_or_404()
    return jsonify(userid=user.userid, username=user.username,image=user.image, gender=user.gender, age=user.age, profile_created_on=user.day)




@app.route("/login", methods=["GET", "POST"])
def login():
    
    
    if current_user.is_authenticated:
        # if user is already logged in, just redirec them to our secure page
        # or some other page like a dashboard
        return redirect(url_for('secure_page'))
    
    file_folder= app.config['UPLOAD_FOLDER']
    form = LoginForm()
    
    if request.method == "POST" and form.validate_on_submit():
        
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(file_folder, filename))
        
        firstname = form.firstname.data
        lastname = form.lastname.data
        age = form.age.data
        bio = form.bio.data
        gender = form.gender.data
        username = form.username.data
        
        
        #user = UserProfile.query.filter_by(firstname=firstname, lastname=lastname, age=age, bio=bio, gender=gender, image=image).first()
        
        userid= userIDgenerator()
        date=  time.strftime(" %d %B %Y") 
        
        
        
        user = UserProfile(date, userid, username, firstname, lastname, gender, age, bio, filename)
        pic= filename
        
        if user is not None:
            
            db.session.add(user) 
            db.session.commit()
            
            # flash('Logged in successfully.', 'success')
           
            next = request.args.get('next')
            
            return redirect(url_for('profile', pic=pic, date= date, userid=userid, username= username, firstname=firstname, lastname=lastname, age=age, bio=bio, gender=gender))
        
    return render_template("login.html", form=form)
    




@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)

@app.route("/logout")
@login_required
def logout():
    # Logout the user and end the session
    logout_user()
    flash('You have been logged out.', 'danger')
    return redirect(url_for('home'))

@app.route("/jquery-getjson")
def get_data():
 return render_template('jquery-getjson.html')

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
    


usercounter = 3005
def userIDgenerator():
    global usercounter 
    usercounter += 1 
    return "USER00" + str(usercounter)
    

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
