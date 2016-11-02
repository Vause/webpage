#!/usr/bin/env python
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for, Markup
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
import os

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    #while True:
    #    socketio.sleep(10)
     #   count += 1
      #  socketio.emit('my_response',
       #               {'data': 'Server generated event', 'count': count},
        #              namespace='/test')


@app.route('/')
def index():
    if not session.get('logged_in'):
	    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_student_login():
	if request.form['password'] == 'password' and request.form['username'] == 'Jane.Doe':
		return render_template('student.html', async_mode=socketio.async_mode)
		session['logged_in'] = True
		
	elif request.form['password'] == 'Adminpass1234' and request.form['username'] == 'ruben.arutyunov':
		return render_template('teacher.html', async_mode=socketio.async_mode)
		session['logged_in'] = True
		
	else:
		flash(Markup('Successfully registered, please click <a href="/me" class="alert-link">here</a>'))
	return index()
		
@app.route('/student')
def student_page():
	if not session.get('logged_in'):
		return index()
	else:
		return render_template('student.html', async_mode=socketio.async_mode)

@app.route('/teacher')
def teacher_page():
	if not session.get('logged_in'):
		return index()
	else:
		return render_template('teacher.html', async_mode=socketio.async_mode)



@socketio.on('my_event', namespace='/test')
def test_message(message):
    session['logged_in'] = session.get('logged_in', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['logged_in']})


@socketio.on('my_broadcast_event', namespace='/test')
def test_broadcast_message(message):
    session['logged_in'] = session.get('logged_in', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['logged_in']},
         broadcast=True)


@socketio.on('join', namespace='/test')
def join(message):
    join_room(message['room'])
    session['logged_in'] = session.get('logged_in', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['logged_in']})


@socketio.on('leave', namespace='/test')
def leave(message):
    leave_room(message['room'])
    session['logged_in'] = session.get('logged_in', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['logged_in']})


@socketio.on('close_room', namespace='/test')
def close(message):
    session['logged_in'] = session.get('logged_in', 0) + 1
    emit('my_response', {'data': 'Room ' + message['room'] + ' is closing.',
                         'count': session['logged_in']},
         room=message['room'])
    close_room(message['room'])


@socketio.on('my_room_event', namespace='/test')
def send_room_message(message):
    session['logged_in'] = session.get('logged_in', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['logged_in']},
         room=message['room'])


@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
    session['logged_in'] = session.get('logged_in', 0) + 1
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['logged_in']})
    disconnect()


@socketio.on('my_ping', namespace='/test')
def ping_pong():
    emit('my_pong')

@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    if thread is None:
        thread = socketio.start_background_task(target=background_thread)
    emit('my_response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)
	
@app.route("/logout")
def logout():
    session['logged_in'] = False
    return index()


if __name__ == '__main__':
    socketio.run(app, debug=True)
