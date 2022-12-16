import pandas as pd
import numpy as np
import os
import pickle
from flask import Flask, redirect, url_for, request, render_template
from flask_sqlalchemy import SQLAlchemy
from create_db import Joke, User
from sqlalchemy import func

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'rates.db')
app.config['SQLALCHEMY_BINDS'] = {
    'jokes': 'sqlite:///' + os.path.join(basedir, 'jokes.db'),
    'users': 'sqlite:///' + os.path.join(basedir, 'users.db')
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

new_user_id = None
new_user_rates = []


@app.route('/', methods = ['POST', 'GET'])
def index():
   if request.method == 'POST':
      if request.form['action'] == "user":
         user_id = request.form['id']
         user_vec = db.session.query(User).filter_by(id=user_id).first()
         user_vec = np.array([list(map(lambda x: float(x), user_vec.vec.split(',')))])
         jokes = db.session.query(Joke).order_by(Joke.id.asc()).all()
         jokes = np.array([list(map(lambda x: float(x), val.vec.split(','))) for val in jokes])
         candidates = []
         with open(r"C:\Users\vdtri\Documents\Учеба\Рекомендательные системы\proj\models\reg1", 'rb') as f:
            reg1 = pickle.load(f)
         with open(r"C:\Users\vdtri\Documents\Учеба\Рекомендательные системы\proj\models\reg2", 'rb') as f:
            reg2 = pickle.load(f)
         with open(r"C:\Users\vdtri\Documents\Учеба\Рекомендательные системы\proj\models\reg3", 'rb') as f:
            reg3 = pickle.load(f)
         with open(r"C:\Users\vdtri\Documents\Учеба\Рекомендательные системы\proj\models\coef", 'rb') as f:
            coef = pickle.load(f)
         print(jokes.shape)
         print(user_vec.shape)
         for ind, val in enumerate(np.concatenate((np.broadcast_to(user_vec, (jokes.shape[0], user_vec.shape[1])), jokes), axis=1)):
            candidates.append((ind, reg1.predict([val])[0] * coef[0] + reg2.predict([val])[0] * coef[1] + reg3.predict([val])[0] * coef[2]))
         joke_ind = sorted(candidates, key=lambda x: x[1], reverse=True)[0][0]
         path = r"C:\Users\vdtri\Documents\Учеба\Рекомендательные системы\proj\dataset\Dataset4JokeSet.xlsx"
         df = pd.read_excel(path, header=None)
         return render_template("ex_usr.html", joke=df.loc[joke_ind].values[0])
      elif request.form['action'] == "new_user":
         path = r"C:\Users\vdtri\Documents\Учеба\Рекомендательные системы\proj\dataset\Dataset4JokeSet.xlsx"
         df = pd.read_excel(path, header=None)
         sample = df.sample().index[0]
         new_id = db.session.query(func.max(User.id)).first()[0] + 1
         return redirect(url_for("new_user", joke_id=sample, new_id=new_id))
   return render_template('index.html')
   

@app.route('/existing_user', methods = ['POST', 'GET'])
def existing_user():
   if request.method == 'POST':
      return redirect(url_for('index'))
   return render_template('ex_usr.html')


@app.route('/new_user',methods = ['POST', 'GET'])
def new_user():
   joke_id = request.args.get("joke_id")
   new_id = request.args.get("new_id")
   if not hasattr(new_user, "new_id") and new_id:
      setattr(new_user, "new_id", new_id)
      setattr(new_user, "joke_id", joke_id)
      setattr(new_user, "rates", [])
   path = r"C:\Users\vdtri\Documents\Учеба\Рекомендательные системы\proj\dataset\Dataset4JokeSet.xlsx"
   if request.method == 'POST':
      return_value = None
      if request.form['action'] == "home":
         jokes = [0 for _ in range(158)]
         for joke_id, rate in getattr(new_user, "rates"):
            jokes[int(joke_id)] = int(rate)
         db.session.add(User(id=getattr(new_user, "new_id"), vec=','.join(list(map(lambda x: str(x), jokes)))))
         db.session.commit()
         delattr(new_user, "new_id")
         delattr(new_user, "rates")
         delattr(new_user, "joke_id")
         return_value = redirect(url_for('index'))
      else:
         df = pd.read_excel(path, header=None)
         ind = df.sample().index[0]
         new_id = getattr(new_user, "new_id")
         rate = request.form.get("radio")
         joke_id = getattr(new_user, "joke_id")
         if rate is not None:
            getattr(new_user, "rates").append((joke_id, rate))
            setattr(new_user, "joke_id", int(ind))
         return_value = redirect(url_for("new_user", joke_id=int(ind), new_id=new_id))
      return return_value
   else:
      sample = pd.read_excel(path, header=None).loc[int(joke_id)]
      return render_template("new_user.html", joke=sample.values[0], new_id=f"Your id is {new_id}")


if __name__ == '__main__':
   app.run(debug = True)