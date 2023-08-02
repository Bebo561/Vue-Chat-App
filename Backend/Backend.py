from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import bcrypt
from flask_cors import CORS
from flask_socketio import SocketIO, join_room,  emit
import jwt, datetime
import json, base64


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Bebo$561@localhost/ChillChat'
app.app_context().push()
db = SQLAlchemy(app)
salt = bcrypt.gensalt(10)
socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins='http://localhost:3000')

#Holds all user information
class Users(db.Model):
   Userid = db.Column(db.Integer, primary_key = True)
   Username = db.Column(db.String(20), unique = True)
   Photo = db.Column(db.LargeBinary(length=(2**32) - 1))
   Password = db.Column(db.String(100)) 

#Holds private chat room information and ids 
class Chats(db.Model):
    UserOne = db.Column(db.String(20))
    UserTwo = db.Column(db.String(20))
    Chatid = db.Column(db.Integer, primary_key = True)

#Holds information about individual messages
class Messages(db.Model):
    Chatid = db.Column(db.Integer)
    Messageid = db.Column(db.Integer, primary_key = True)
    Creator = db.Column(db.String(20))

    #Used if message is just text
    textContent = db.Column(db.String(275))

    #Used if message is an image
    imageContent = db.Column(db.LargeBinary(length=(2**32) - 1))

    #Text, PNG, or JPG
    MessageType = db.Column(db.String(20))

#User registration endpoint
@app.route('/Register', methods=['POST'])
def Register():
    data = json.loads(request.data)
    print(data)
    Username = data["Username"]
    password = str(data["Password"])
    Password = bcrypt.hashpw(password.encode('utf-8'), bytes(salt))

    #Make sure username is unique and already exists, if not than return error
    user = Users.query.filter_by(Username=Username).first()
    if user:
        return jsonify({'Data': 'Already Exists'}), 401
    try:
        #Add user to database, return success.
        New_user = Users(Username= Username, Password = Password)
        db.session.add(New_user)
        db.session.commit()
        return jsonify({'Data': 'Success'}), 200
    #Issue with database commit, send server error.
    except Exception as e:
        print(e)
        return jsonify({'Data': 'Server Error'}),403
    
@app.route('/Login', methods=['POST'])
def Login():
    #Retrieve username of user trying to sign in, verify that username is valid, and compare passwords 
    data = json.loads(request.data)
    username = data["Username"]
    password = str(data["Password"])
    user = Users.query.filter_by(Username=username).first()
    hashedPass = str(user.Password)
    if user:
        #If the user exists, and the password is valid, create a jwt authentication token to send to the frontend for security.
        if bcrypt.checkpw(password.encode('utf-8'), hashedPass.encode('utf-8')):
            payload = {
                    'id': username,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
                    'iat': datetime.datetime.utcnow()
                }
            ID = user.Userid
            
            token = jwt.encode(payload, 'SECRET_KEY', algorithm='HS256')
            trueToken = jwt.decode(token, 'SECRET_KEY', algorithms=['HS256'])
            return jsonify({'Data': 'Success',
                            'Token': token, 'ID': ID}), 200
        else:
            return jsonify({'Data': 'Error'}),403
    else:
        return jsonify({'Data': 'Does Not Exist'}),400

