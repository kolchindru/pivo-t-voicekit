from .tinkoff.cloud.stt.v1 import stt_pb2_grpc, stt_pb2
from .tinkoff.cloud.tts.v1 import tts_pb2, tts_pb2_grpc
from .auth import authorization_metadata
import grpc
import os
import json
import wave
from dotenv import load_dotenv
load_dotenv(override=True)

endpoint = os.environ.get("VOICEKIT_ENDPOINT") or "stt.tinkoff.ru:443"
api_key = os.environ["VOICEKIT_API_KEY"]
secret_key = os.environ["VOICEKIT_SECRET_KEY"]
sample_rate = 48000

# ---
# Sound to text part
# ---

def stt_build_first_request(sample_rate_hertz, num_channels):
    request = stt_pb2.StreamingRecognizeRequest()
    request.streaming_config.config.encoding = stt_pb2.AudioEncoding.LINEAR16
    request.streaming_config.config.sample_rate_hertz = sample_rate_hertz
    request.streaming_config.config.num_channels = num_channels
    return request

def stt_generate_requests(wav_filename):
    try:
        with wave.open(wav_filename) as f:
            yield stt_build_first_request(f.getframerate(), f.getnchannels())
            frame_samples = f.getframerate()//10 # Send 100ms at a time
            for data in iter(lambda:f.readframes(frame_samples), b''):
                request = stt_pb2.StreamingRecognizeRequest()
                request.audio_content = data
                yield request
    except Exception as e:
        print("Got exception in stt_generate_requests", e)
        raise

def stt_get_streaming_recognition_responses(responses, debug=False):
    message_pieces = []
    for response in responses:
        for result in response.results:
            if result.recognition_result.channel == 1:
                continue
            for alternative in result.recognition_result.alternatives:
                message_piece = alternative.transcript
                message_pieces.append(message_piece)
    return " ".join(message_pieces)

# Sound to text main method. Convert string to wav.
def stt_wav_to_string(wav_filename):
    stub = stt_pb2_grpc.SpeechToTextStub(grpc.secure_channel(endpoint, grpc.ssl_channel_credentials()))
    metadata = authorization_metadata(api_key, secret_key, "tinkoff.cloud.stt")
    responses = stub.StreamingRecognize(stt_generate_requests(wav_filename), metadata=metadata)
    result_message = stt_get_streaming_recognition_responses(responses)
    return result_message

# ---
# Text to sound part
# ---
def tts_build_request(string):
    return tts_pb2.SynthesizeSpeechRequest(
        input=tts_pb2.SynthesisInput(text=string),
        audio_config=tts_pb2.AudioConfig(
            audio_encoding=tts_pb2.LINEAR16,
            sample_rate_hertz=sample_rate,
        ),
    )

# Text to sound main method
def tts_string_to_wav(string, wav_filename):
    with wave.open(wav_filename, "wb") as f:
        f.setframerate(sample_rate)
        f.setnchannels(1)
        f.setsampwidth(2)

        stub = tts_pb2_grpc.TextToSpeechStub(grpc.secure_channel(endpoint, grpc.ssl_channel_credentials()))
        request = tts_build_request(string)
        metadata = authorization_metadata(api_key, secret_key, "tinkoff.cloud.tts")
        responses = stub.StreamingSynthesize(request, metadata=metadata)
        for key, value in responses.initial_metadata():
            if key == "x-audio-num-samples":
                break
        for stream_response in responses:
            f.writeframes(stream_response.audio_chunk)

if __name__ == "__main__":
    pass
    # # Test:
    # result = stt_wav_to_string("wav_files/input.wav")
    # print(result)
    # tts_string_to_wav("Съешь же ещё этих мягких французских булочек, да выпей чаю", "wav_files/output.wav")
