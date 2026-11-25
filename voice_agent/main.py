from dotenv import load_dotenv
load_dotenv()
import asyncio
import os
import speech_recognition as sr
from openai import AsyncOpenAI 
from openai.helpers.audio import LocalAudioPlayer
from openai import OpenAI

client = OpenAI(
    api_key = os.getenv("GEMINI_API_KEY"),
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
)

async_client = AsyncOpenAI(
    api_key = os.getenv("GEMINI_API_KEY"),
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
)


async def tts(speech: str):
    async with async_client.audio.speech.with_streaming_response.create(
        model="gemini-2.5-t",
        voice="alloy",
        input=speech,
        instructions="You are a helpful assistant that speaks in a friendly and engaging manner.",
        response_format="pcm",
    ) as response:
        await LocalAudioPlayer().play(response)

SYSTEM_PROMPT = """ 
    You are a expert voice agent. You are given the transcript of what user has said using voice.
    you need to output as if you are an voice agent and hatever you speak will be converted back to audio using AI and played back to user
"""

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
]
            
def main():
    r = sr.Recognizer() # speech to text
    
    with sr.Microphone() as source: # mic access
        print("Listening...")
        r.adjust_for_ambient_noise(source) # adjust for ambient noise
        r.pause_threshold = 2 # set pause threshold
        
        while True:
            audio = r.listen(source) # listen to audio
            
            print("Processing audio...")
            stt = r.recognize_google(audio) # convert audio to text
            print("You said:", stt)
            
            messages.append({"role": "user", "content": stt})
            
            response = client.chat.completions.create(
                model = "gemini-2.5-flash",
                messages = messages
            )
            
            print("Voice Agent Response:", response.choices[0].message.content)
            asyncio.run(tts(response.choices[0].message.content)) # convert text to speech and play audio
            
main()