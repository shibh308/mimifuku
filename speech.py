from credentials import credential_json_path
from google.cloud import texttospeech
from pydub import AudioSegment
import pathlib
import os
import io

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_json_path

def generate_and_save_audio(text: str, filepath: pathlib.Path):
    filepath.parent.mkdir(parents=True, exist_ok=True)
    print(f'generating: {filepath}')

    is_long = len(text.encode()) > 5000

    client =  texttospeech.TextToSpeechClient()


    voice = texttospeech.VoiceSelectionParams(
        language_code="ja-JP",
        name="ja-JP-Wavenet-D",
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = None

    if is_long:
        lines = text.split('\n')
        audio_bytes = []
        while lines:
            text_bytes = b''
            while lines and len(text_bytes) + len(lines[0].encode()) <= 5000:
                text_bytes += lines.pop(0).encode()
            synthesis_input = texttospeech.SynthesisInput(text=text_bytes.decode())
            response = client.synthesize_speech(
                input=synthesis_input, voice=voice, audio_config=audio_config
            )
            audio_bytes.append(response.audio_content)
        audio_segments = [AudioSegment.from_mp3(io.BytesIO(audio)) for audio in audio_bytes]
        audio = audio_segments[0]
        for seg in audio_segments[1:]:
            audio += seg
        audio.export(filepath, format="mp3")
    else:
        synthesis_input = texttospeech.SynthesisInput(text=text)
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        with open(filepath, "wb") as out:
            out.write(response.audio_content)
    print(f"generated: {filepath}")


if __name__ == '__main__':
    content = synthesize_text("これはsampleです。string attractorの検索", "output.mp3")
