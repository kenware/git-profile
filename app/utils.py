
import os
import requests
from app.constants import constants, message
from flask import Response, abort

def get_next_page_link(links, index=1):
    """
    Get the next page url of github from the response header
    returns none if the response do not contain next page
    """

    link_list = links.split(',')
    for link in link_list:
        if 'rel="next"' in link:
            next_link= link.split('>;')[0][index:]
            return next_link
    return None

def append_github_data(data, profile_data):
    """
    Extract the needed data from github
    make an additional api call to fetch needed data eg repo languages
    """

    profile_data['total_repo'] += len(data)
    validate_github_data(data)
    followers = requests.get(data[0]['owner'].get('followers_url'))
    profile_data['total_team_followers'] += len(followers.json())
    for item in data:
        profile_data['total_watchers_across_all_repo'] += item['watchers_count']
        profile_data['topic_list'] += item['topics']
        if item['fork']:
            profile_data['total_forked_repo'] += 1
        languages = requests.get(item.get('languages_url'))
        languages = languages.json().keys()
        for language in languages:
            if language not in profile_data['list_of_languages_across_all_repo']:
                profile_data['list_of_languages_across_all_repo'].append(language)

    return profile_data
    
def append_bitbucket_data(data, profile_data, team_name):
    """
    Extract the needed data from bitbucket
    make an additional api call to fetch needed data eg followers
    """

    data = data.get('values')
    profile_data['total_repo'] += len(data)
    followers = requests.get(constants['bitbucket_followers'].format(team_name))
    profile_data['total_team_followers'] += followers.json().get('size')
    
    for item in data:
        watcher_url = item['links']['watchers'].get('href')
        watcher = requests.get(watcher_url)
        profile_data['total_watchers_across_all_repo'] = watcher.json().get('size')
        if item.get('language') not in profile_data['list_of_languages_across_all_repo']:
            profile_data['list_of_languages_across_all_repo'].append(item.get('language'))
    return profile_data

def prepare_github_data(data):
    """
    Prepare github data by extracting information needed
    if the data contains next page for this team/organisation continue to fetch the next
    page until the last page
    """

    profile_data = constants['profile']
    next_page = False
    link = None
    profile_data = append_github_data(data.json(), profile_data)
    if  data.headers.get('Link'):
        next_page = True
        link = get_next_page_link(data.headers.get('Link'))
    while next_page:
        next_data = requests.get(link, headers=constants['headers'])
        profile_data = append_github_data(next_data.json(), profile_data)
        if next_data.headers.get('Link'):
            link = get_next_page_link(next_data.headers.get('Link'),2)
            if not link:
                next_page = False
        else:
            next_page = False
    return profile_data

def prepare_bitbucket_data(data, profile_data, team_name):
    """
    Prepare bitbucket data by extracting information needed
    if the data contains next page for this team/organisation continue to fetch the next
    page until the last page
    """

    next_page = False
    link = None
    profile_data = append_bitbucket_data(data.json(), profile_data, team_name)

    if  data.json().get('next'):
        next_page = True
        link = data.json().get('next')
    while next_page:
        next_data = requests.get(link)
        profile_data = append_bitbucket_data(next_data.json(), profile_data, team_name)
        if  next_data.json().get('next'):
            link = next_data.json().get('next')
        else:
            next_page = False
    return profile_data

def get_github_url(team_name):
    """
    Get github url from env
    """

    client_id = os.environ.get('GITHUB_CLIENT_ID')
    client_secrete = os.environ.get('GITHUB_CLIENT_SECRETE')
    
    if (not client_id) or (not client_secrete):
        abort(Response(constants['message']))
    return constants['github_url'].format(team_name, client_id, client_secrete)

def validate_github_data(data):
    """
    Validate github API rate limit
    """

    if isinstance(data, dict):
        abort(Response(data.get('message')))
