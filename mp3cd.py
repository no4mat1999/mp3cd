# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from clint.textui import progress
from urllib import request
from os import system, name
import requests
import webbrowser
import sys
import argparse

# update if necessary
MP3CLAN_URL = 'http://mp3clan.top/mp3/'

class MusicFile:
	song_name = ''
	download_url = ''

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def download(music_file):
	try:
		print(bcolors.HEADER + '- Download ' + bcolors.WARNING + music_file.song_name + bcolors.HEADER)
		web_session = requests.Session()
		web_session.get(MP3CLAN_URL)
		print('- Session started! Getting file URL, please wait')
		resp = web_session.get(music_file.download_url)
		real_url_file = resp.url
		print('- File URL: ' + bcolors.WARNING + real_url_file)
		print(bcolors.HEADER + '- Downloading...')
		file = requests.get(real_url_file, allow_redirects=True, stream=True)
		with open(music_file.song_name+'.mp3', 'wb') as f:
			total_length = int(file.headers.get('content-length'))
			for chunk in progress.bar(file.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
				if chunk:
					f.write(chunk)
					f.flush
		web_session.close()
		print(bcolors.HEADER + '- Done!')
	except Exception as e:
		print(e)

def search(song_name):
	song_name = song_name.replace(' ', '_')
	music_list = []
	try:
		web_page = request.urlopen(MP3CLAN_URL + song_name)
		soup = BeautifulSoup(web_page.read().decode("utf-8"), "html.parser")
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
	print(bcolors.HEADER + 'Searching...')
	music_list = search(str(args.s))
	if(len(music_list)==0):
		print('Not found')
		exit()
	clear()
	count = 1
	for element in music_list:
		print(bcolors.OKBLUE + str(count) + bcolors.HEADER  + ' - ' + element.song_name)
		count += 1
	select = -1
	while (select < 1 or select > len(music_list)):
		select = int(input(bcolors.OKBLUE + '> '))
	clear()
	download(music_list[select-1])

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
