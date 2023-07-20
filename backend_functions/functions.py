import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import openai
import json 
import requests
import pygame
import textwrap
import asyncio
import requests, base64, random, argparse, time, re




def initialize():
    # set up the count
    count = 1


def generate_script(topic):
    """Takes a topic, two people and returns a script as a dict"""
    # engineering the prompt
    prompt = f"""Generate a discussion between Socrates and Nietzsche on the topic of {topic}. 
                 Socrates should always start the conversation, this is very important.
                 The script should only contain dialog lines in the form of a json array, 
                 where each message is an object of this form:
                 {{name: ..., message:...}}, where name is the last name of the person who says the line.
                 The discussion should be something that the two philosophers would actually say and have real depth. 
                 Take inspiration from their work and make them both sound real.
                 The discussion needs to be as realistic as possible.
                 Do NOT end the discussion with something about the importance of diversity.
                 They should also try to sometimes argue and not just agree on everything.
                 The JSON array should not end with a comma."""

    # generating the script as a JSON object
    print("Generating script ...")
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", #gpt-3.5-turbo
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    try:
        discussionDict = json.loads(str(completion['choices'][0]['message']['content']))
        return discussionDict
    except Exception as e:
        print("Error occured when parsing the response, the following response was generated:")
        print(str(completion['choices'][0]['message']['content']))
        print("Error: ", e)

def get_count(directory):
    count = 0
    for entry in os.scandir(directory):
        if entry.is_dir():
            count += 1
    return count

def save_script_and_audio(script, session_id):
    print("Saving script ...")
    # create directory for the script using an index and the topic name
    current_directory = "scripts"

    count = get_count(current_directory)
    
    directory_name = f"script_{count}"

    path = os.path.join(current_directory, directory_name)

    os.mkdir(path)

    file_path = os.path.join(path, "script.json")

    # create json file inside the directory and put the script inside
    with open(file_path, "w") as f:
        json.dump(script, f, indent=4)

    print("Generating audio ...")
    # create a folder inside the script folder containing the voice lines
    audio_path = os.path.join(path, "audio")
    os.mkdir(audio_path)
    for i in range(len(script)):
        filename = os.path.join(audio_path, f"audio_{i}.mp3")
        if (script[i]["name"]).lower() == "Socrates".lower():
            tts(session_id, "en_us_ghostface", script[i]["message"], filename, False)
        else:
            tts(session_id, "en_us_007", script[i]["message"], filename, False)
    return path


def format_script(script):
    # TODO: add color to each name
    max_name_length = max(len(obj['name']) for obj in script)
    for obj in script:
        name = prRed(obj['name'])
        message = obj['message']
        wrapped_message = textwrap.wrap(message, width=80 - max_name_length - 2)  # Subtract 2 for the colon and space
        print(f"{name:{max_name_length + (len(name) - len(obj['name']))}}: {wrapped_message[0]}")
        #print(name + (" " * max_name_length) + ":")
        for line in wrapped_message[1:]:
            print(" " * (max_name_length + 3) + line)

def format_line( line, max_name_length):
    name = prRed(line['name'])
    message = line['message']
    wrapped_message = textwrap.wrap(message, width=80 - max_name_length - 2)  # Subtract 2 for the colon and space
    print(f"{name:{max_name_length + (len(name) - len(line['name']))}}: {wrapped_message[0]}")
    for line in wrapped_message[1:]:
        print(" " * (max_name_length + 3) + line)

def prRed(skk): return "\033[91m {}\033[00m" .format(skk)
 
def prGreen(skk): return "\033[92m {}\033[00m" .format(skk)



