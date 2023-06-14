Test
# Introduction

This project is a refactoring work of the repository [Python-OC-Lettings-FR](https://github.com/OpenClassrooms-Student-Center/Python-OC-Lettings-FR) project.
CI/CD pipelines have been added with [CircleCI](https://circleci.com).
The application can be deployed with [Heroku](https://www.heroku.com).
You can monitor the application errors with [Sentry](https://sentry.io/welcome/).

# Local development

## Prerequisites

- Python 3.6 or higher.
- A SQLite3 client (for database modification)
- Docker Desktop (for running, building and pushing images locally)

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

NB: On Windows, you must add your SQLite folder to your PATH system variable for the command `sqlite3` to work

- Go to your application directory (where oc-lettings-site.sqlite3 is)
- Open a shell session `sqlite3`
- Connect to the database `.open oc-lettings-site.sqlite3`
- Request examples:
    - View tables in the database `.tables`
    - View columns in the selected table, `pragma table_info(<table_name>);`
    - Run a query on the profiles table, `select user_id, favorite_city from oc_lettings_site_profile where favorite_city like 'B%';`
- `.quit` to exit

## Admin panel

- Go to http://127.0.0.1:8000/admin/
- Login with username `admin`, password `Abc1234!`

## Docker

### Build a Docker image


- Build image `docker build -t <image-name> .` with the desired image name
- Use `docker run --rm -p 8080:8080 --env-file .env <image-name>` command, replacing *image-name* with the one built before.
The .env file is corresponding to the file created by executing `python ./setup_env.py`

You can access the app in your internet browser at http://127.0.0.1:8080/

If you want to push your docker image to DockerHub, make sure to name correctly (ie `<DOCKER_LOGIN>/<DOCKER_REPO>:<image-tag>`)

You can label your docker image by executing `docker tag <image-name> <new-image-name>`
You can push your local image to your Docker repository by executing `docker push <image-name>`

If the push does not work, try to logout and login again by executing 
```bash
docker logout
docker login
```
and correctly fill the asked input


### Pull an existing image from DockerHub to run the app locally


- Go to your Docker repository
- Use `docker run --rm -p <PORT>:8080 <DOCKER_LOGIN>/<DOCKER_REPO>:<image-tag>` command, using your docker login and repository and image-tag with the selected tag.

If you do not know which port to use, simply use `8080`
If your image cannot be found locally, Docker will download the image from your repository.

You can access the app in your internet browser at `http://127.0.0.1:<PORT>/`


# Deployment and CI/CD

## Description

When pushing your commits to your Github repository, a pipeline will be created.
The pipeline will execute the following steps:
- Create virtual environment and activate it
- Install requirements
- Run linter
- Run pytest

If none of the steps are failed and the pushed branch is main, the pipeline will:
- create a docker image and push it to your docker repository.
- deploy your apllcation on Heroku

The deployed application will be accessible at https://$HEROKU_APP_NAME.herokuapp.com

If the pushed branch is an other branch, the image creation and application deployment will not occur.

The pipeline will be accessible at https://app.circleci.com/pipelines/github/$GITHUB_REPO_OWNER/$GITHUB_REPO_NAME

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

- DJANGO_SECRET_KEY = Django secret key (get the one from your .env file)
- SENTRY_DSN  = Sentry project URL (under *Project Settings* > *Client Keys(DSN)*)
- DOCKER_LOGIN = Docker account username
- DOCKER_PASSWORD = Docker account password
- DOCKER_REPO = DockerHub repository name
- HEROKU_APP_NAME = Heroku app name
- HEROKU_TOKEN = Heroku token, can be found in account settings (*Heroku API Key*)

The pipeline is accessible at https://app.circleci.com/pipelines/github/$GITHUB_REPO_OWNER/$GITHUB_REPO_NAME


### Docker


Create a DockerHub repository. The repository name must match the *DOCKER_REPO* variable set in CircleCI.
The CircleCI pipeline will build and push the app image in the DockerHub repository.

The available images can be accessed at https://hub.docker.com/repository/docker/$DOCKER_USERNAME/$DOCKER_REPO/general


### Heroku


Create an app on the Heroku website. The name of the app must match the *HEROKU_APP_NAME* variable set in CircleCI.
The CircleCI pipeline will deploy your application on Heroku.

The deployed application will be available at https://$HEROHU_APP_NAME.herokuapp.com


### Sentry


Set up a Django project, under the Projects tab follow:
- Create Project
- Select Django in Platform
- Configure alert frequency as you want it
- Fill project Name

The SENTRY_DSN can be found under *Project Settings > Client Keys (DSN)*.

Sentry error logging can be tested via the `/sentry-debug/` endpoint, which will raise a *ZeroDivisionError*.
