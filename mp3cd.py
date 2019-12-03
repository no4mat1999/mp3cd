# -*- coding: utf-8 -*-
import urllib2
import sys
import webbrowser

url = "http://mp3clan.top/mp3/" #actualizar en caso de que mp3clan cambie de dominio
song_urls = []
song_names = []

def search(songname):
	print "Buscando..."
	songnameclean = songname.replace(" ","_")
	complete = False
	while complete==False:
		try:
			respuesta = urllib2.urlopen(url+songnameclean)
			linea = respuesta.readline()
			while linea!="":
				if linea.find('<li class="mp3list-play" id=')>=0:
					split_1 = linea.split("data-title=")
					temp = split_1[1].replace(">","")
					temp = temp.replace('"','')
					song_names.append(temp.strip())
					linea = respuesta.readline()
					linea = respuesta.readline()
					split_1 = linea.split('rel=')
					song_urls.append(split_1[0].strip()) 
				linea = respuesta.readline()
			finalhtml = '<html><head><meta charset="utf-8"><title>Resultados de: '+songname+'</title><link rel="stylesheet" type="text/css" href="resources/estilos.css" media="screen"></head><body><article><h1>Resultados de la búsqueda:</h1>'
			position = 0
			for element in song_names:
				finalhtml += "<p>" + str(position+1) + ". " + str(song_urls[position]) + ">" + str(song_names[position]) + "</a></p>"
				position += 1
			finalhtml += '</article></body><html>'
			file = open("resultados.html","w")
			file.write(finalhtml)
			file.close()
			if len(song_names)>0:
				print(str(len(song_names))+ " melodías encontradas. Abriendo navegador.")
				webbrowser.open('resultados.html')
			else:
				print(str(len(song_names))+ " melodías encontradas.")
			complete = True
		except Exception:
			print "Error en la conexión."
			complete = True


def main():
	try:
		search(sys.argv[1])
	except Exception:
		print "Faltan argumentos"

main()
