import pytube
import sys
import os
import ffmpeg  # download audio only
import unicodedata
import re

VIDEO_OUTPUT = "C:\видео\скачанные видео аудио"
MUSIC_OUTPUT = "C:\видео\музыка"
AUDIO_OUTPUT = "C:\видео\Звуковые эффекты"


def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value)
    return value


def download_using_ffmpeg(stream, title, output_path):
    yt.streams.filter(progressive=False, type="audio").order_by('abr').desc().first().download(
        filename="audio.mp3"
    )
    audio = ffmpeg.input("audio.mp3")  # download video only

    # video_stream = yt.streams.filter(res="1080p", progressive=False).first()
    stream.download(filename="video.mp4")

    video = ffmpeg.input("video.mp4")
    print(title)
    ffmpeg.output(audio, video, output_path + "\\" + title + ".mp4").run(overwrite_output=True)
    os.remove("video.mp4")
    os.remove("audio.mp3")
    return output_path + "\\" + title + ".mp4"


def download_video(yt, title, output_path):
    stream = yt.streams.filter(res="1080p", progressive=False).first()
    if stream is not None:
        print("Found 1080p option, downloading using FFMPEG...")
        path = download_using_ffmpeg(stream, title, output_path)
    else:
        print("Cant download 1080p video, downloading 720p instead...")
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by(
            'resolution').desc().first()
        path = stream.download(output_path=output_path, filename=title+".mp4")
    return path, stream


if __name__ == '__main__':
    link = sys.argv[1]
    output_parameter = None
    if len(sys.argv)>2:
        output_parameter = sys.argv[2]
    yt = pytube.YouTube(link)
    print("Start downloading...")
    title = slugify(yt.title, True)
    match output_parameter:
        case "-v":
            output_path = VIDEO_OUTPUT
            print("Downloading video to " + output_path)
            path, stream = download_video(yt, title, output_path)
        case "-m":
            output_path = MUSIC_OUTPUT
            print("Downloading music to " + output_path)
            stream = yt.streams.filter(progressive=False, type="audio").order_by('abr').desc().first()
            path = stream.download(output_path=output_path, filename=title+".mp3")
        case "-a":
            output_path = AUDIO_OUTPUT
            print("Downloading audio to " + output_path)
            stream = yt.streams.filter(progressive=False, type="audio").order_by('abr').desc().first()
            path = stream.download(output_path=output_path, filename=title+".mp3")
        case _:
            output_path = VIDEO_OUTPUT
            print("Downloading video to " + output_path)
            path, stream = download_video(yt, title, output_path)
    print("Download finished")
    print(path)
    print("Title:",stream.title,"| Resolution:",stream.resolution,"| Average bitrate:",stream.abr)

# print(yt.streams)
