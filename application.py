import os

from flask import Flask, request, session
from flask import render_template as rt
from flask_session import Session
from flask_socketio import SocketIO, emit #DONT WORK WITH FLASK_DEBUG=1
import requests
from model import Room

app=Flask(__name__)

app.config['SESSION_TYPE']='filesystem'
app.config['SESSION_PERMANENT']=False
app.config['SECRET_KEY']=os.getenv('SECRET_KEY')
socketio=SocketIO(app)
Session(app)

messages={}
rooms={}
users={}

@app.route('/')
def index():
    try: 
        session['name']
    except KeyError:
        return rt('login.html')
    return rt('index.html', rooms=rooms)

@app.route('/log')
def log():
    return rt('login.html')

@app.route('/login', methods=["POST"])
def login():
    session['name']=request.form.get('username')
    return rt('index.html', rooms=rooms)

@app.route('/logout')
def logout():
    try:
        session.pop('name')
    except KeyError:
        pass
    return rt('login.html')

@app.route('/<string:name>')
def chatroom(name):
    try:
        session['name']
    except KeyError:
        return rt('login.html')
    else:
        messages=rooms[name].get_messages()
        return rt('chatroom.html',name=session['name'], messages=messages, room=name)

'''
@app.route('/<string:name>')
def chatroom(name):
    try:
        session['name']
    except KeyError:
        return rt('login.html')
    else:
        messages=rooms[name].get_messages()
        return rt('chatroom.html',name=session['name'], messages=messages, room=name)

@socketio.on("create room")
def create_room(data):
    name=data['name']
    if name in rooms:
        status="There is already a room with that name";
        emit('failure',status, broadcast=False)
    else:
        room=Room(title=name,made_by=session['name'])
        rooms[name]=room
        #print(room.title)
        room=room.__dict__
        emit('show rooms', room, broadcast=True)
        try:
            users[session['name']]
        except KeyError:
            users[session['name']]=request.sid
            print('SID: ', users[session['name']])

@socketio.on("send", namespace='/room')
def send_message(data):
    text=data['message']
    name=data['name']
    mess={'name':name, 'message':text}
    room=data['room']
    rooms[room].add_message(username=name,message=text);
    emit('show messages', mess, broadcast=True)
'''
@socketio.on('connect')
def on_connect():
    try:
        users[session['name']]
    except KeyError:
        users[session['name']]=request.sid
        print('SID: ', users[session['name']])


@socketio.on("create room")
def create_room(data):
    name = data['name']
    if name in rooms:
        status="There is already a room with that name";
        emit('failure',status, broadcast=False)
    else:
        room=Room(title=name,made_by=session['name'])
        rooms[name]=room
        room=room.__dict__
        emit('show rooms', room, broadcast=True)

@socketio.on("join", namespace='/join_room')
def join_room(data):
    room=data['room']
    print('Room: ', room)

#left to implement private messaging and rooms to work 
#!See: https://github.com/miguelgrinberg/Flask-SocketIO/blob/master/example/app_namespace.py for reference

@socketio.on("send", namespace='/room')
def send_message(data):
   # socketio.join()
    text=data['message']
    name=data['name']
    mess={'name':name, 'message':text}
    room=data['room']
    rooms[room].add_message(username=name,message=text);
    emit('show messages', mess, broadcast=True)

@socketio.on("private_msg", namespace='/private')
def send_private_msg():
    pass


