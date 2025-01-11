from hyperpocket.auth.context import AuthContext
from hyperpocket.auth.github.context import GitHubAuthContext
from hyperpocket.auth.github.oauth2_context import GitHubOAuth2AuthContext
from hyperpocket.auth.github.token_context import GitHubTokenAuthContext
from hyperpocket.auth.google.context import GoogleAuthContext
from hyperpocket.auth.google.oauth2_context import GoogleOAuth2AuthContext
from hyperpocket.auth.handler import AuthHandlerInterface
from hyperpocket.auth.linear.token_context import LinearTokenAuthContext
from hyperpocket.auth.provider import AuthProvider
from hyperpocket.auth.slack.oauth2_context import SlackOAuth2AuthContext
from hyperpocket.auth.slack.token_context import SlackTokenAuthContext
from hyperpocket.util.find_all_leaf_class_in_package import find_all_leaf_class_in_package

PREBUILT_AUTH_HANDLERS = find_all_leaf_class_in_package("hyperpocket.auth", AuthHandlerInterface)
AUTH_CONTEXT_MAP = {
    leaf.__name__: leaf for leaf in find_all_leaf_class_in_package("hyperpocket.auth", AuthContext)
}

__all__ = [
    'PREBUILT_AUTH_HANDLERS',
    'AUTH_CONTEXT_MAP',
    'AuthProvider',
    'AuthHandlerInterface',
]