# Tiktok TTS
def tts(session_id: str, text_speaker: str = "en_us_002", req_text: str = "TikTok Text To Speech", filename: str = 'voice.mp3', play: bool = False):

    req_text = req_text.replace("+", "plus")
    req_text = req_text.replace(" ", "+")
    req_text = req_text.replace("&", "and")

    headers = {
        'User-Agent': 'com.zhiliaoapp.musically/2022600030 (Linux; U; Android 7.1.2; es_ES; SM-G988N; Build/NRD90M;tt-ok/3.12.13.1)',
        'Cookie': f'sessionid={session_id}'
    }
    url = f"https://api16-normal-useast5.us.tiktokv.com/media/api/text/speech/invoke/?text_speaker={text_speaker}&req_text={req_text}&speaker_map_type=0&aid=1233"
    r = requests.post(url, headers = headers)

    if r.json()["message"] == "Couldn't load speech. Try again.":
        output_data = {"status": "Session ID is invalid", "status_code": 5}
        print(output_data)
        return output_data

    vstr = [r.json()["data"]["v_str"]][0]
    msg = [r.json()["message"]][0]
    scode = [r.json()["status_code"]][0]
    log = [r.json()["extra"]["log_id"]][0]
    
    dur = [r.json()["data"]["duration"]][0]
    spkr = [r.json()["data"]["speaker"]][0]

    b64d = base64.b64decode(vstr)

    with open(filename, "wb") as out:
        out.write(b64d)

    output_data = {
        "status": msg.capitalize(),
        "status_code": scode,
        "duration": dur,
        "speaker": spkr,
        "log": log
    }

    #print(output_data)

    if play is True:
        play_audio(filename)

    return output_data

def play_script(script_path):
    # get the script into json format
    script_file = os.path.join(script_path,'script.json')
    with open(script_file) as json_file:
        script = json.load(json_file)

    audio_path = os.path.join(script_path, 'audio')
    max_name_length = max(len(obj['name']) for obj in script)
    for i in range(len(script)):
        # print line
        format_line( script[i], max_name_length)
        # play the audio
        play_audio(os.path.join(audio_path, f"audio_{i}.mp3"))
        
def check_fix_audio(script_path):
    # checks the integrity of the audio files and fixes them in case of corrupted mp3 files
    # using the Tiktok TTS, there seems to be no workaround, it simply fails with particular inputs at times
    print("Checking audio integrity...")
    script_file = os.path.join(script_path,'script.json')
    with open(script_file) as json_file:
        script = json.load(json_file)

    pygame.mixer.init()
    audio_path = os.path.join(script_path, 'audio')
    for i in range(len(script)):
        filename = os.path.join(audio_path, f"audio_{i}.mp3")
        try:
            pygame.mixer.music.load(filename)
        except Exception as e:
            print(filename, "is corrupted.")




def play_audio(filename):
    if filename:
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

def stop_audio():
    pygame.mixer.music.stop()

""" voices = [
    # DISNEY VOICES
    'en_us_ghostface',            # Ghost Face
    'en_us_chewbacca',            # Chewbacca
    'en_us_c3po',                 # C3PO
    'en_us_stitch',               # Stitch
    'en_us_stormtrooper',         # Stormtrooper
    'en_us_rocket',               # Rocket

    # ENGLISH VOICES
    'en_au_001',                  # English AU - Female
    'en_au_002',                  # English AU - Male
    'en_uk_001',                  # English UK - Male 1
    'en_uk_003',                  # English UK - Male 2
    'en_us_001',                  # English US - Female (Int. 1)
    'en_us_002',                  # English US - Female (Int. 2)
    'en_us_006',                  # English US - Male 1
    'en_us_007',                  # English US - Male 2
    'en_us_009',                  # English US - Male 3
    'en_us_010',                  # English US - Male 4

    # EUROPE VOICES
    'fr_001',                     # French - Male 1
    'fr_002',                     # French - Male 2
    'de_001',                     # German - Female
    'de_002',                     # German - Male
    'es_002',                     # Spanish - Male

    # AMERICA VOICES
    'es_mx_002',                  # Spanish MX - Male
    'br_001',                     # Portuguese BR - Female 1
    'br_003',                     # Portuguese BR - Female 2
    'br_004',                     # Portuguese BR - Female 3
    'br_005',                     # Portuguese BR - Male

    # ASIA VOICES
    'id_001',                     # Indonesian - Female
    'jp_001',                     # Japanese - Female 1
    'jp_003',                     # Japanese - Female 2
    'jp_005',                     # Japanese - Female 3
    'jp_006',                     # Japanese - Male
    'kr_002',                     # Korean - Male 1
    'kr_003',                     # Korean - Female
    'kr_004',                     # Korean - Male 2

    # SINGING VOICES
    'en_female_f08_salut_damour'  # Alto
    'en_male_m03_lobby'           # Tenor
    'en_female_f08_warmy_breeze'  # Warmy Breeze
    'en_male_m03_sunshine_soon'   # Sunshine Soon

    # OTHER
    'en_male_narration'           # narrator
    'en_male_funny'               # wacky
    'en_female_emotional'         # peaceful
] """