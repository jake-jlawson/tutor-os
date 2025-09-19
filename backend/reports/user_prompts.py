from string import Template


user_prompt_1 = Template("""Here is the data for the most recent lesson:
<Lesson Information>
$lesson_text
</Lesson Information>

<Lesson Transcript>
$transcript
</Lesson Transcript>
""")