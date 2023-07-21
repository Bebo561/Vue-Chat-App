from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import bcrypt
from flask_cors import CORS
from flask_socketio import SocketIO, join_room, leave_room, emit
import jwt, datetime
import json, base64


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
   Photo = db.Column(db.LargeBinary(length=(2**32) - 1))
   Password = db.Column(db.String(100)) 
   
class MessagesWith(db.Model):
    Userid = db.Column(db.Integer, primary_key = True)
    MessagedUser = db.Column(db.String(20), unique = True)
    MessagedUserId = db.column(db.Integer)

class Messages(db.Model):
    Messageid = db.Column(db.Integer, primary_key = True)
    Userfrom = db.Column(db.String(20))
    UserTo = db.Column(db.String(20))
    Contents = db.Column(db.LargeBinary(length=(2**32) - 1))
    #Text, PNG, or JPG
    MessageType = db.column(db.String(20))

@app.route('/Register', methods=['POST'])
def Register():
    data = json.loads(request.data)
    print(data)
    Username = data["Username"]
    password = str(data["Password"])
    Password = bcrypt.hashpw(password.encode('utf-8'), bytes(salt))

    user = Users.query.filter_by(Username=Username).first()
    if user:
        return jsonify({'Data': 'Already Exists'}), 401
    try:
        New_user = Users(Username= Username, Password = Password)
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
                            'Token': token}), 200
        else:
            return jsonify({'Data': 'Error'}),403
    else:
        return jsonify({'Data': 'Does Not Exist'}),400

#This will be called everytime the account page is loaded, sends details about the account to the frontend.
@app.route('/AccountRetrieveDetails', methods=['GET'])
def AccountRetrieveDetails():
    username = request.args.get('username')
    user = Users.query.filter_by(Username = username).first()
    base64_string = None
    if user:
        if user.Photo is not None:
            base64_string = base64.b64encode(user.Photo).decode('utf-8')
        data = {
            'Username': user.Username,
            'Photo': base64_string
        }
        return jsonify({'Data': data}), 200
    else:
        return jsonify({"Data": "Server Error"}), 400
    

#This will be called everytime the user updates their pfp or username.
@app.route('/AccountUpdate', methods=["PUT"])
def AccountUpdate():
    Json = request.json
    data =json.loads(request.data)
    Token = data["Token"]
    OldUsername = data["Username"]
    NewUsername = data["NewUser"]
    NewPhoto = data["Photo"]
    print(Json["Token"])
    print(NewUsername)
    print(NewUsername.isspace())
    try:
            jwt.decode(Token, 'SECRET_KEY', algorithms=['HS256'])
            NewUser = Users.query.filter_by(Username=NewUsername).first()
            if NewUser:
                return jsonify({"Data": "Username Already Taken"}), 402
            else:
                user = Users.query.filter_by(Username=OldUsername).first()
                if NewUsername is not None and NewPhoto is not None:
                    if NewUsername.isspace() == True:
                        print("Hi")
                        return jsonify({"Data": "Please Enter a valid Username"}), 402
                    binaryData = base64.b64decode(NewPhoto)
                    user.Photo = binaryData
                    user.Username = NewUsername
                    db.session.commit()
                    ReturnData = {
                    "Username": user.Username,
                    "Photo": NewPhoto
                    }
                    return jsonify({"Data": ReturnData}), 200
                    
                elif NewPhoto is not None:
                    binaryData = base64.b64decode(NewPhoto)
                    user.Photo = binaryData
                    db.session.commit()
                    ReturnData = {
                    "Username": user.Username,
                    "Photo": NewPhoto
                    }
                    return jsonify({"Data": ReturnData}), 200

                elif NewUsername.isspace() == False:
                    user.Username = NewUsername
                    db.session.commit()
                    ReturnData = {
                    "Username": user.Username,
                    "Photo": NewPhoto
                    }
                    return jsonify({"Data": ReturnData}), 200
                
                elif NewUsername.isspace() == True:
                    print("Hi")
                    return jsonify({"Data": "Please Enter a valid Username"}), 402

    except jwt.ExpiredSignatureError:
            return jsonify({"Data": "Token Expired"}), 401
    except jwt.InvalidTokenError:
            return jsonify({"Data": "Invalid Token"}), 403

@app.route('/AccountSearch', methods=['GET'])
def AccountSearch():  
    Username = request.args.get('Username')
    User = Users.query.filter(Users.Username.contains(Username)).all()
    UserNameList = []
    UserPhotos = []
    
    for i in range(len(User)):
        UserNameList.append(User[i].Username)
        if User[i].Photo is not None:
            base64_string = base64.b64encode(User[i].Photo).decode('utf-8')
            UserPhotos.append(base64_string)
        else:
            UserPhotos.append(None)
    Data = {
        "UserList": UserNameList,
        "UserPhotos": UserPhotos
    }

    return jsonify({"Data": Data}), 200

@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)


if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)
   socketio.run(app)