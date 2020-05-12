from flask import Flask, render_template, session, request, redirect, url_for
from flask_socketio import SocketIO, send, emit, join_room, leave_room
import secrets
import json
import os
import games

app = Flask(__name__)

if os.path.exists('config.json'):
	with open('config.json') as file:
		config = json.load(file)
else:
	config = {'secret': secrets.token_urlsafe(16)}
	with open('config.json', 'w') as file:
		json.dump(config, file)

app.secret_key = config['secret']
socketio = SocketIO(app)

gamerooms = {}

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/clear-session')
def clear_session():
	session.clear()
	return redirect(url_for('index'))

@app.route('/qwirkle', methods=['GET', 'POST'])
def qwirkle():
	if request.method == 'POST':
		session['username'] = request.form['username']
		session['gameroom'] = request.form['gameroom']

	if 'gameroom' in session:
		if session['gameroom'] not in gamerooms:
			gamerooms[session['gameroom']] = games.Qwirkle(session['gameroom'])
		return render_template('qwirkle.html', game=gamerooms[session['gameroom']])

	return render_template('start_qwirkle.html')

@socketio.on('mousePosition')
def handle_message(data):
	data['username'] = session['username']
	emit('mouse', data, broadcast=True)

@socketio.on('connect')
def test_connect():
	emit('connection', {'username': f'{session["username"]}', 'type': 'connected'}, broadcast=True)

@socketio.on('disconnect')
def test_disconnect():
	emit('connection', {'username': f'{session["username"]}', 'type': 'disconnected'}, broadcast=True)

if __name__ == '__main__':
	socketio.run(app)
