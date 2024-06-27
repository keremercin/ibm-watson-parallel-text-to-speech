import concurrent.futures
import pandas as pd
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os
import re

# Function to clean folder names
def clean_folder_name(folder_name):
    folder_name = re.sub(r'[\\/*?:"<>|]', '', folder_name)
    folder_name = folder_name.replace('\n', '').strip()
    return folder_name

def text_to_speech(row):
    text1 = str(row[0])
    text2 = str(row[1])
    text3 = str(row[2])
    text4 = str(row[3])

    dir1 = clean_folder_name(str(row[0]))
    dir2 = clean_folder_name(str(row[1]))

    if not os.path.exists(dir1):
        os.mkdir(dir1)
    if not os.path.exists(os.path.join(dir1, dir2)):
        os.mkdir(os.path.join(dir1, dir2))

    audio_filename = f"{dir1}_{dir2}_{clean_folder_name(str(row[2]))}.mp3"

    with open(os.path.join(dir1, dir2, audio_filename), 'wb') as audio_file:
        res = tts.synthesize(f"<speak><prosody rate='0%'>{text1} {text2} {text3}<break time='1s'/>{text4}</prosody></speak>", accept='audio/mp3', voice='en-US_KevinV3Voice').get_result()
        audio_file.write(res.content)

# IBM Watson credentials
apikey = os.getenv('IBM_WATSON_API_KEY')
url = os.getenv('IBM_WATSON_URL')

# Setup service
authenticator = IAMAuthenticator(apikey)
tts = TextToSpeechV1(authenticator=authenticator)
tts.set_service_url(url)

# Read the Excel file
file_path = "path/to/your/excel/file.xlsx"
df = pd.read_excel(file_path)

executor = concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count())
futures = [executor.submit(text_to_speech, row) for _, row in df.iterrows()]

concurrent.futures.wait(futures)
