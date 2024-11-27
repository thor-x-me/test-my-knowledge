from dotenv import load_dotenv
import os
from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)
load_dotenv()


def generate_transcript(audio_file):
    deepgram_api = os.environ.get("DEEPGRAM_API_KEY")
    try:
        deepgram = DeepgramClient(deepgram_api)

        with open(audio_file, "rb") as file:
            buffer_data = file.read()

        payload: FileSource = {
            "buffer": buffer_data,
        }

        options = PrerecordedOptions(
            model="nova-2",
            smart_format=True,
        )

        response = deepgram.listen.rest.v("1").transcribe_file(payload, options)
        print("Transcript generation completed!")

        return True, response.results.channels[0].alternatives[0].transcript

    except Exception as e:
        print(f"Exception: {e}")
        return False, "Failed!"
