from fastapi import APIRouter

from hyperpocket.server.auth.github import github_auth_router
from hyperpocket.server.auth.google import google_auth_router
from hyperpocket.server.auth.linear import linear_auth_router
from hyperpocket.server.auth.slack import slack_auth_router
from hyperpocket.server.auth.token import token_router
from hyperpocket.server.auth.calendly import calendly_auth_router
from hyperpocket.util.get_objects_from_subpackage import get_objects_from_subpackage

auth_router = APIRouter(prefix="/auth")

routers = get_objects_from_subpackage("hyperpocket.server.auth", APIRouter)
for r in routers:
    auth_router.include_router(r)
