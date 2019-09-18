import json

def test_git_profile(client, mock_test, mock_test2, mock_test3):
    """Start with a blank database."""

    print(client)
    response = client.get('/git-profile/pygame')
    print(response.data)
    assert b'total_repo' in response.data
    assert b'total_forked_repo' in response.data
    data = json.loads(response.data)
    assert data['total_original_repo'] == data['total_repo'] - data['total_forked_repo']
