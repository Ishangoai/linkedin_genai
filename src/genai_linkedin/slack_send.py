import os

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

SLACK_TOKEN = os.environ["SLACK_API_TOKEN"]
CHANNEL = "#general"  # Replace with your channel name

# Initialize the Slack client
client = WebClient(token=SLACK_TOKEN)


def send_message(message):
    try:
        # Send a message to the channel
        response = client.chat_postMessage(
            channel=CHANNEL,
            text=message
        )
        print("Message sent successfully!")
        return response
    except SlackApiError as e:
        print(f"Error sending message: {e.response['error']}")
