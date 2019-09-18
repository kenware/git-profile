

constants = {
    'headers' :{
        'Accept': 'application/vnd.github.mercy-preview+json'
    },
    'github_url': 'https://api.github.com/orgs/{}/repos?client_id={}&&client_secrete={}',
    'bitbucket_url': 'https://api.bitbucket.org/2.0/repositories/{}',
    'message': 'Pleas provide both github client Id and client secrete',
    'bitbucket_followers': 'https://api.bitbucket.org/2.0/teams/{}/followers',
    'profile': {
        'total_repo': 0,
        'total_forked_repo': 0,
        'total_team_followers': 0,
        'total_watchers_across_all_repo': 0,
        'list_of_languages_across_all_repo': [],
        'topic_list': []
    }
}
message = {
     'not_found': '{} not found'
 }