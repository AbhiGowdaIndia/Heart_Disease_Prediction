from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,SelectField,FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from Heart_Disease.models import Doctor, DoctorAdd
from flask_login import current_user

class DoctorLoginForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()],render_kw={"placeholder": "Email address"})                    
    password = PasswordField(validators=[DataRequired()],render_kw={"placeholder": "Password"})
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
	
class AdminLoginForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()],render_kw={"placeholder": "Email address"})                    
    password = PasswordField(validators=[DataRequired()],render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')
    
    
class RegistrationForm(FlaskForm):
    username = StringField(validators=[DataRequired(), Length(min=2, max=20)],
                           render_kw={"placeholder": "Username"})
    email = StringField(validators=[DataRequired(), Email()],
                        render_kw={"placeholder": "Email address"})
    password = PasswordField(validators=[DataRequired()],
                             render_kw={"placeholder": "Password"})
    confirm_password = PasswordField(validators=[DataRequired(), EqualTo('password')],
                                     render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField('Sign Up')
    
    def validate_email(self, email):
        doctor =Doctor.query.filter_by(email=email.data).first()
        if doctor:
            raise ValidationError('This email is already registered.')
            
class AddDoctorForm(FlaskForm):
    name = StringField(validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField(validators=[DataRequired(), Email()])                    
    submit = SubmitField('Add')
    def validate_email(self, email):
        doctor1 = DoctorAdd.query.filter_by(email=email.data).first()
        doctor2 = Doctor.query.filter_by(email=email.data).first()
        if doctor1:
            raise ValidationError('This email is already added.')
        if doctor2:
            raise ValidationError('This email is already registered.')
			
class ChangePassword(FlaskForm):                    
    current_password = PasswordField(validators=[DataRequired()],render_kw={"placeholder": "Current Password"})
    new_password = PasswordField(validators=[DataRequired()],render_kw={"placeholder": "New Password"})
    submit = SubmitField('Change Password')

class DiseasePredict(FlaskForm):
    age=FloatField(validators=[DataRequired()])
    sex=SelectField(validators=[DataRequired()])
    cp =SelectField(validators=[DataRequired()])
    trestbps =FloatField(validators=[DataRequired()])
    chol =FloatField(validators=[DataRequired()])
    fbs=SelectField(validators=[DataRequired()])
    restecg=SelectField(validators=[DataRequired()])
    thalach=FloatField(validators=[DataRequired()])
    exang=SelectField(validators=[DataRequired()])
    oldpeak = FloatField(validators=[DataRequired()])
    slope = SelectField(validators=[DataRequired()])
    ca = SelectField(validators=[DataRequired()])
    thal = SelectField(validators=[DataRequired()])
    submit = SubmitField('Predict')