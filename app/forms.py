from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField,FileField
from wtforms.validators import InputRequired

class LoginForm(FlaskForm):
    
    firstname = StringField(u'First name', validators=[InputRequired()])
    lastname = StringField(u'Last name', validators=[InputRequired()])
    username = StringField(u'Username', validators=[InputRequired()])
    age = StringField(u'Age', validators=[InputRequired()])
    bio = TextAreaField(u'Biography', validators=[InputRequired()])
    gender=  SelectField(u'Gender', choices=[('Male', 'M'), ('Female', 'F')])
    file = FileField(u'Upload an Image file', validators=[InputRequired()])
    

