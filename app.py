import time
from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit, join_room, rooms

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route('/')
def root():
    return render_template('index.html')


@app.route('/r')
def res():
    return render_template('receiver.html')

# 1: built in event on conncet lisen for users connection
@socketio.on('connect')
def handleConnect():
    print("connected", request.sid)

# 2: custom back-end listener "joinTrip": to add the clint to a trip
@socketio.on('joinTrip')
def handleJoinTrip(tripId):
    print("user join trip: " + tripId)
    # add the clint to the room which is the tripId.
    join_room(tripId)
    # 3: send confirmation to the client that confirm he joined the room.
    emit("roomJointed", "you joint room: " + tripId, room=tripId)


# 4: custom back-end listener "sendLocation" to resive the location from the sender and send it to the receiver.
@socketio.on('sendLocation')
def handleLocation(data):
    print('location from user: ' + request.sid +
          "location: " + str(data['location']))
    # 5: Send the location the receiver on the same room which is the tripId.
    emit('locationToTrip', data['location'], room=data['tripId'])

# 6: back-end listener on user desconnect.
@socketio.on('disconnect')
def handleConnect():
    print("user disConnected: " + request.sid)


if __name__ == '__main__':
    socketio.run(app)
