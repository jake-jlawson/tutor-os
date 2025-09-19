import os

from reporting_agent import ReportingAgent, Lesson

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
key = os.getenv("OPEN_ROUTER_API_KEY")


# REPORT LESSON DETAILS (INPUT)
lesson_details = Lesson.model_validate({
    "lesson_title": "ESAT Content (P2): Transformers & Transformer Problems",
    "student": {
        "name": "Chloe",
        "subjects": [
            "Cambridge Engineering Admissions", 
            "Admissions Test (ESAT)", 
            "Interview Prep"
        ],
    },
    "lesson_notes": """""",
    "transcript": "",
})






if __name__ == "__main__":
    print(key)
    pass