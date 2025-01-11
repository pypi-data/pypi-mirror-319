# import asyncio
# from unittest import TestCase
# from unittest.mock import patch
#
# from pocket.auth.context import AuthContext
# from pocket.auth.slack.token_handler import SlackTokenAuthHandler
# from pocket.auth.slack.token_schema import SlackTokenRequest
#
#
# class TestSlackTokenAuthHandler(TestCase):
#     def test_authenticate(self):
#         loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(loop)
#
#         slack_auth = SlackTokenAuthHandler()
#         auth_req = SlackTokenRequest()
#
#         # when
#         with patch("builtins.input", return_value="test-slack-token"):
#             context: AuthContext = loop.run_until_complete(slack_auth.authenticate(auth_req))
#
#         # then
#         assert context.access_token == "test-slack-token"
