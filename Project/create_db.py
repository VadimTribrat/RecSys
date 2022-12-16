import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from tqdm import tqdm

from sqlalchemy.sql import func


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'rates.db')
app.config['SQLALCHEMY_BINDS'] = {
    'jokes': 'sqlite:///' + os.path.join(basedir, 'jokes.db'),
    'users': 'sqlite:///' + os.path.join(basedir, 'users.db')
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Joke(db.Model):
    __tablename__ = 'jokes'
    __bind_key__ = 'jokes'
    id = db.Column(db.Integer, primary_key=True)
    vec = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f'{self.vec}'


# class Rate(db.Model):
#     __tablename__ = 'rates'
#     user_id = db.Column(db.Integer, primary_key=True)
#     joke_id = db.Column(db.Integer, primary_key=True)
#     rate = db.Column(db.Float, nullable=False)

#     def __repr__(self):
#         return f'{self.user_id} {self.joke_id} {self.rate}'


class User(db.Model):
    __tablename__ = 'users'
    __bind_key__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    vec = db.Column(db.String(1500), nullable=False)

    def __repr__(self):
        return f'{self.vec}'

# with app.app_context():
#     db.create_all()
#     df = pd.read_csv(r"C:\Users\vdtri\Documents\Учеба\Рекомендательные системы\proj\dataset\dataset.csv", index_col='index')
#     for i in df.index:
#         db.session.add(User(id=i, vec=','.join(list(map(lambda x: str(x), df.loc[i].values)))))
#     df = pd.read_csv(r"C:\Users\vdtri\Documents\Учеба\Рекомендательные системы\proj\dataset\joke_vecs.csv", index_col='index')
#     for i in df.index:
#         db.session.add(Joke(id=i, vec=df.loc[i]['vec']))
#     db.session.commit()
if __name__ == '__main__':
    app.run(debug = True)