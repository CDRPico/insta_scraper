from instaloader import Instaloader, Profile
from pydub import AudioSegment

import speech_recognition as sr
import os

def download_videos(username):
    l = Instaloader()
    profile = Profile.from_username(l.context, username)
    for post in profile.get_posts():
        filename=post.date_utc.strftime('%Y-%m-%d %H-%M-%S')
        if post.is_video:
            l.download_post(post, target=filename)
            print(f"Downloaded: {filename}.mp4")

def transcript_export_video(videoname_url):
    videoname = videoname_url.split('/')
    video = AudioSegment.from_file(videoname_url, format="mp4")
    audio = video.set_channels(1).set_frame_rate(16000).set_sample_width(2)
    audio.export(videoname[-1][:-3] + 'wav', format="wav")
    r = sr.Recognizer()
    with sr.AudioFile(videoname[-1][:-3] + 'wav') as source:
        audio_text = r.record(source)
    text = r.recognize_google(audio_text, language='es-CO')
    file_name = videoname[-1][:-3] + 'txt'
    with open(file_name, "w") as file:
        file.write(text)
    os.system(f"start {file_name}")