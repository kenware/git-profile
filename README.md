# Git profile
[![CircleCI](https://circleci.com/gh/kenware/git-profile/tree/staging.svg?style=svg)](https://circleci.com/gh/kenware/git-profile/tree/staging)

Git profile is an app that merge team/organisations github profile and bitbucket profile serving as a single source of truth.

## Setup And Installation:

* install virtualenv if you don't have it
    ```
    pip install virtualenv

    ```
* On the root directory of the project run on the terminal
  ```
  virtualenv env
  ```
* In the root directory, open `env/bin/activate` file and add the environmental variable at the bottom of the activate file accordingto the sample bellow:

    ``` 
    export GITHUB_CLIENT_ID=<client_id>
    export GITHUB_CLIENT_SECRETE=<client_secrete>

    ```
* NB: Github client secrete and client id is required. This is to avoid github [api rate limit](https://developer.github.com/v3/#rate-limiting)
* Activate Virtualenv
  ```
  source env/bin/activate
  ```

## Running the code
* Run Test
  ```
  pytest
  ```
* Spin up the service

    ```
    # start up local server
    python -m run 
    ```

* Making Requests

    ```
    curl -i "http://127.0.0.1:5000/git-profile/<team_name>"
    ```
