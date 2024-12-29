import google.generativeai as genai
import os
import json
import re
from Prompt import get_prompt


def generate_quiz(summary, file_name):
    try:
        genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(get_prompt('quiz_max_question_prompt.txt') + summary)

        # Use regex to extract the JSON string
        filtered = re.search(r'\[.*\]', str(response.text), re.DOTALL).group(0)

        # Load the extracted JSON string
        data = json.loads(filtered)

        # Write to file
        with open(f'quiz_json/{file_name}.json', 'w') as file:
            json.dump(data, file, indent=4)
        return True
    except Exception as ge:
        print(ge)
        return False
