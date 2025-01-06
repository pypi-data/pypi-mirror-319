import hashlib
import hmac
import logging
import os
import sys
from asyncio import subprocess
from typing import Annotated

import git
import github
import requests
import yaml
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Header, BackgroundTasks, Depends
from fastapi import HTTPException
from fastapi.logger import logger
from fastapi.security import OAuth2PasswordBearer
from github.GithubIntegration import GithubIntegration

from utils import discord_webhook, run_deploy

if os.environ.get('GITHUB_APP_ID'):
    GH_APP_ID = os.environ.get('GITHUB_APP_ID')
    GH_APP_SECRET = open(os.environ.get('GITHUB_SECRET_FILE')).read()

def load_yaml(config_file):
    with open(config_file, 'r') as config_stream:
        return yaml.load(config_stream, Loader=yaml.FullLoader)


def write_yaml(config_file, dump):
    with open(config_file, 'w') as config_stream:
        yaml.dump(dump, config_stream)

config = load_yaml('config.yml')


def get_app_config(token=None, repo=None):
    for deployment in config:
        for app_name, values in deployment.items():
            if repo == values.get('repo') or token in values.get('tokens'):
                return {
                    'app_name': app_name,
                    'repo': values['repo'],
                    'branch': values.get('branch', 'main'),
                    'owner': values['repo'].split('/')[0],
                    'repo_name': values['repo'].split('/')[1],
                }


async def verify_signature(payload_body, secret_token, signature_header):
    if not signature_header:
        raise HTTPException(status_code=403, detail="x-hub-signature-256 header is missing!")
    hash_object = hmac.new(secret_token.encode(), msg=payload_body, digestmod=hashlib.sha256)
    expected_signature = "sha256=" + hash_object.hexdigest()

    if not hmac.compare_digest(expected_signature, signature_header):
        print(expected_signature)
        print("signature doesnt match")
        raise HTTPException(status_code=403, detail="Request signatures didn't match!")


def get_gh_access_token(app_config):
    auth = github.Auth.AppAuth(GH_APP_ID, GH_APP_SECRET)
    gi = github.GithubIntegration.GithubIntegration(auth=auth)
    installation = gi.get_repo_installation(app_config['owner'], app_config['repo_name'])
    access_token = gi.get_access_token(installation.id).token
    return access_token


def update_repo(app_config, access_token):
    origin_url = f"https://x-access-token:{access_token}@github.com/{app_config['repo']}"
    repo_path = f'./test/{app_config["app_name"]}'
    repo = git.Repo.init(repo_path)
    origin = repo.create_remote("origin", origin_url)
    repo.remotes.origin.pull(app_config['branch'])
    repo.delete_remote(origin)


async def update_repo_and_deploy(app_config):
    discord_webhook(f"## :arrow_right: Deploying {app_config['app_name']}")

    access_token = get_gh_access_token(app_config)
    update_repo(app_config, access_token)

    # run deployment
    message = await run_deploy(app_config['app_name'])

    # healthcheck

    # call chat webhooks
    discord_webhook(message)
    discord_webhook(f"## :white_check_mark: {app_config['app_name']} Deployed")



# @app.post('/cd')
# async def cd(request: Request, background_tasks: BackgroundTasks, token: Annotated[str, Depends(oauth2_scheme)]):
#     app_config = get_app_config(token=token)
#     if not app_config:
#         raise HTTPException(status_code=403, detail='not app configured found for webhook')
#
#     payload = await request.json()
#     # print(payload)
#
#     background_tasks.add_task(update_repo_and_deploy, app_config)
#
#     return {"status": "queued"}
#
# @app.post('/github/')
# async def webhook(request: Request,
#                   background_tasks: BackgroundTasks,
#                   x_github_event: Annotated[str | None, Header()] = None,
#                   x_hub_signature_256: Annotated[str | None, Header()] = None):
#     await verify_signature(await request.body(), os.environ.get('GITHUB_WEBHOOK_SECRET'), x_hub_signature_256)
#     payload = await request.json()
#     action = payload.get('action')
#     print(x_github_event, action)
#
#     app_config = get_app_config(repo=payload['repository']['full_name'])
#     if not app_config:
#         raise HTTPException(status_code=403, detail='no app config found for webhook')
#
#     if x_github_event == 'push':
#         background_tasks.add_task(update_repo_and_deploy, app_config)
#
#     return {"status": "queued"}
