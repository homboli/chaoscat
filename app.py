#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
from requests.exceptions import RequestException
from flask import Flask, jsonify



APP = Flask(__name__)

TEAM = {
    "teamName": "cica",
    "members": [
        {
            "name": "Rabinovits Jakov",
        },
        {
            "name": "Tuskó Gergely",
        },
        {
            "name": "Bognár Márton",
        },
    ]
}

TEAMS_URL = 'https://chaosstack-starter.herokuapp.com/teams?hash=FMJB6A5JXTMsJuULE9fpq94mHgn2'

def set_encoding(response):
    """Set the response's content type and encoding"""

    response.headers["Content-Type"] = "text/json; charset=utf-8"
    return response


@APP.route('/team-members')
def get_team_members():
    """Return the list of the team members"""

    return set_encoding(jsonify(TEAM))


@APP.route('/competitors')
def get_competitors():
    """Return the names of all the teams in the competition (if their API
    responds in time)"""

    teams = [
        {
            "name": TEAM["teamName"],
        },
    ]

    try:
        urls = requests.get(TEAMS_URL)
    except RequestException:
        print("Failed to fetch teams url")
        return set_encoding(jsonify(teams=teams))

    for url in urls.json():
        full_url = '/'.join([url['url'].strip('/'), 'team-members'])

        try:
            team_request = requests.get(full_url, timeout=2)
        except RequestException:
            print("Failed to load url", full_url)
        else:
            if team_request.status_code == 200:
                try:
                    req_team = team_request.json()
                except ValueError:
                    print("Invalid format for url", full_url)
                else:
                    teams.append({'name': req_team['teamName']})
                    print("Successfully parsed", full_url)

    return set_encoding(jsonify(teams=teams))

if __name__ == '__main__':
    APP.config['JSON_AS_ASCII'] = False
    APP.run()
