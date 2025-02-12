import os
from typing import Union
from google import genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch


client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

google_search_tool = Tool(
    google_search=GoogleSearch()
)

generation_config = GenerateContentConfig(
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


def generate_post(contents: Union[str, list[str]]) -> str | None:
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
