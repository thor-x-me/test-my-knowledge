import gradio as gr
import os
import json
from datetime import datetime


def find_newest_file(directory):
    """
    Find the newest file in the specified directory.

    Args:
        directory (str): Path to the directory to search

    Returns:
        str: Full path to the newest file, or None if directory is empty
    """
    # Check if directory exists
    if not os.path.exists(directory):
        raise ValueError(f"Directory {directory} does not exist")

    # Check if it's actually a directory
    if not os.path.isdir(directory):
        raise ValueError(f"{directory} is not a directory")

    # List to store file information
    files = []

    # Iterate through all files in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        # Skip subdirectories
        if os.path.isdir(file_path):
            continue

        # Get file's last modification time
        try:
            mod_time = os.path.getmtime(file_path)
            files.append((file_path, mod_time))
        except Exception as e:
            print(f"Could not get modification time for {file_path}: {e}")

    # If no files found, return None
    if not files:
        return None

    # Find the file with the most recent modification time
    newest_file = max(files, key=lambda x: x[1])

    return newest_file[0]


# Function to handle the quiz logic and update question index
def quiz_handler(option, index, correct, wrong):
    question_folder = 'quiz_json'
    latest_quiz = find_newest_file(question_folder)
    with open(latest_quiz, 'r') as quiz:
        questions = json.load(quiz)

    # controller to start delivering questions.
    if index == -1:
        result = 'Select your option'
    else:
        # Check if the answer is correct
        if questions[index]["Answer"] == option:
            result = "Correct Answer"
            correct += 1
        else:
            result = "Wrong Answer"
            wrong += 1

    # Increment the index to load the next question
    index += 1
    # Check if there are more questions left
    if index < len(questions):
        # Return the next question, updated options, result, and updated index
        return (
            questions[index]["Question"],
            gr.update(choices=questions[index]["Option"]),
            result,
            index,
            gr.update(visible=True),
            correct,
            wrong
        )
    else:
        # End of quiz
        return (
            "Quiz Completed!",
            gr.update(choices=[]),
            result,
            index,
            gr.update(visible=False),
            correct,
            wrong)
