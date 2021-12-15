from AkilliOtopark import db
from AkilliOtopark.models import User

def create():
    db.create_all()
    admin = User(username='admin', password='1111')
    db.session.add(admin)
    db.session.commit()
