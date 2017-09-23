import requests
from requests.exceptions import RequestException
from flask import Flask, jsonify
app = Flask(__name__)

team = ('cica', [{'name': 'Rabinovits Jakov'}, {'name': 'Bognar Marton'}, {'name': 'Tusko Gergely'}])
teams_url = 'https://chaosstack-starter.herokuapp.com/teams?hash=FMJB6A5JXTMsJuULE9fpq94mHgn2'

@app.route('/team-members')
def get_team_members():
    return jsonify(members=team[1], teamName=team[0])

@app.route('/competitors')
def get_competitors():
    urls = requests.get(teams_url)
    teams = []
    for url in urls.json():
        try:
            fullUrl = '/'.join([url['url'].strip('/'), 'team-members'])
            team_request = requests.get(fullUrl, timeout=0.1)
            if team_request.status_code == 200:
                try:
                    req_team = team_request.json()
                    teams.append({'name': req_team['teamName']})
                except ValueError:
                    pass
        except RequestException:
            pass
    return jsonify(teams=teams)

if __name__ == '__main__':
    app.run()