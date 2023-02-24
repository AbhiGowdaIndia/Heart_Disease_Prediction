from flask import render_template, url_for, flash, redirect,request,session,Response,jsonify
from Heart_Disease import app, db, bcrypt
from Heart_Disease.forms import AdminLoginForm, AddDoctorForm, DoctorLoginForm, RegistrationForm,ChangePassword,DiseasePredict
from Heart_Disease.models import Doctor, DoctorAdd, Admin
from Heart_Disease.predict_methods import predict_disease
from flask_login import login_user, current_user, logout_user

@app.route("/")
@app.route("/home")
def home():
    if not Admin.query.all():
        pwd='Admin@HD'
        pswrd=bcrypt.generate_password_hash(pwd).decode('utf-8')
        user = Admin(email='admin@hd.com',password=pswrd)
        db.session.add(user)
        db.session.commit()
    return render_template('home.html', title='Home')


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    form = AdminLoginForm()
    if form.validate_on_submit():
        # if form.email.data == 'admin@hd.com' and form.password.data == 'Admin@HD':
        admin=Admin.query.filter_by(email=form.email.data).first()
        if admin and bcrypt.check_password_hash(admin.password, form.password.data):
            flash('hello Admin... \n You have been logged in!', 'success')
            return redirect(url_for('adminhome'))
        else:
            flash('Login Unsuccessful. Please check Email address and password', 'danger')
    return render_template('adminlogin.html', title='Login', form=form)

@app.route("/adminhome")
def adminhome():
    return render_template('adminhome.html', title='Home')

@app.route("/adminchangepassword",methods=['GET','POST'])
def adminchangepassword():
    form=ChangePassword()
    if form.validate_on_submit():
        record=Admin.query.all()[0]
        if bcrypt.check_password_hash(record.password,form.current_password.data):
            record.password=bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            db.session.commit()
            flash('Password changed successfully..!', 'success')
            return redirect(url_for('adminhome'))
        else:
            flash('Please enter correct current password', 'danger')
    return render_template('adminchangepassword.html', title='Change Password',form=form)

@app.route("/adddoctor",methods=['GET','POST'])
def adddoctor():
    form=AddDoctorForm()
    if form.validate_on_submit():
        doctor = DoctorAdd(username=form.name.data, email=form.email.data)
        db.session.add(doctor)
        db.session.commit()
        flash('Doctor added successfully..!', 'success')
        return redirect(url_for('adddoctor'))
    return render_template('adddoctor.html', title="Doctor",form=form)

@app.route("/viewdoctor")
def viewdeletedoctor():
    result=Doctor.query.all()
    return render_template('viewdoctor.html', title='Doctor',result=result)

@app.route("/deletedoctor/<int:id>")
def deletedoctor(id):
    entry=Doctor.query.get_or_404(id)
    db.session.delete(entry)
    db.session.commit()
    flash("Deleted successfully...!",'success')
    return redirect(url_for('viewdeletedoctor'))

@app.route("/adminlogout")
def adminlogout():
    return redirect(url_for('home'))


@app.route("/doctorlogin", methods=['GET', 'POST'])
def doctorlogin():
    if current_user.is_authenticated:
        return redirect(url_for('doctorhome'))
    form = DoctorLoginForm()
    if form.validate_on_submit():
        doctor_add=DoctorAdd.query.filter_by(email=form.email.data).first()
        doctor=Doctor.query.filter_by(email=form.email.data).first()
        if not doctor_add and not doctor:
            flash('You are not a Doctor, please contact admin.','info')
        elif doctor_add:
            flash('You are not registered.','info')
            return redirect(url_for('register'))
        elif doctor and bcrypt.check_password_hash(doctor.password, form.password.data):
            login_user(doctor, remember=form.remember.data)
            flash('Logged in successfully..!','success')
            return redirect(url_for('doctorhome'))
        else:
            flash('Please check your password..','danger')
            return redirect(url_for('doctorlogin'))
    return render_template('doctorlogin.html',title='Login',form=form)


@app.route("/doctorhome")
def doctorhome():
    return render_template('doctorhome.html', title='Home')

@app.route("/changepassword",methods=['GET','POST'])
def changepassword():
    form=ChangePassword()
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password,form.current_password.data):
            current_user.password=bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            db.session.commit()
            flash('Password changed successfully..!', 'success')
            return redirect(url_for('doctorhome'))
        else:
            flash('Please enter correct current password', 'danger')
    return render_template('changepassword.html', title='Change Password',form=form)

@app.route("/doctorlogout")
def doctorlogout():
    logout_user()
    session.pop('running',None)
    return redirect(url_for('home'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        doctor_add=DoctorAdd.query.filter_by(email=form.email.data,username=form.username.data).first()
        if not doctor_add:
            flash('You are not a faculty, please contact admin.','info')
            return redirect(url_for('register'))
        else:
            db.session.delete(doctor_add)
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            doctor = Doctor(username=form.username.data, email=form.email.data,password=hashed_password)
            db.session.add(doctor)
            db.session.commit()
            flash('Registration successfull..', 'success')
            return redirect(url_for('doctorlogin'))
    return render_template('register.html', title='Registration Form', form=form)

@app.route("/diseasepredict",methods=['GET','POST'])
def diseasepredict():
    form= DiseasePredict()
    if request.method=='POST':

        age=int(request.form['age'])
        sex_=request.form.get('sex')
        cp_ =request.form.get('cp')
        trestbps =int(request.form['trestbps'])
        chol =int(request.form['chol'])
        fbs_=request.form.get('fbs')
        restecg_=request.form.get('restecg')
        thalach=int(request.form['thalach'])
        exang_=request.form.get('exang')
        oldpeak = float(request.form['oldpeak'])
        slope_ = request.form.get('slope')
        ca_ = request.form.get('ca')
        thal_ = request.form.get('thal')

        prediction = predict_disease(age,sex_,cp_,trestbps,chol,fbs_,restecg_,thalach,exang_,oldpeak,slope_,ca_,thal_)
        return render_template('diseaseresult.html', recommendation=prediction, title='Disease Prediction')
    return render_template('doctorhome.html', title='Home',form=form)