#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# "Esteganografía con ficheros de audio WAV"
# Archivo: codificador.py
# Autor: Christian Prieto Bustamante

import wave
import gnupg

# constantes cifrado
CIPHER_ON = 1 # cifrado activo
CIPHER_OFF = 0 # cifrado inactivo

# variables modificables a gusto
jumpsData = 10 #Espacio de muestras del framerate para la toma de datos válidos
numFraSize = 4 # 32bits para determinar cuantos bytes ocupa el fichero oculto
cipher = CIPHER_ON # establecemos si se va a cifrar o no
header = ["S", "Y", "L", "M"] # 1 byte por cada caracter (contra menos caracteres, más posibilidades de error por accidente)
passphrase_cipher = "clavedecifrado" # clave de cifrado en caso de haberlo activado

# DATOS DE LOS FICHEROS NECESARIOS:
pathFileToHide = "calico.jpg" # archivo que queremos ocultar
pathFileToHideCipher = pathFileToHide + ".cipher"
pathFileWav = "audioBase3.wav" # fichero de audio base que se utilizará para ocultar la información
pathFileWavResult = "estego.wav" # nombre de fichero de salida (el que ocultará el contenido)



#
# COMPOSICIÓN DE LA TRAMA DE DATOS OCULTOS:
#
#  (CABECERA)->(CIFRADO)->(TAMAÑO ARCHIVO)->(BYTES ARCHIVO)
#



#TRATANDO CON LOS FICHEROS:

# FICHERO BASE WAV DONDE LO VAMOS A OCULTAR
fileWav = wave.open(pathFileWav,'rb')
bytesfileWav = bytearray(fileWav.readframes(fileWav.getnframes())) # guardamos los bytes (del muestreo) en un array de bytes


channels = fileWav.getnchannels() # canales de audio (1 mono, 2 stereo)
sampleWidth = fileWav.getsampwidth() # número de bytes para las muestras del samplerate
frameRate = fileWav.getframerate() # obtenemos el número de muestras (frames) por segundo que realiza
numTotalFrames = fileWav.getnframes() # obtenemos el número total de muestras disponibles (frames)

# calculamos el número total de bytes que se puede almacenar:
bytesMaximos = ((numTotalFrames / sampleWidth) / jumpsData) - len(header) - 1 # el -1 es para evitar Bytes huérfanos


# mostramos la información por pantalla:
print "Número de canales: ",channels
print "Ancho de muestra del sample (bytes): ",sampleWidth
print "Número de frames totales: ", numTotalFrames
print "Capacidad máxima de almacenado: ", bytesMaximos, "Bytes (",float(bytesMaximos / 1024), "KBytes )"



# FICHERO QUE QUEREMOS OCULTAR
try:
	fileToHide = open(pathFileToHide,'rb')
except:
	print "ERROR: problema con fichero"
	exit(1)



# Si el cifrado está activo, lo ciframos (nos guardamos también el fichero cifrado original)
if cipher == CIPHER_ON:
	
	gpg_home = "gnupg"
	gpg = gnupg.GPG(gnupghome=gpg_home)
	encrypted_ascii_data = gpg.encrypt_file(fileToHide, None, passphrase=passphrase_cipher, symmetric=True, output=pathFileToHideCipher)
	#fileToHide.close()
	
	fileToHideEncripted = open(pathFileToHideCipher, 'rb')
	bytesFileToHide = bytearray(fileToHideEncripted.read()) # guardamos todos los bytes del archivo en un array
	#fileToHideEncripted.close()

else:
	
	bytesFileToHide = bytearray(fileToHide.read()) # guardamos todos los bytes del archivo en un array
	#fileToHide.close()



# comprobamos que el archivo de audio tenga capacidad para esconder el fichero:
if len(bytesFileToHide) < bytesMaximos:
	print "El archivo a ocultar ocupa: ", len(bytesFileToHide), "Bytes (OK!)"
else:
	print "ERROR: El fichero que desea ocultar es demasiado grande"
	exit(1)



startIn = 0 # byte del sample de audio donde se empieza a contar
# A tener en cuenta:
#
#  bytem = byte menos significativo
#  byteM = byte más significativo
#
# si se un sistema estereo el muestreo comienza así -> bytem_ch1 - byteM_ch1 - bytem_ch2 - byteM_ch2 .....
# si se un sistema mono el muestreo comienza así -> bytem_ch1 - byteM_ch1 - bytem_ch1 - byteM_ch1 .....
#
# ----------------


indexHeader = 0
indexFileToHide = 0
indexSampleWav = startIn
jump = (sampleWidth * jumpsData)  # salto para grabar en los bytes correctos

# grabamos la cabecera
while indexHeader < len(header):
	bytesfileWav[indexSampleWav] = header[indexHeader]
	indexHeader += 1
	indexSampleWav += jump
	
# grabamos el valor de cifrado
bytesfileWav[indexSampleWav] = cipher
indexSampleWav += jump


# grabamos el tamaño bytes que ocupa el fichero oculto en los bytes asignados para ello
# utilizamos desplazamiento de bits para guardarlo en bloques de un octeto (byte) y luego poder recomponerlo
desplazamiento = 0
for i in range(numFraSize):
	
	#print bytes(len(bytesFileToHide)>>24 & 0xFF) , bytes(len(bytesFileToHide)>>16 & 0xFF) , bytes(len(bytesFileToHide)>>8 & 0xFF) , bytes(len(bytesFileToHide)>>0 & 0xFF)
	bytesfileWav[indexSampleWav] = len(bytesFileToHide)>>desplazamiento & 0xFF
	desplazamiento += 8
	indexSampleWav += jump


# grabamos los bytes del archivo oculto en el audio
while indexFileToHide < len(bytesFileToHide):
	bytesfileWav[indexSampleWav] = bytesFileToHide[indexFileToHide]
	indexSampleWav += jump
	indexFileToHide += 1

print indexFileToHide

# GRABAMOS EL FICHERO DE AUDIO RESULTANTE:
outEstegoWAV = wave.open(pathFileWavResult, "wb") 
outEstegoWAV.setnchannels(channels) 
outEstegoWAV.setsampwidth(sampleWidth) 
outEstegoWAV.setframerate(frameRate) 
outEstegoWAV.writeframes(bytesfileWav) 
outEstegoWAV.close() 









