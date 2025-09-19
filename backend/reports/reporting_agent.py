from openai import OpenAI
import os
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from pathlib import Path

# Load environment variables
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

class Agency(str, Enum):
    TutorChase = "TutorChase"
    UniAdmissions = "UniAdmissions"
    OxbridgeApplications = "OxbridgeApplications"

class Student(BaseModel):
    name: str
    subjects: list[str] = Field(alias="subjects")

class Lesson(BaseModel):
    # Allow population by field name in addition to aliases and ignore extra keys
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    title: str = Field(alias="title")
    agency: Agency = Field(alias="agency")
    student: Student
    notes: str = Field(alias="additional_notes")
    transcript: str = Field(alias="transcript")







client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("OPEN_ROUTER_API_KEY"),
)


# completion = client.chat.completions.create(
#   model="openai/gpt-4o",
#   # pass extra_body to access OpenRouter-only arguments.
#   # extra_body={
#     # "models": [
#     #   "${Model.GPT_4_Omni}",
#     #   "${Model.Mixtral_8x_22B_Instruct}"
#     # ]
#   # },
#   messages=[
#     {
#       "role": "user",
#       "content": "Say this is a test",
#     },
#   ],
# )
# print(completion.choices[0].message.content)





class ReportingAgent:
    def __init__(self):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPEN_ROUTER_API_KEY"),
        )
        from system_prompts import system_prompt_1
        self.system_prompt = system_prompt_1
        from user_prompts import user_prompt_1
        self.user_prompt = user_prompt_1

    def generate_report(self, lesson: Lesson, transcript_path: str, example_settings: dict, ) -> str:
        """
        Generate a report for a given lesson details.

        Args:
            lesson_details: Lesson data describing the session details.

        Returns:
            A string containing the report.
        """
        # Construct the system prompt
        system_prompt = self.system_prompt.substitute(
          report_format=self.load_format(lesson.agency),
          examples=self.load_examples(example_settings["folder_path"], example_settings["n_examples"]),
        )
        # Construct lesson data (not used in template yet but useful for debugging)
        user_prompt = self.user_prompt.substitute(
          lesson_text=self.load_lesson_text(lesson),
          transcript=self.load_transcript(transcript_path),
        )

        report = self.client.chat.completions.create(
          model="openai/gpt-4o",
          messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
          ],
        )
        self.save_report(report.choices[0].message.content, "reports/outputs/" + os.path.basename(transcript_path))
        return report.choices[0].message.content

 
    def load_examples(self, folder_path: str, n: int) -> str:
        """
        Load up to n example .md files from folder_path and wrap each in
        <Example> ... <Example/> tags, stacked vertically. If n exceeds the
        number of available examples, use all available.

        The folder_path may be absolute or relative. If relative, several
        sensible base directories are attempted for convenience.
        """

        def resolve_candidates(raw_path: str) -> list[Path]:
            candidates: list[Path] = []
            raw = Path(raw_path)
            here = Path(__file__).resolve().parent
            repo_root = here.parent.parent

            # As provided
            candidates.append(raw)
            # Relative to this module directory
            candidates.append(here / raw)
            # Common subfolders
            candidates.append(here / "report-examples" / raw)
            candidates.append(here / "report-examples" / raw.name)
            # Relative to repo root
            candidates.append(repo_root / raw)
            candidates.append(repo_root / "backend" / "reports" / raw)
            candidates.append(repo_root / "backend" / "reports" / "report-examples" / raw)
            candidates.append(repo_root / "backend" / "reports" / "report-examples" / raw.name)

            # Deduplicate while preserving order
            seen: set[Path] = set()
            unique: list[Path] = []
            for p in candidates:
                if p not in seen:
                    unique.append(p)
                    seen.add(p)
            return unique

        base_dir: Path | None = None
        for candidate in resolve_candidates(folder_path):
            if candidate.exists() and candidate.is_dir():
                base_dir = candidate
                break

        if base_dir is None:
            # Folder not found; return empty string to avoid breaking prompt
            return ""

        # Find markdown files (non-recursive first, then fallback to recursive if none)
        md_files = sorted([p for p in base_dir.glob("*.md") if p.is_file()])
        if not md_files:
            md_files = sorted([p for p in base_dir.rglob("*.md") if p.is_file()])

        if not md_files:
            return ""

        limit = min(max(n, 0), len(md_files))
        selected = md_files[:limit]

        # Build indented block with <Examples> wrapper.
        lines: list[str] = []

        for file_path in selected:
            try:
                content = file_path.read_text(encoding="utf-8")
            except Exception:
                continue
            # Indent tags by 4 spaces (template adds 4 to the first line only)
            lines.append("      <Example>")
            # Keep original content formatting to avoid breaking markdown semantics
            lines.append(content)
            lines.append("      <Example/>")
        return "\n".join(lines)

    def load_format(self, agency: Agency) -> str:
        """
        Load the format for a given agency.
        """
        from formats import report_formats
        return report_formats[agency]

    def load_lesson_text(self, lesson: Lesson) -> str:
        """
        Load the lesson text for a given lesson.
        """
        import json
        # lesson is a Pydantic model, not a dict. Use model_dump to extract fields.
        data = lesson.model_dump(include={"title", "student", "notes"}, by_alias=False)
        return json.dumps(data, indent=2)
        
    def load_transcript(self, transcript_path: str) -> str:
        """
        Load the transcript for a given lesson.
        """
        path = Path(transcript_path)
        here = Path(__file__).resolve().parent
        repo_root = here.parent.parent

        candidates = [
            path,
            here / path,
            repo_root / path,
            repo_root / "backend" / "reports" / path,
        ]

        for candidate in candidates:
            if candidate.exists() and candidate.is_file():
                return candidate.read_text(encoding="utf-8")

        # Not found; return empty string to avoid breaking callers
        return ""


    def save_report(self, report: str, report_path: str) -> None:
        """
        Save the report to a given path.
        """
        # Create the file if it doesn't exist
        if not os.path.exists(report_path):
          os.makedirs(os.path.dirname(report_path), exist_ok=True)
          
        with open(report_path, "w") as f:
          f.write(report)