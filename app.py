from flask import Flask, jsonify
app = Flask(__name__)

team = ('cica', ['Rabinovits Jakov', 'Bognar Marton', 'Tusko Gergely'])

@app.route('/team-members')
def team_members():
	return jsonify(members=team[1], teamName=team[0])