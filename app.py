import gradio as gr
import time
import os
from AudioDownloader import download_audio
from TranscriptGenerator import generate_transcript
from QuizGenerator import generate_quiz
from Description import get_description
from QuizDelivery import quiz_handler


def handle_ui1():
    return gr.update(visible=False), gr.update(visible=True)


def handle_ui2(url):
    yield "Downloading Audio...", gr.update(visible=False)

    status, message = download_audio(url)
    print(message, " downloaded")
    time.sleep(1)
    audio_path = f"audio_files/{message}"
    if status:
        yield "Generating transcript...", gr.update(visible=False)

        # if trascript is already generated, skip regenerating transcript to save resources
        if os.path.exists(f"generated_transcript/{message[:-4]}.txt"):
            transcript_status = True
            # Reading already saved transcript
            with open(f"{message[:-4]}.txt") as trans:
                transcript = trans.read()
        else:
            transcript_status, transcript = generate_transcript(audio_path)
            # Saving a copy of transcript
            time.sleep(5)
            with open(f"{message[:-4]}.txt", "w") as file:
                file.write(transcript)
            yield "Transcript Generated!", gr.update(visible=False)
        time.sleep(1)

        if transcript_status:
            global questions
            yield "Generating Quiz...", gr.update(visible=False)
            quiz_status = generate_quiz(transcript, file_name=message[:-4])
            time.sleep(1)
            if quiz_status:
                yield "Quiz generated successfully!", gr.update(visible=True)
            else:
                yield "Quiz generation failed!", gr.update(visible=False)
        else:
            yield "Transcript generation failed!", gr.update(visible=False)
    else:
        yield "Download Failed!", gr.update(visible=False)


def handle_ui3():
    return gr.update(visible=True, render=True), gr.update(visible=False)


with gr.Blocks() as quiz_app:
    with gr.Column(visible=True) as UI_description:
        gr.Markdown(get_description("description.txt"))
        UI_description_submit_btn = gr.Button("Continue")

    with gr.Column(visible=False) as UI_pre_process:
        URL_input = gr.Textbox(placeholder="Enter URL and press submit", label="URL")
        download_start_button = gr.Button("Start Task")
        progress_output = gr.Textbox(label="Progress", lines=2, interactive=False)
        start_quiz_button = gr.Button("Start Quiz", visible=False)
        questions = []

    with gr.Column(visible=False) as UI_quiz:
        # Question
        initial_question = "Question will appear here."
        # Options
        initial_options = ['a', 'b', 'c', 'd']
        # Display the question
        question_text = gr.Textbox(label="Question", value=initial_question, interactive=False)
        # Display the options as radio buttons
        radio_option = gr.Radio(choices=initial_options, label="Options")
        # Submit button
        submit_btn = gr.Button("Submit")
        # Output to display the result of the answer
        output = gr.Textbox(label="Result", interactive=False)
        # Hidden state to track the current question index
        index_state = gr.State(value=-1)

        # Update question, options, and index on button click
        submit_btn.click(
            fn=quiz_handler,
            inputs=[radio_option, index_state],
            outputs=[question_text, radio_option, output, index_state, submit_btn]
        )

    # UI1 to UI2
    UI_description_submit_btn.click(handle_ui1, outputs=[UI_description, UI_pre_process])
    # Download and generate quiz
    download_start_button.click(handle_ui2, inputs=[URL_input], outputs=[progress_output, start_quiz_button])
    # Prepare quiz
    start_quiz_button.click(handle_ui3, outputs=[UI_quiz, UI_pre_process])

quiz_app.launch(share=True)
