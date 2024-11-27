import gradio as gr

# Function to handle the quiz logic and update question index


def quiz_handler(option, index):
    if index == -1:
        # Check if the answer is correct
        result = "Correct Answer" if questions[index]["Answer"] == option else "Wrong Answer"
        # Increment the index to load the next question
        index += 1
        # Check if there are more questions left
        if index < len(questions):
            # Return the next question, updated options, result, and updated index
            return (
                questions[index]["Question"],
                gr.update(choices=questions[index]["Option"]),
                result,
                index
            )
        else:
            # End of quiz
            return "Quiz Completed!", gr.update(choices=[]), result, index
