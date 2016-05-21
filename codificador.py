#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# "Esteganografía con ficheros de audio WAV"
# Autor: Christian Prieto Bustamante

import wave


jumpsData = 20 #Espacio de muestras del framerate para la toma de datos válidos

numFraData = 2 #El dato (1 byte) se compone de la lectura de 2 tomas del framerate
numFraCipher = 1 
numFraElemHead = 1

bitsCipherEnable = b"00000001"

numBitsData = [5, 4] #se toman 5 bits de datos en la primera muestra y 4 bits en la segunda 
#(el bit sobrante del octeto byte es para control (es el más significativo), y el resto de 
#bits son los menos significantes del dato, para que no afecte negativamente al audio)

bitsDatoControl = [b"10000", b"0000"] #en decimal 256 (b"100000000")

cabeceraInicio = ["S", "Y", "L", "M"] # 1 byte por cada caracter

repControlFinal = 4 # número de veces que se tiene que repetir los bits de control para finalizar la lectura


#TRATANDO CON LOS FICHEROS:

# FICHERO QUE QUEREMOS OCULTAR
ocultar = "calico.jpg"
fileOcultar = open(ocultar,'rb')
bytesFileOcultar = bytearray(fileOcultar.read())
print int(bytesFileOcultar[1])


# FICHERO BASE WAV DONDE LO VAMOS A OCULTAR
audioBase = "audioBase1.wav"
fileAudioBase = wave.open(audioBase,'rb')
bytesFileAudioBase = bytearray(fileAudioBase.readframes(fileAudioBase.getnframes()))

print "bytes fichero a ocultar:"
print len(bytesFileOcultar)
print len(bytesFileAudioBase) / 4 #2 canales de 16 bits cada unos (por eso se divide entre 4 para compararlo con en num de frames)
print fileAudioBase.getnframes()

print fileAudioBase.getsampwidth() # bytes del tamaño del sample

inicioLectura = 0
saltos=1
if fileAudioBase.getsampwidth() == 2:
	inicioLectura = 0
	saltos = 2


for i in range(4):
	print bytesFileAudioBase[i]
	
indexFileOculto = 0
indexAudioBase = inicioLectura
while indexFileOculto < len(bytesFileOcultar):
	bytesFileAudioBase[indexAudioBase] = bytesFileOcultar[indexFileOculto]
	indexAudioBase += saltos
	indexFileOculto += 1


# GRABAMOS EL FICHERO DE AUDIO RESULTANTE:
salidaEstegoWAV = wave.open("estego.wav", "wb") 
salidaEstegoWAV.setnchannels(2) 
salidaEstegoWAV.setsampwidth(16 / 8) 
salidaEstegoWAV.setframerate(11025) 
salidaEstegoWAV.writeframes(bytesFileAudioBase) 
salidaEstegoWAV.close() 









