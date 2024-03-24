"""
Script to convert audio to text.

Uses the Wav2Vec2 model from Hugging Face.
"""
from transformers import Wav2Vec2Tokenizer, Wav2Vec2ForCTC
import torch
import librosa
from dotenv import load_dotenv
import os
import openai

tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

def transcribe_wav2vec(audio_path: str) -> str:
    """
    A function to convert a single audio file to text using the Wav2Vec2 model.

    Args:
        audio_path (str): The path to the audio file.

    Returns:
        str: The transcribed text.
    """
    input_audio, _ = librosa.load(audio_path, sr=16000)
    input_values = tokenizer(input_audio, return_tensors="pt", padding="longest").input_values

    with torch.no_grad():
        logits = model(input_values).logits
        predicted_ids = torch.argmax(logits, dim=-1)

    transcription = tokenizer.batch_decode(predicted_ids)[0]

    return transcription

def transcribe_whisper(audio_path: str, api_key: str) -> str:
    client = openai.OpenAI()
    file = open(audio_path, "rb")

    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=file
    )
    return transcription.text
    

if __name__ == "__main__":
    audio_path = "output.wav"
    # transcription = transcribe_wav2vec(audio_path)
    # print(f"Transcription: {transcription}")

    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = api_key
    transcription = transcribe_whisper(audio_path, api_key)
    print(f"Transcription: {transcription}")