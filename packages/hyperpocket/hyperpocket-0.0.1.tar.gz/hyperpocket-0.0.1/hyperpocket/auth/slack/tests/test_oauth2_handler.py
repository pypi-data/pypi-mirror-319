# import asyncio
# from unittest import TestCase
#
# from pocket.auth.slack.oauth2_handler import SlackOAuth2AuthHandler
# from pocket.auth.slack.oauth2_schema import SlackOAuth2Request
# from pocket.config import config
# from pocket.server.server import get_proxy_server, get_server
#
#
# class TestSlackOAuth2AuthHandler(TestCase):
#
#     def test_authenticate(self):
#         loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(loop)
#         server = get_server()
#         asyncio.ensure_future(server.serve(), loop=loop)
#         proxy_server = get_proxy_server()
#         if proxy_server:
#             asyncio.ensure_future(proxy_server.serve(), loop=loop)
#
#         slack_auth = SlackOAuth2AuthHandler()
#         auth_req = SlackOAuth2Request(
#             auth_scopes=["channels:history", "im:history", "mpim:history", "groups:history", "reactions:read"],
#             client_id=config.auth.slack.client_id,
#             client_secret=config.auth.slack.client_secret,
#         )
#
#         # when
#         context = loop.run_until_complete(slack_auth.authenticate(auth_req))
#
#         # then
#         print("access_token : ", context.access_token)
