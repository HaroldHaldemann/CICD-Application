# Introduction

This project is a refactoring work of the repository [Python-OC-Lettings-FR](https://github.com/OpenClassrooms-Student-Center/Python-OC-Lettings-FR) project.
CI/CD pipelines have been added with [CircleCI](https://circleci.com).
The application can be deployed with [Heroku](https://www.heroku.com).
You can monitor the application errors with [Sentry](https://sentry.io/welcome/).

# Local development

## Prerequisites

- Python 3.6 or higher.
- A SQLite3 client for easier database modifications.

## Installation

1 - Clone the github Repository.

```bash
git clone https://github.com/HaroldHaldemann/CICD-Application
```

2 - Create your virtual environment.

```bash
python -m venv name-virtual-env
```

3 - Activate your virtual environment.

On Windows
```windows
name-virtual-env\Scripts\activate.bat #In cmd
name-virtual-env\Scripts\Activate.ps1 #In Powershell
```

NB: If you activate your environment with Powershell, don't forget to enable running script :
```windows
Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser
```

On Unix/MacOs
```bash
source name-virtual-env/bin/activate
```

4 - Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required modules.

```bash
pip install -r ./requirements.txt
```

5 - Make the migrations for Django to enable the database

Then excute the migrations
```bash
python ./manage.py makemigrations
python ./manage.py migrate
```

6 - Create an environment file
```bash
python ./setup_env.py
```

And fill it with according values

```
DJANGO_SECRET_KEY={AUTOMATICALLY_FILLED}
SENTRY_DSN={SENTRY_PROJECT_URL}
HEROKU_APP_NAME={HEROKU_APPLICATION_NAME}
DEBUG={0(False) or 1(True)}
```

## Usage

- To run the server locally, execute the following:
```bash
python ./manage.py runserver
```

Then go to the adress http://127.0.0.1:8000/ in an internet browser.

- To run the linter, execute the following:
```bash
flake8
```

- To run the unit tests, execute the following:
```bash
pytest
```

## Database

- Open a shell session `sqlite3`
- Connect to the database `.open oc-lettings-site.sqlite3`
- View tables in the database `.tables`
- View columns in the profiles table, `pragma table_info(oc_lettings_site_profile);`
- Run a query on the profiles table, `select user_id, favorite_city from oc_lettings_site_profile where favorite_city like 'B%';`
- `.quit` to exit

## Admin panel

- Go to http://127.0.0.1:8000/admin/
- Login with username `admin`, password `Abc1234!`

## Docker

### Build a Docker image to run the app locally


- Build image `docker build -t <image-name> .` with the desired image name
- Use `docker run --rm -p 8080:8080 --env-file .env <image-name>` command, replacing *image-name* with the one built before

You can access the app in your internet browser at http://127.0.0.1:8080/


### Pull an existing image from DockerHub to run the app locally


- Go to your Docker repository
- Use `docker run --rm -p 8080:8080 <DOCKER_LOGIN>/<DOCKER_REPO>:<image-tag>` command, using your docker login and repository and image-tag with the selected tag.

You can access the app in your internet browser at http://127.0.0.1:8080/


# Deployment and CI:CD

## Prerequisites


- [CircleCI](https://circleci.com) account
- [Docker](https://www.docker.com) account
- [Heroku](https://www.heroku.com) account
- [Sentry](https://sentry.io/welcome/) account


## Configuration

### CircleCI


Set up a new project on CircleCI via *"Set Up Project"*.
Select the **master** branch as a source for the *.circleci/config.yml* file.

To run the CircleCI pipeline properly, set up the following environment variables (*Project Settings* > *Environment Variables*):

- DJANGO_SECRET_KEY = Django secret key
- SENTRY_DSN  = Sentry project URL
- DOCKER_LOGIN = Docker account username
- DOCKER_PASSWORD = Docker account password
- DOCKER_REPO = DockerHub repository name
- HEROKU_APP_NAME = Heroku app name
- HEROKU_TOKEN = Heroku token, can be found in account settings (*Heroku API Key*)


### Docker


Create a DockerHub repository. The repository name must match the *DOCKER_REPO* variable set in CircleCI.
The CircleCI workflow will build and push the app image in the DockerHub repository.


### Heroku


Create the app on the Heroku website. The name of the app must match the *HEROKU_APP_NAME* variable set in CircleCI


### Sentry


Set up a Django project. 
The SENTRY_DSN can be found under *Project Settings > Client Keys (DSN)*.

Sentry error logging can be tested via the `/sentry-debug/` endpoint, which will raise a *ZeroDivisionError*.
