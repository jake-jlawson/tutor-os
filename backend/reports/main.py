import os

from reporting_agent import ReportingAgent, Lesson

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
key = os.getenv("OPEN_ROUTER_API_KEY")


# REPORT LESSON DETAILS (INPUT)
example_settings = {
    "folder_path": "examples/oa-admissions-test",
    "n_examples": 5,
}

lesson_details = Lesson.model_validate({
    "title": "ESAT Content (P2): Transformers & Transformer Problems",
    "agency": "OxbridgeApplications",
    "student": {
        "name": "Ruben",
        "subjects": [
            "Cambridge Engineering Admissions", 
            "Admissions Test (ESAT)", 
            "Interview Prep"
        ],
    },
    "additional_notes": """
    """,
    "transcript": "transcripts/ruben_2025-09-17.md",
})

transcript_path = "transcripts/ruben_2025-09-17.md"


if __name__ == "__main__":
    print("Generating report...")
    report = ReportingAgent().generate_report(lesson_details, transcript_path, example_settings)
    print("Report: ", report)