import speech_recognition as sr
import sys, os, pyaudio
from pocketsphinx import Config, Decoder


def run():
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    # recognize speech using whisper
    try:
        print("Whisper thinks you said " + r.recognize_whisper(audio, language="english"))
    except sr.UnknownValueError:
        print("Whisper could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Whisper; {e}")

def model():
    modeldir = "sphinx/models"

    # Create a decoder with certain model
    config = Config(keyphrase='hey bradley')
    # config.set_string('-hmm', os.path.join(modeldir, 'en-us/en-us'))
    # config.set_string('-dict', os.path.join(modeldir, 'en-us/cmudict-en-us.dict'))
    # #disable -logfn to get logs in console
    # config.set_string('-logfn', 'sphinx/sphinx.log')
    #decoder = Decoder(config)

    #decoder.set_kws('keyword', 'keyword.list')
    #decoder.set_search('keyword')

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True)
    stream.start_stream()

    # Process audio chunk by chunk. On keyword detected perform action and restart search
    decoder = Decoder(config)
    decoder.start_utt()
    while True:
        buf = stream.read(1024)

        decoder.process_raw(buf, False, False)

        if decoder.hyp() != None:
            #print ([(seg.word, seg.prob, seg.start_frame, seg.end_frame) for seg in decoder.seg()])
            for seg in decoder.seg():
                print(seg.word)
                break
            print ("Detected keyword, restarting search")
            #
            # Here you run the code you want based on keyword
            #
            decoder.end_utt()
            decoder.start_utt()


if __name__ == "__main__":
    model()
