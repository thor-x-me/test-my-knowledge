from pytubefix import YouTube
import os


def get_newest_file(directory):
    """Returns the name of the newest file in a directory."""
    newest_file = None
    newest_mtime = 0
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):  # Check if it's a file (not a directory)
            mtime = os.path.getmtime(filepath)
            if mtime > newest_mtime:
                newest_mtime = mtime
                newest_file = filename
    return newest_file


def download_audio(url, path="audio_files"):
    try:
        yt = YouTube(url)

        stream = yt.streams.get_audio_only()

        # Making sure if the path exist, creating otherwise
        if not os.path.exists(path):
            os.makedirs(path)

        print(f"Downloading: {yt.title}...")

        # Downloading the audio
        stream.download(output_path=path)

        print(f"Download completed! file saved to {path}")

    except Exception as e:
        print(f"An error occurred: {e}")
        return False, "Failed"

    return True, get_newest_file('audio_files')
