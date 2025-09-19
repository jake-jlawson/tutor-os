
"""
Report Formats for different tutoring websites
"""

# Oxbridge Admissions
oa_format = """<Report_Format>
        
        # Lesson Title:
        A short but descriptive title for the lesson, describing the overall focuses of the lesson.
        
        # Summary & Student Progress: 
        A summary of the lesson, the things that were covered and the progress the student made. This section could include information such as:
        - A step by step recount/summary of the lesson, going through what was covered and why.
        - A rationale for the lesson (why we covered the things we did and how this will help the student).
        - Strengths / improvements that the student showed and made during the lesson and praise for these improvements.
        - Some feedback points based on things to remember, things we learned / revised, things to improve, and/or things to avoid (these can be listed as prose or bullet points but don't overuse bullet points).

        # Homework & Plans for Next Session: 
        This section should generally discuss two distinct topics in two separate paragraphs:
        - Homework:  Suggestions for homework or additional things that the student can do after the lesson to further progress the lesson outcomes. 
        -- If any explicit suggestions were made by the tutor in the lesson of things to do or focus on these should be included here.
        -- You may also suggest resources the student can use for further reading / learning. Only suggest things if they are relevant and are likely to be helpful for the student.

        - Plans for Next Session:  Suggestions for the next session, such as what we will cover, what we will focus on, etc.
        -- If any explicit suggestions were made by the tutor in the lesson of things to do or focus on these should be included here.
        -- If the student mentioned any specific things they wanted to focus on in the future, these should be also included here.
        -- If no suggestions were made, suggest a plan based on the focuses of this lesson and the natural focus next session, but do not go overboard and invent/assume lots of missing information. 

    <Report_Format/>"""



report_formats = {
    "OxbridgeApplications": oa_format,
}