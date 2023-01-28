from gtts import gTTS
import os

text = "Ella is british, and a very smart person"

tts = gTTS(text=text, lang='en')

tts.save("filename.mp3")

os.system("filename.mp3")