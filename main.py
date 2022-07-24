import PyPDF2
from google.cloud import texttospeech_v1
import os
from glob import glob

# Add your 'GOOGLE_APPLICATION_CREDENTIALS' key path
# credential_path = "C:/Users/user/PycharmProjects/example.json"
credential_path = "KEY_PATH"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

# Add your pdf files in "pdf_files" folder
# mp3 file will be saved in "mp3_files" folder

file_path = "../TextToSpeech"
files = glob(f"{file_path}/pdf_files/*.pdf")
text = {}
for file in files:
    file_text = ""
    infile = open(file, 'rb')
    pdf_read = PyPDF2.PdfFileReader(infile)
    file_name = file.split('\\')[-1].replace('.pdf', '')
    page_num = pdf_read.numPages
    for num in range(0, page_num):
        page = pdf_read.getPage(num)
        file_text += page.extractText()
    text.update({file_name: file_text})

client = texttospeech_v1.TextToSpeechClient()

for key in text:
    synthesis_input = texttospeech_v1.SynthesisInput(text=text[key])

    voice = texttospeech_v1.VoiceSelectionParams(
        language_code='en-US',
        ssml_gender=texttospeech_v1.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech_v1.AudioConfig(
        audio_encoding=texttospeech_v1.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(f"{file_path}/mp3_files/{key}.mp3", "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{key}.mp3"')
