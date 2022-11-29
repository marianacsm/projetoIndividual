# crie um arquivo de credenciais do slack
# e coloque o token do seu bot
# https://api.slack.com/bot-users
# https://api.slack.com/custom-integrations/legacy-tokens

# Path: dashboard\slack.py

import slack
import slackCredentials

class Slack:
    def __init__(self):
        self.client = slack.WebClient(token=slackCredentials.token)

    def post_message(self, channel, text):
        self.client.chat_postMessage(channel=channel, text=text)

    def post_message_with_attachment(self, channel, text, attachment):
        self.client.chat_postMessage(channel=channel, text=text, attachments=[attachment])

    def post_message_with_attachments(self, channel, text, attachments):
        self.client.chat_postMessage(channel=channel, text=text, attachments=attachments)

    def post_message_with_block(self, channel, text, block):
        self.client.chat_postMessage(channel=channel, text=text, blocks=[block])

    def post_message_with_blocks(self, channel, text, blocks):
        self.client.chat_postMessage(channel=channel, text=text, blocks=blocks)

    def post_message_with_block_and_attachment(self, channel, text, block, attachment):
        self.client.chat_postMessage(channel=channel, text=text, blocks=[block], attachments=[attachment])