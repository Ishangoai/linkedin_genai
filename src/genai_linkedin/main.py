from fastapi import FastAPI, Request, HTTPException, Response
from slack_sdk import WebhookClient

from genai_linkedin.model import generate_post_about, generate_technical_guide_about
from genai_linkedin.slack_send import send_message, is_valid_signature


app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/run")
def read_response():
    Option_1 = generate_post_about("the latest trends in AI and ML")
    Option_2 = generate_post_about("the trending tech news this week")
    Option_3 = generate_technical_guide_about("regression analysis in Python")
    return {"Option_1": Option_1, "Option_2": Option_2, "Option_3": Option_3}


@app.get("/run_send")
def send_response():
    Option_1 = generate_post_about("the latest trends in AI and ML")
    Option_2 = generate_post_about("the trending tech news this week")
    Option_3 = generate_technical_guide_about("regression analysis in Python")
    message = f"Option 1: {Option_1}\n\nOption 2: {Option_2}\n\nOption 3: {Option_3}"
    res = send_message(message)
    return "sent" if res else "error"


@app.post("/slack/events")
async def webhook(request: Request):

    if not is_valid_signature(request):
        # if slack challenge request
        if request.method == "GET":
            # Handle the URL verification challenge
            return Response(request.query_params["challenge"], 200)
        raise HTTPException(status_code=403, detail="Invalid signature")

    form = await request.form()
    if "command" in form \
        and form["command"] == "/run_test":
        response_url = str(form["response_url"])
        text = form["text"]
        webhook = WebhookClient(response_url)
        # Send a reply in the channel
        response = webhook.send(text=f"Hi {form['user_name']}, you sent: {text}")
        # Acknowledge this request
        return Response("", 200)

    if "command" in form \
        and form["command"] == "/run_send":
        response_url = str(form["response_url"])
        Option_1 = generate_post_about("the latest trends in AI and ML")
        Option_2 = generate_post_about("the trending tech news this week")
        Option_3 = generate_technical_guide_about("regression analysis in Python")
        message = f"Option 1: {Option_1}\n\nOption 2: {Option_2}\n\nOption 3: {Option_3}"
        webhook = WebhookClient(response_url)
        # Send a reply in the channel
        response = webhook.send(text=message)
        # Acknowledge this request
        return Response("", 200)

    else:
        # Handle other events
        return Response("success", 200)
