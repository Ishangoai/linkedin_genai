import os

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


# Initialize the Slack client
client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])


def send_message(message):
    try:
        # Send a message to the channel
        response = client.chat_postMessage(
            channel="#linkedin_posts",
            text=message
        )
        print("Message sent successfully!")
        return response
    except SlackApiError as e:
        print(f"Error sending message: {e.response['error']}")
