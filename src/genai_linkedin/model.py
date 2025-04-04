import os
import typing
import google.genai as google_genai
import google.genai.types as google_genai_types


client = google_genai.Client(api_key=os.environ["GEMINI_API_KEY"])

google_search_tool = google_genai_types.Tool(
    google_search=google_genai_types.GoogleSearch()
)

generation_config = google_genai_types.GenerateContentConfig(
  temperature=1,
  top_p=0.95,
  top_k=40,
  max_output_tokens=8192,
  response_mime_type="text/plain",
  tools=[
      google_search_tool
  ],
  system_instruction=[
      "You are an automated bot for generating Engaging LinkedIn posts for a tech company.",
      "Include neccessary hashtags in the post."
  ]
)


def generate_post(contents: typing.Union[str, list[str]]) -> str | None:
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=contents,
        config=generation_config,
    )

    return response.text


def generate_post_about(topic: str) -> str | None:
    contents = f"Generate a new post for today about {topic}"
    return generate_post(contents)


def generate_technical_guide_about(topic: str) -> str | None:
    contents = [
        f"Generate a technical guide about {topic}",
        "Make sure to include all the necessary details, code snippets and steps to follow.",
        ]
    return generate_post(contents)


def process_run_send() -> str:
    # Generate the options
    Option_1 = generate_post_about("the latest trends in AI and ML")
    Option_2 = generate_post_about("the trending tech news this week")
    Option_3 = generate_technical_guide_about("regression analysis in Python")
    return f"Option 1: {Option_1}\n\nOption 2: {Option_2}\n\nOption 3: {Option_3}"
