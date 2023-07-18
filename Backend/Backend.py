from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import bcrypt
from flask_cors import CORS
from flask_socketio import SocketIO, join_room, leave_room, emit
import jwt, datetime
import json


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Bebo$561@localhost/ChillChat'
app.app_context().push()
db = SQLAlchemy(app)
salt = bcrypt.gensalt(10)
socketio = SocketIO(app, cors_allowed_origins='http://localhost:3000')

class Users(db.Model):
   Userid = db.Column(db.Integer, primary_key = True)
   Username = db.Column(db.String(20), unique = True)
   Photo = db.Column(db.Text)
   Password = db.Column(db.String(100)) 

class Messages(db.Model):
    Messageid = db.Column(db.Integer, primary_key = True)
    Userfrom = db.Column(db.String(20))
    UserTo = db.Column(db.String(20))
    Contents = db.Column(db.String(250))

@app.route('/Register', methods=['POST'])
def Register():
    data = json.loads(request.data)
    print(data)
    Username = data["Username"]
    password = str(data["Password"])
    Password = bcrypt.hashpw(password.encode('utf-8'), bytes(salt))

    Displayname = data["DisplayName"]
    user = Users.query.filter_by(Username=Username).first()
    if user:
        return jsonify({'Data': 'Already Exists'}), 401

    try:
        New_user = Users(Username= Username, Displayname = Displayname, Password = Password )
        db.session.add(New_user)
        db.session.commit()
        return jsonify({'Data': 'Success'}), 200
    except Exception as e:
        print(e)
        return jsonify({'Data': 'Error'}),403
    
@app.route('/Login', methods=['POST'])
def Login():
    data = json.loads(request.data)
    username = data["Username"]
    password = str(data["Password"])
    user = Users.query.filter_by(Username=username).first()
    hashedPass = str(user.Password)
    if user:
        if bcrypt.checkpw(password.encode('utf-8'), hashedPass.encode('utf-8')):
            payload = {
                    'id': username,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
                    'iat': datetime.datetime.utcnow()
                }
            token = jwt.encode(payload, 'SECRET_KEY', algorithm='HS256')
            trueToken = jwt.decode(token, 'SECRET_KEY', algorithms=['HS256'])
            return jsonify({'Data': 'Success',
                            'Token': trueToken}), 200
        else:
            return jsonify({'Data': 'Error'}),403
    else:
        return jsonify({'Data': 'Does Not Exist'}),400

#This will be called everytime the account page is loaded, sends details about the account to the frontend.
@app.route('/AccountRetrieveDetails', methods=['GET'])
def AccountRetrieveDetails():
    return

#This will be called everytime the user updates their pfp or username.
@app.route('/AccountUpdate', methods=["PUT"])
def AccountUpdate():
    return

@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)


if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)
   socketio.run(app)