# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from clint.textui import progress
from os import system, name
import requests
import argparse

# update if necessary
MP3CLAN_URL_BASE = 'http://mp3clan.mobi/mp3/'
MP3CLAN_URL = 'http://mp3clan.mobi/mp3_source.php'


class MusicFile:
    song_name = ''
    download_url = ''


def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


def download(music_file):
    try:
        print('- Download ' + music_file.song_name)
        web_session = requests.Session()
        web_session.get(MP3CLAN_URL_BASE)
        print('- Session started! Getting file URL, please wait')
        resp = web_session.get(music_file.download_url)
        real_url_file = resp.url
        print('- File URL: ' + real_url_file)
        print('- Downloading...')
        file = requests.get(real_url_file, allow_redirects=True, stream=True)
        with open(music_file.song_name + '.mp3', 'wb') as f:
            total_length = int(file.headers.get('content-length'))
            for chunk in progress.bar(file.iter_content(chunk_size=1024), expected_size=(total_length / 1024) + 1):
                if chunk:
                    f.write(chunk)
                    f.flush()
        web_session.close()
        print('- Done!')
    except Exception as e:
        print(e)


def search(song_name):
    # song_name = song_name.replace(' ', '_')
    song_name = song_name.replace(' ', '+')
    music_list = []
    try:
        # web_page = requests.get(MP3CLAN_URL + song_name) //Old method
        options = {'page': 0, 'ser': song_name}
        web_page = requests.post(MP3CLAN_URL, options)
        soup = BeautifulSoup(web_page.text, "html.parser")
        mp3clan_list = soup.find_all("li", {"class": "mp3list-play"})
        # remove first element because it's not a song
        mp3clan_list.pop(0)
        for element in mp3clan_list:
            soup = BeautifulSoup(str(element), "lxml")
            music_file = MusicFile()
            music_file.song_name = (soup.find("div")).attrs.get('title')
            music_file.download_url = (soup.find("a")).attrs.get('href')
            music_list.append(music_file)
    except Exception as e:
        print('Problem searching music')
        print(e)
    return music_list


def start_process(args):
    print('Searching...')
    music_list = search(str(args.s))
    if len(music_list) == 0:
        print('Not found')
        exit()
    clear()
    count = 1
    for element in music_list:
        print(str(count) + ' - ' + element.song_name)
        count += 1
    select = -1
    while select < 1 or select > len(music_list):
        select = int(input('> '))
    clear()
    download(music_list[select - 1])


def main():
    parser = argparse.ArgumentParser(description='Python mp3clan simple downloader')
    required_arguments = parser.add_argument_group('required arguments')
    required_arguments.add_argument('-s', '--search',
                                    action='store',
                                    required=True,
                                    dest='s',
                                    help='Search a song name')
    parser.add_argument('--version', action='version',
                        version='%(prog)s 1.1')

    start_process(parser.parse_args())


main()
