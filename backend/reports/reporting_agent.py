from openai import OpenAI
import os
from pydantic import BaseModel, Field, ConfigDict

# Load environment variables
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


class Student(BaseModel):
    name: str
    subjects: list[str] = Field(alias="subjects")

class Lesson(BaseModel):
    # Allow population by field name in addition to aliases and ignore extra keys
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    title: str = Field(alias="lesson_title")
    student: Student
    notes: str = Field(alias="lesson_notes")
    transcript: str = Field(alias="transcript")







client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("OPEN_ROUTER_API_KEY"),
)


completion = client.chat.completions.create(
  model="openai/gpt-4o",
  # pass extra_body to access OpenRouter-only arguments.
  # extra_body={
    # "models": [
    #   "${Model.GPT_4_Omni}",
    #   "${Model.Mixtral_8x_22B_Instruct}"
    # ]
  # },
  messages=[
    {
      "role": "user",
      "content": "Say this is a test",
    },
  ],
)
print(completion.choices[0].message.content)





class ReportingAgent:
    def __init__(self):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPEN_ROUTER_API_KEY"),
        )

    def generate_report(self, lesson_details: "Lesson") -> str:
        """
        Generate a report for a given lesson details.

        Args:
            lesson_details: Lesson data describing the session details.

        Returns:
            A string containing the report.
        """
        pass