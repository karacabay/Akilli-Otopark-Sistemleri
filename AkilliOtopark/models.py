from AkilliOtopark import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    plakas = db.relationship('Plaka', backref='user', lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f'Kullanıcı Adı : {self.username}'

class Plaka(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    surname = db.Column(db.String)
    plaka = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, name, surname, plaka, user_id):
        self.name = name
        self.surname = surname
        self.plaka = plaka
        self.user_id = user_id

    def __repr__(self):
        return f'{self.name} {self.surname}'
