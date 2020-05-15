from flask import Flask, render_template, session, request, redirect, url_for
from flask_socketio import SocketIO, send, emit, join_room, leave_room
import secrets
import json
import os
import games
import subprocess
import glob

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

@app.route('/list')
def pip_list():
	with open('out.txt','w+') as fout:
	    with open('err.txt','w+') as ferr:
	        out = subprocess.call(['pip', 'list'], stdout=fout, stderr=ferr)
	        fout.seek(0)
	        output = fout.read()
	        ferr.seek(0)
	        errors = ferr.read()
	return '<h1>Output:</h1><br>' + output.replace('\n', '<br>') + '<br><h1>Errors:</h1><br>' + errors.replace('\n', '<br>')

@app.route('/try')
def try_():
	try:
		from flask_socketio import SocketIO, send, emit, join_room, leave_room
	except Exception as e:
		return str(e)
	return 'It worked'

@app.route('/ls')
def ls():
	output = ''
	for path in glob.glob('*.log'):
		output += '<h1>' + path + '</h1><br>'
		output += open(path).read().replace('\n', '<br>')
	return output

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
