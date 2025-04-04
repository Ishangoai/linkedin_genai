import os

from slack_sdk import WebClient
from slack_sdk.signature import SignatureVerifier
from slack_sdk.errors import SlackApiError


# Initialize the Slack client
client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])

signature_verifier = SignatureVerifier(
    signing_secret=os.environ["SLACK_SIGNING_SECRET"]
)


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


async def is_valid_signature(request):
    # Verify the request signature
    body = await request.body()
    return signature_verifier.is_valid_request(
        body=body,
        headers=request.headers
    )
