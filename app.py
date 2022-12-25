from urllib import request
from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
import os

base_dir = os.path.dirname(os.path.realpath(__file__))

db = SQLAlchemy()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(base_dir, 'users.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer(), primary_key=True) #Primary key means no two users should have the same id even if it has been deleted before. It is set to false by default
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False) # nullable means it shoild throw an error if the field id empty
    age = db.Column(db.Integer(), nullable=False)
    gender = db.Column(db.String(25), nullable=False)

    def __repr__(self):
        return f"User {self.username}"
# @app.before_first_request
# def create_tables():
#     db.create_all()

@app.route('/', methods = ['POST', 'GET'])
def home():
    users = User.query.all()

    context = {
        'users' : users
    }

    return render_template('home.html', **context)

@app.route('/users', methods = ['POST', 'GET'])
def create_user():

    if request.method == 'POST':    

        username = request.form.get('username')
        email = request.form.get('email')                    #request.form.get means it should get the value from the form
        age = request.form.get('age')
        gender = request.form.get('gender')

        new_user = User(username=username, email=email, age=age, gender=gender)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('home'))   
        

@app.route('/update/<int:id>/', methods = ['POST', 'GET'] )
def update(id):
    update_user = User.query.get_or_404(id)

    if request.method == 'POST':

        update_user.username = request.form.get('username')
        update_user.email = request.form.get('email')
        update_user.age = request.form.get('age')
        update_user.gender = request.form.get('gender')

        db.session.commit()

        return redirect(url_for('home'))   

    context = {
        'user' : update_user
    }    
    return render_template('update.html', **context)


@app.route('/delete/<int:id>', methods = ['GET'])
def delete_user(id):
    delete_user = User.query.get_or_404(id)

    db.session.delete(delete_user)
    db.session.commit()

    return redirect(url_for('home'))



if __name__ == '__main__':
    app.run(debug=True)

