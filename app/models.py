from . import db

class UserProfile(db.Model):
    userid = db.Column(db.String(10), primary_key=True)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    username = db.Column(db.String(80))
    gender = db.Column(db.String(20))
    age = db.Column(db.String(10))
    bio = db.Column(db.String(255))
    image = db.Column(db.String(255))
    day = db.Column(db.String(255))

    def __init__(self, day, userid, username, firstname, lastname, gender, age, bio, image): 
        self.day =day
        self.userid =userid
        self.username= username
        self.firstname = firstname
        self.lastname = lastname
        self.gender = gender
        self.age = age
        self.bio = bio
        self.image = image 

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.userid)
