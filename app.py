from flask import Flask, render_template, session, request, redirect, url_for
import games

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MRmxbZxgpUWwWp6bH6jKpA'

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
	print(request.form)
	return 'Got something I guess'
