import flask
from flask import jsonify, abort
import logging
import requests

from app.constants import constants
from app.utils import prepare_github_data, prepare_bitbucket_data, get_github_url

app = flask.Flask("user_profiles_api")
logger = flask.logging.create_logger(app)
logger.setLevel(logging.INFO)


@app.route("/git-profile/<team_name>", methods=["GET"])
def merge_profile(team_name):
    """
    Git profile endpoint
    merges github and bitbucket profile
    """

    github_url = get_github_url(team_name)
    github_response = requests.get(github_url, headers=constants['headers'])
    bitbucket_response = requests.get(constants['bitbucket_url'].format(team_name))
    github_data = prepare_github_data(github_response)
    data = prepare_bitbucket_data(bitbucket_response, github_data, team_name)
    
    total_repo = data['total_repo']
    total_forked_repo = data['total_forked_repo']
    data['total_original_repo'] = total_repo - total_forked_repo
    return jsonify(data)
