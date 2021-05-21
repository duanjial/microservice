import urllib.request
import shutil
import os
import re
from pathlib import Path


def download_m3u8_file(url, file_name):
    if not os.path.exists('../downloadM3U8/tmp'):
        os.makedirs('../downloadM3U8/tmp')
    file = os.path.join('../downloadM3U8/tmp', file_name)
    with urllib.request.urlopen(url) as response, open(file, 'wb') as outFile:
        shutil.copyfileobj(response, outFile)


def download_mp4(file_name):
    if not os.path.exists('../downloadM3U8/videos'):
        os.makedirs('../downloadM3U8/videos')
    mp4_file = Path(f"./downloadM3U8/videos/{file_name[:-5]}.mp4")
    if mp4_file.is_file():
        print(f"{file_name[:-5]}.mp4 already exist!")
        return False
    else:
        os.system(
            f"ffmpeg -protocol_whitelist file,http,https,tcp,tls,crypto -loglevel quiet\
                 -i ./downloadM3U8/tmp/{file_name} -c copy ./downloadM3U8/videos/{file_name[:-5]}.mp4")
        return True


def add_home_url_to_m3u8_file(home_url, file_name):
    with open(os.path.join('../downloadM3U8/tmp', file_name), 'r') as file:
        lines = file.readlines()

    def add_prefix(line):
        if not line.startswith('#'):
            return home_url + line
        else:
            return line
    data = list(map(add_prefix, lines))
    with open(os.path.join('../downloadM3U8/tmp', file_name), 'w') as file:
        file.writelines(data)


def get_home_url(url, file_name):
    return url.replace(file_name, '')


class Downloader:
    @staticmethod
    def download(url):
        fileName = re.findall(r'\d+.m3u8', url)[0]
        homeUrl = get_home_url(url, fileName)
        download_m3u8_file(url, fileName)
        add_home_url_to_m3u8_file(homeUrl, fileName)
        return download_mp4(fileName)
