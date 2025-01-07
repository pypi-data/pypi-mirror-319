import speech_recognition as sr
from pydub import AudioSegment
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm
import io

class Voxcribe:
    def __init__(self, chunk_duration=30, show_progress=True):
        """
        Initialize the AudioTranscriber.
        :param chunk_duration: Duration of each audio chunk in seconds (default is 30).
        :param show_progress: Whether to display a progress bar (default is True).
        """
        self.chunk_duration = chunk_duration
        self.show_progress = show_progress
        self.recognizer = sr.Recognizer()

    def _process_chunk(self, chunk_data):
        chunk, start_time, end_time = chunk_data
        with io.BytesIO() as temp_chunk_file:
            chunk.export(temp_chunk_file, format="wav")
            temp_chunk_file.seek(0)

            try:
                with sr.AudioFile(temp_chunk_file) as source:
                    audio_data = self.recognizer.record(source)
                    text = self.recognizer.recognize_google(audio_data)
            except sr.UnknownValueError:
                text = "[Unintelligible audio]"
            except sr.RequestError as e:
                text = f"[Error with the recognition service: {e}]"
        return text

    def _split_audio(self, audio):
        total_duration = len(audio) // 1000  # Convert milliseconds to seconds
        return [
            (audio[start_time * 1000:end_time * 1000], start_time, end_time)
            for start_time in range(0, total_duration, self.chunk_duration)
            for end_time in [min(start_time + self.chunk_duration, total_duration)]
        ]

    def transcribe(self, file_path):
        try:
            # Load the audio file
            audio = AudioSegment.from_file(file_path)
        except Exception as e:
            return f"[Error loading audio file: {e}]"

        # Split the audio into chunks
        chunks = self._split_audio(audio)

        # Process chunks using ProcessPoolExecutor with an optional progress bar
        results = []
        with ProcessPoolExecutor() as executor:
            if self.show_progress:
                for result in tqdm(executor.map(self._process_chunk, chunks), total=len(chunks), desc="Processing audio chunks"):
                    results.append(result)
            else:
                results = list(executor.map(self._process_chunk, chunks))

        return " ".join(results)


# Example usage
# if __name__ == "__main__":
#     # Set show_progress to False if you don't want the progress bar
#     transcriber = Voxcribe()
#     result = transcriber.transcribe("audio.mp3")
#     print("Transcription:")
#     print(result)
