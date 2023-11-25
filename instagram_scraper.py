from instaloader import Instaloader, Profile
from pydub import AudioSegment

import speech_recognition as sr
import shutil
import os
import whisper

def download_videos(username):
    l = Instaloader()
    profile = Profile.from_username(l.context, username)
    for post in profile.get_posts():
        filename=username + '_' + post.date_utc.strftime('%Y%m%d_%H%M%S')
        if post.is_video:
            l.download_post(post, target=filename)
            print(f"Downloaded: {filename}.mp4")

def video_to_audio(videoname_url):
    videoname = videoname_url.split('/')
    try:
        video = AudioSegment.from_file(videoname_url, format="mp4")
        audio = video.set_channels(1).set_frame_rate(16000).set_sample_width(2)
        wav_name = "/".join(videoname[:-1]) + '/' + videoname[-1][:-3] + 'wav'
        audio.export(wav_name, format="wav")
    except Exception as e:
        print(e)

def move_mp4_files(src_folder, dst_folder):
    # Iterate over all the directories in the source folder
    for root, dirs, files in os.walk(src_folder):
        for file in files:
            if file.endswith(".mp4"):
                src_path = os.path.join(root, file)
                dst_path = os.path.join(dst_folder, file)
                # Move the file to the destination folder
                shutil.move(src_path, dst_path)
                break  # Remove this line if you want to process all MP4 files in each subfolder

source_folder = "/mnt/c/Users/Mi/My Documents/python_projects/insta_scraper/mispropiasfinanzas"  # Replace with the path to your source folder
destination_folder = "/mnt/c/Users/Mi/My Documents/python_projects/insta_scraper/mispropiasfinanzas"  # Replace with the path to your main folder

move_mp4_files(source_folder, destination_folder)

def find_mp4_files(folder_path):
    mp4_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".wav"):
                mp4_files.append(os.path.join(root, file))
    return mp4_files

source_folder = "/mnt/c/Users/Mi/My Documents/python_projects/insta_scraper"

def transcript_audios(source_folder, username):
    mp4_files_list = find_mp4_files(source_folder)
    model = whisper.load_model("large-v2")
    for file in mp4_files_list:
        audioname = file.split('/')
        file_name = "/".join(audioname[:-1]) + '/' + username + "_" + audioname[-1][:-3] + 'txt'
        print(file_name)
        result = model.transcribe(file)
        text = result["text"]
        with open(file_name, "w") as file:
            file.write(text)
        os.system(f"start {file_name}")
        