# -*- coding: utf-8 -*-
from app import app, db
from app.models import User, Post

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}

if User.query.all() == []:
    chau = User(username="TLC", email="longchau21@gmail.com")
    chau.set_password('leso')
    db.session.add(chau)
    db.session.commit()

    trang = User(username="TTKT", email="testemail@gmail.com")
    trang.set_password('leso')
    db.session.add(trang)
    db.session.commit()

elif User.query.filter_by(username='TLC').first() is None:
    chau = User(username="TLC", email="longchau21@gmail.com")
    chau.set_password('leso')
    db.session.add(chau)
    db.session.commit()

elif User.query.filter_by(username='TTKT').first() is None:
    trang = User(username="TTKT", email="testemail@gmail.com")
    trang.set_password('leso')
    db.session.add(trang)
    db.session.commit()