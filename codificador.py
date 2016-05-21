#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# "Esteganografía con ficheros de audio WAV"
# Archivo: codificador.py
# Autor: Christian Prieto Bustamante

import wave


jumpsData = 10 #Espacio de muestras del framerate para la toma de datos válidos
numFraData = 1 #El dato (1 byte) se compone de la lectura de 1 framerate
numFraCipher = 1 #Un framerate para configurar el cifrado
numFraElemHead = 1 #cada elemento de la cabecera (para saber si se trata de un archivo generado por nosotros) ocupa un framerate
numFraSize = 4 # 32bits para determinar cuantos bytes ocupa el fichero oculto

cipherPskEnable = 1
cipherDisable = 0

header = ["S", "Y", "L", "M"] # 1 byte por cada caracter (contra menos caracteres, más posibilidades de error por accidente)

#print ord(header[0])
#print ord(header[1])
#print ord(header[2])
#print ord(header[3])
#exit(0)

#
# COMPOSICIÓN DE LA TRAMA DE DATOS:
#
#  (CABECERA)->(CIFRADO)->(TAMAÑO ARCHIVO)->(BYTES ARCHIVO)
#

# DATOS DEL USUARIO:
pathFileToHide = "calico.jpg"
pathFileWav = "audioBase3.wav"
pathFileWavResult = "estego.wav"

# inicializamos a 0 el tamaño de bytes de los ficheros para tratamiento de errores:
# El del fichero a ocultar es el tamaño total de bytes que ocupa en disco. El de el fichero .wav
# donde lo vamos a ocultar el tamaño se refiere a los bytes totales del samplerate del octeto 
# menos significativo de cada canal
sizeFileToHide = 0 
sizeFileWav = 0


#TRATANDO CON LOS FICHEROS:

# FICHERO BASE WAV DONDE LO VAMOS A OCULTAR
fileWav = wave.open(pathFileWav,'rb')
bytesfileWav = bytearray(fileWav.readframes(fileWav.getnframes()))


channels = fileWav.getnchannels() # canales de audio
sampleWidth = fileWav.getsampwidth() # número de bytes para las muestras del samplerate
frameRate = fileWav.getframerate()
numTotalFrames = fileWav.getnframes()

bytesMaximos = ((numTotalFrames / sampleWidth) / jumpsData) - len(header) - 1 # el -1 es para evitar Bytes huérfanos

print "Número de canales: ",channels
print "Ancho de muestra del sample (bytes): ",sampleWidth
print "Número de frames totales: ", numTotalFrames
print "Capacidad máxima de almacenado: ", bytesMaximos, "Bytes (",float(bytesMaximos / 1024), "KBytes )"



# FICHERO QUE QUEREMOS OCULTAR
try:
	fileToHide = open(pathFileToHide,'rb')
except:
	print "ERROR: problema con fichero de audio y/o incompatible"
	exit(1)
	
bytesFileToHide = bytearray(fileToHide.read())

if len(bytesFileToHide) < bytesMaximos:
	print "El archivo a ocultar ocupa: ", len(bytesFileToHide), "Bytes (OK!)"
else:
	print "ERROR: El fichero que desea ocultar es demasiado grande"
	exit(0)


startIn = 0
indexHeader = 0
indexFileToHide = 0
indexSampleWav = startIn

while indexHeader < len(header):
	bytesfileWav[indexSampleWav] = header[indexHeader]
	indexHeader += 1
	indexSampleWav += (sampleWidth * jumpsData)
	
bytesfileWav[indexSampleWav] = cipherDisable
indexSampleWav += (sampleWidth * jumpsData)

desplazamiento = 0
for i in range(numFraSize):
	
	#print bytes(len(bytesFileToHide)>>24 & 0xFF) , bytes(len(bytesFileToHide)>>16 & 0xFF) , bytes(len(bytesFileToHide)>>8 & 0xFF) , bytes(len(bytesFileToHide)>>0 & 0xFF)
	bytesfileWav[indexSampleWav] = len(bytesFileToHide)>>desplazamiento & 0xFF
	desplazamiento += 8
	indexSampleWav += (sampleWidth * jumpsData)



while indexFileToHide < len(bytesFileToHide):
	bytesfileWav[indexSampleWav] = bytesFileToHide[indexFileToHide]
	indexSampleWav += (sampleWidth * jumpsData)
	indexFileToHide += 1




# GRABAMOS EL FICHERO DE AUDIO RESULTANTE:
outEstegoWAV = wave.open(pathFileWavResult, "wb") 
outEstegoWAV.setnchannels(channels) 
outEstegoWAV.setsampwidth(sampleWidth) 
outEstegoWAV.setframerate(frameRate) 
outEstegoWAV.writeframes(bytesfileWav) 
outEstegoWAV.close() 