#This will be called everytime the account page is loaded, sends details about the account to the frontend.
@app.route('/AccountRetrieveDetails', methods=['GET'])
def AccountRetrieveDetails():
    #When the account page is loaded, retrieve the user trying to access their data
    username = request.args.get('username')
    user = Users.query.filter_by(Username = username).first()
    base64_string = None
    #If the user is valid, and they have set a profile picture, translate that profile picture from binary to base64,
    # and send their ID, username, and profile picture to the frontend.
    if user:
        if user.Photo is not None:
            base64_string = base64.b64encode(user.Photo).decode('utf-8')
        data = {
            'Username': user.Username,
            'Photo': base64_string, 
            "ID": user.Userid
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
    try:    
            #Test to see if the JWT is valid, if not return errors based on why it was invalid.
            jwt.decode(Token, 'SECRET_KEY', algorithms=['HS256'])
            #If valid, check if the username the user is trying to change to already exists, if it does return an error.
            NewUser = Users.query.filter_by(Username=NewUsername).first()
            if NewUser:
                return jsonify({"Data": "Username Already Taken"}), 402
            else:
                #If the username is not taken, and the user is trying to update both their username and pfp, update both in 
                # database and send new data to the frontend.
                user = Users.query.filter_by(Username=OldUsername).first()
                if NewUsername is not None and NewPhoto is not None:
                    if NewUsername.isspace() == True:
                        return jsonify({"Data": "Please Enter a valid Username"}), 402
                    #Turn base64 image into binary format for storage.
                    binaryData = base64.b64decode(NewPhoto)
                    user.Photo = binaryData
                    user.Username = NewUsername
                    db.session.commit()
                    ReturnData = {
                    "Username": user.Username,
                    "Photo": NewPhoto
                    }
                    return jsonify({"Data": ReturnData}), 200
                
                #If the user is only updating their photo
                elif NewPhoto is not None:
                    binaryData = base64.b64decode(NewPhoto)
                    user.Photo = binaryData
                    db.session.commit()
                    ReturnData = {
                    "Username": user.Username,
                    "Photo": NewPhoto
                    }
                    return jsonify({"Data": ReturnData}), 200
                
                #If the user is updating their username into something valid.
                elif NewUsername.isspace() == False:
                    user.Username = NewUsername
                    db.session.commit()
                    ReturnData = {
                    "Username": user.Username,
                    "Photo": NewPhoto
                    }
                    return jsonify({"Data": ReturnData}), 200
                
                #If the user has sent an invalid username
                elif NewUsername.isspace() == True:
                    print("Hi")
                    return jsonify({"Data": "Please Enter a valid Username"}), 402
    except jwt.ExpiredSignatureError:
            return jsonify({"Data": "Token Expired"}), 401
    except jwt.InvalidTokenError:
            return jsonify({"Data": "Invalid Token"}), 403

#Function used for account searches 
@app.route('/AccountSearch', methods=['GET'])
def AccountSearch():  
    #Retrieve paramters of username being searched, and the username of the user making the search
    Username = request.args.get('Username')
    Request = request.args.get("Requester")
    print(Request)

    #Return all users similar to the User being searched, but is not the user searching.
    #Users cannot search for themselves.
    User = Users.query.filter(Users.Username.contains(Username), ~Users.Username.like(Request)).all()

    #Lists that hold User Information 
    UserNameList = []
    UserPhotos = []
    
    #Goes through each user found, returns their Usernames and profile pics to display in frontend.
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

#Function that is used to retrieve all messages in a chat history, and send them to frontend.
@app.route('/RetrieveMessageHistory', methods=["GET"])
def RetrieveMessageHistory():
    RoomID = request.args.get("RoomID")
    print(RoomID)
    messages = Messages.query.filter_by(Chatid=RoomID).order_by(Messages.Messageid).all()

    MessageList = []
    if messages is not None:
        for m in messages: 
            base64String = None
            if m.MessageType == "Image":
                base64String = base64.b64encode(m.imageContent).decode('utf-8')   
            data = {
                'Chatid': m.Chatid,
                "MessageId": m.Messageid,
                "Creator": m.Creator,
                "textContent": m.textContent,
                "MessageType": m.MessageType,
                "imageContent": base64String
            }
            MessageList.append(data)

        
        return jsonify({"Data": MessageList}), 200
    else:
        return jsonify({"Data": "No message history"}), 200

#Retrieves user contacts for contact page
@app.route('/RetrieveChats', methods=['GET'])
def RetrieveChats():
    User = request.args.get("User")
    chat = Chats.query.filter(db.or_(Chats.UserOne == User, Chats.UserTwo == User)).all()
    print(chat)
    if chat is None:
        return jsonify({'Data': 'No Chats'}), 200
    ChatList = []
    for c in chat:
        if c.UserOne != User:
            MessageWith = Users.query.filter_by(Username = c.UserOne).first()
            base64_string = None
            if MessageWith:
                if MessageWith.Photo is not None:
                    base64_string = base64.b64encode(MessageWith.Photo).decode('utf-8')
                data = {
                    'Username': MessageWith.Username,
                    'Photo': base64_string, 
                    "ID": MessageWith.Userid
                }
                ChatList.append(data)
        else:
            MessageWith = Users.query.filter_by(Username = c.UserTwo).first()
            base64_string = None
            if MessageWith:
                if MessageWith.Photo is not None:
                    base64_string = base64.b64encode(MessageWith.Photo).decode('utf-8')
                data = {
                    'Username': MessageWith.Username,
                    'Photo': base64_string, 
                    "ID": MessageWith.Userid
                }
                ChatList.append(data)
    return jsonify({"Data": ChatList}), 200

            



#Deletes a message by MessageID
@app.route('/DeleteMessage', methods=["DELETE"])
def DeleteMessage():
    MessageID = request.args.get("MessageID")
    message = Messages.query.filter_by(Messageid = MessageID).first()
    if message is None:
        return jsonify({"Error": "Message not found"}), 404

    db.session.delete(message)
    db.session.commit()
    return jsonify({'Data': 'Message deleted successfully'}), 200


#Function that checks if a room ID already exists for a given chat, and sends it to the frontend.
@app.route('/RetreiveChatID', methods=["GET"])
def RetrieveChatID():
    UserOne = request.args.get('UserOne')
    UserTwo = request.args.get("UserTwo")

    print(UserOne)
    print(UserTwo)
    #Or query that checks if messages between two users already exists.

    query = db.or_(
    db.and_(Chats.UserOne == UserOne, Chats.UserTwo == UserTwo),
    db.and_(Chats.UserTwo == UserTwo, Chats.UserTwo == UserOne)
    )  

    #Check if a chat between two users already exists, and return it.
    chat = Chats.query.filter(query).first()
    

    #If it exists, return the roomID to the frontend, else return the information that there is no existing chats yet.
    if chat is not None:
        Data = {
            "RoomId": chat.Chatid
        }
        return jsonify({"Data": Data}), 200
    else:
        print("Bye")
        return jsonify({"Data": "No RoomId"}), 200

@socketio.on("connect")
def handle_connect():
    print("Client connected.")

@socketio.on('join_room')
def on_join(data):
    room = data['room']
    join_room(room)
    print(f"User joined room: {room}")

@socketio.on("media_message")
def handle_media_message(data):
    Image = data["imageContent"]
    Creator = data["Creator"]
    Type = data["MessageType"]
    RoomID = data["RoomID"]
    recipient = data["Recipient"]

    Chat = Chats.query.filter_by(Chatid=RoomID).first()
    if Chat is None:
        NewChat = Chats(UserOne = Creator, UserTwo = recipient, Chatid=int(RoomID))
        db.session.add(NewChat)
        db.session.commit()

    binaryData = base64.b64decode(Image)
    #Saves each message into the sql database.
    NewMessage = Messages(Creator=Creator, Chatid=RoomID, imageContent=binaryData, MessageType=Type)
    db.session.add(NewMessage)
    db.session.commit()

    #Retrieve unique message id.
    message_id = NewMessage.Messageid

    #Send message to the Room received from
    emit("private_message", {"Creator": Creator, "imageContent": Image, "MessageType": Type, "MessageId": message_id}, room=RoomID)


@socketio.on('private_message')
def handle_private_message(data):
    recipient = data["Recipient"]
    message = data["MessageContent"]
    sender = data["Sender"]
    type = data["MessageType"]
    RoomID = data["RoomID"]

    print(sender)

    #Adds every room into a chat table, where the chatID, and participates of the room are stored. This information is later
    # used in order to retrieve open chats in the frontend. 
    Chat = Chats.query.filter_by(Chatid=RoomID).first()
    if Chat is None:
        NewChat = Chats(UserOne = sender, UserTwo = recipient, Chatid=int(RoomID))
        db.session.add(NewChat)
        db.session.commit()
    #Saves each message into the sql database.
    NewMessage = Messages(Creator=sender, Chatid=RoomID, textContent=message, MessageType=type)
    db.session.add(NewMessage)
    db.session.commit()

    #Retrieve unique message id.
    message_id = NewMessage.Messageid

    #Send message to the Room received from
    emit("private_message", {"Creator": sender, "textContent": message, "MessageType": type, "MessageId": message_id}, room=RoomID)

if __name__ == '__main__':
   db.create_all()
   #app.run(debug = True)
   socketio.run(app)