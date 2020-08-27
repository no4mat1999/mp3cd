# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import webbrowser
import sys
import argparse
import webbrowser

# apt install python-bs4

# update if necessary
MP3CLAN_URL = 'http://mp3clan.top/mp3/'
TEMPLATE_FILE = 'resources/template.txt'
FILENAME = 'resultados.html'

class MusicFile:
	song_name = ''
	download_url = ''

def generate_results(music_list):
	try:
		final_file = ''
		with open(TEMPLATE_FILE) as template:
			final_file = template.read()
		for element in music_list:
			final_file += '<p>' + str(element.song_name) + '</p>'
			final_file += '<audio controls><source src="' + str(element.download_url) + '"></audio>'
		final_file += '</article></body><html>'
		file = open(FILENAME, 'w')
		file.write(final_file)
		file.close()
		webbrowser.open(FILENAME)
	except Exception, e:
		print('Error generating ' + str(FILENAME))
		print e

def check_if_avalible(music_file):
	try:
		urllib2.urlopen(music_file.download_url)
		return True
	except urllib2.HTTPError, e:
		print(e.code)
	except urllib2.URLError, e:
		print(e.args)
	return False

def search(song_name):
	song_name = song_name.replace(' ', '_')
	music_list = []
	try:
		web_page = urllib2.urlopen(MP3CLAN_URL + song_name)
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
	except Exception, e:
		print('Problem searching music')
		print e
	return music_list

def start_process(args):
	print('Searching...')
	music_list = search(str(args.s))
	if args.c:
		print('Validating...')
		music_list_checked = []
		for element in music_list:
			if (check_if_avalible(element)):
				music_list_checked.append(element)
		music_list = music_list_checked
	print('Generating html...')
	generate_results(music_list)

def main():
	parser = argparse.ArgumentParser(description='Python mp3clan simple downloader')
	required_arguments = parser.add_argument_group('required arguments')
	required_arguments.add_argument('-s', '--search',
						action='store',
						required=True,
						dest='s',
						help='Search a song name')
	parser.add_argument('-c', '--check', action='store_true',
						dest='c',
						help='Enable validate file URL step')
	parser.add_argument('--version', action='version',
						version='%(prog)s 1.0')

	start_process(parser.parse_args())

main()
