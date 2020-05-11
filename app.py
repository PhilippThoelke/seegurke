from flask import Flask, render_template, session, request, redirect, url_for
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

@app.route('/block-dropped', methods = ['POST'])
def block_dropped():
	x, y = int(request.form['x']), int(request.form['y'])
	if 'gameroom' in session and session['gameroom'] in gamerooms:
		gamerooms[session['gameroom']][x, y] = True
		return 'Successful'
	else:
		print('ERROR: gameroom not found')
		return 'Error: gameroom not found'
