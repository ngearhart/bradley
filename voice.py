from playsound import playsound
from google.cloud import texttospeech
from os.path import exists, join
from os import mkdir, listdir, getcwd
from hashlib import md5

import logging

logger = logging.getLogger(__name__)

CACHE_FOLDER='./.audio-cache'


def play_sound_of_text(text: str, block: bool=True):
    playsound(get_audio_filename_for_text(text), block=block)


def get_audio_filename_for_text(text: str) -> str:
    """
    Synthesizes speech from the input string of text with caching.
    Return a path to an audio file containing the audio.
    """

    text = text.strip()
    text_hash = md5(text.lower().encode()).hexdigest()
    output_file_name = join(getcwd(), CACHE_FOLDER, text_hash + ".wav")

    logger.debug(f'Checking voice cache for hash {text_hash}')

    if not exists(CACHE_FOLDER):
        mkdir(CACHE_FOLDER)
    elif text_hash + ".wav" in listdir(join(getcwd(), CACHE_FOLDER)):
        logger.debug('Cache hit')
        # Cache hit. Audio file already exists in cache for same text.
        return output_file_name

    logger.debug(f'Cache miss. Asking GCP Voice')
    # text = "Good evening, Noah! I hope you had a great day at work."
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(
        # language_code="en-US",
        # name="en-US-Journey-D",
        language_code="en-GB",
        name="en-GB-Journey-D",
        ssml_gender=texttospeech.SsmlVoiceGender.MALE,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16,
        # speaking_rate=2.0,
        # pitch=-15.0
    )

    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )

    # The response's audio_content is binary.
    with open(output_file_name, "wb") as out:
        out.write(response.audio_content)
    return output_file_name


if __name__ == "__main__":
    text = input()
    play_sound_of_text(text)
