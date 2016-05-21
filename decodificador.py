#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# "Esteganografía con ficheros de audio WAV"
# Archivo: decodificador.py
# Autor: Christian Prieto Bustamante

import wave


jumpsData = 10 #Espacio de muestras del framerate para la toma de datos válidos
numFraData = 1 #El dato (1 byte) se compone de la lectura de 1 framerate
numFraCipher = 1 #Un framerate para configurar el cifrado
numFraElemHead = 1 #cada elemento de la cabecera (para saber si se trata de un archivo generado por nosotros) ocupa un framerate
numFraSize = 4 # 32bits para determinar cuantos bytes ocupa el fichero oculto

# Constantes de cifrado
cipherPskEnable = 1
cipherDisable = 0

header = ["S", "Y", "L", "M"] # 1 byte por cada caracter (tiene que coincidir con la cabecera con la que se ocultó el contenido)


# DATOS DEL USUARIO:
pathFileWav = "estego.wav"
pathFileResultado = "resultado"


sizeFileToHide = 0 
sizeFileWav = 0


# Abrimos el archivo WAV que oculta algo
fileAudioBase = wave.open(pathFileWav,'rb')
bytesFileAudioBase = bytearray(fileAudioBase.readframes(fileAudioBase.getnframes()))

channels = fileAudioBase.getnchannels() # canales de audio
sampleWidth = fileAudioBase.getsampwidth() # número de bytes para las muestras del samplerate
frameRate = fileAudioBase.getframerate()
numTotalFrames = fileAudioBase.getnframes()



startIn = 0
indexHeader = 0
indexSampleWav = startIn
saltos = (sampleWidth * jumpsData)
bytesFileOculto = []
indexFileOculto = 0

error = 0

# Leemos cabecera:
for i in range(len(header)):
	
	#bytesFileOculto.append(bytesFileAudioBase[indexSampleWav])
	#indexFileOculto += 1
	print header[i], chr(bytesFileAudioBase[indexSampleWav])
	if header[i] != chr(bytesFileAudioBase[indexSampleWav]):
		error = 1
		print "Cabecera no válida"
		exit(error)
	indexSampleWav += saltos


print "Cabecera válida (OK!)"

# Leemos el tipo de cifrado que utilizará el fichero resultante:
typeCipher = bytesFileAudioBase[indexSampleWav]
indexSampleWav += saltos


listTamanio = []
# Leemos los bytes que determinan el tamaño en bytes del fichero:
for i in range(numFraSize):
	listTamanio.append(bytesFileAudioBase[indexSampleWav])
	indexSampleWav += saltos

print "Bytes tamaño fichero oculto: ", listTamanio
listTamanio.reverse()
print "Bytes tamaño reordenados: ", listTamanio

desplazamiento = 0
tamanio = bin(0 & 0xFF)[2:]
for i in range(numFraSize):
	print tamanio
	tamanio += bin(listTamanio[i] & 0xFF)[2:]
	desplazamiento += 8

sizeFileHidden = int(tamanio, 2)
print sizeFileHidden

bytesFileOculto = []
indexDataHidden = 0
while indexDataHidden < sizeFileHidden:
	bytesFileOculto.append(bytesFileAudioBase[indexSampleWav])
	indexSampleWav += saltos
	indexDataHidden += 1
	
	
ficheroRecuperado = open("recuperado", 'wb')
newFileByteArray = bytearray(bytesFileOculto)
ficheroRecuperado.write(newFileByteArray)
ficheroRecuperado.close()
	
	
