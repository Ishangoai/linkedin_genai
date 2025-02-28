from fastapi import FastAPI

from genai_linkedin.model import generate_post_about, generate_technical_guide_about
from genai_linkedin.slack_send import send_message


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
