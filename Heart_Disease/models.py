from Heart_Disease import db,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Doctor.query.get(int(user_id))


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"Admin('{self.email}')"

class DoctorAdd(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"DoctorAdd('{self.username}', '{self.email}')"

class Doctor(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"Doctor('{self.username}', '{self.email}')"

db.create_all()