#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# "Esteganografía con ficheros de audio WAV"
# Archivo: decodificador.py
# Autor: Christian Prieto Bustamante

import wave
import gnupg, os

# constantes cifrado
CIPHER_ON = 1 # cifrado activo
CIPHER_OFF = 0 # cifrado inactivo

# variables modificables a gusto
jumpsData = 10 #Espacio de muestras del framerate para la toma de datos válidos
numFraSize = 4 # 32bits para determinar cuantos bytes ocupa el fichero oculto
header = ["S", "Y", "L", "M"] # 1 byte por cada caracter (contra menos caracteres, más posibilidades de error por accidente)
passphrase_cipher = "clavedecifrado" # clave de cifrado en caso de haberlo activado


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
tamanio = ""
for i in range(numFraSize):
	#tamanio += bin(listTamanio[i] & 0xFF)[2:]
	listTamanio[i]>>desplazamiento
	tamanio += bin(listTamanio[i] & 0xFF)[2:].zfill(8)
	print "byte: ", bin(listTamanio[i])[2:].zfill(8)
	desplazamiento += 8

sizeFileHidden = int(tamanio, 2)
print "Bytes ocultos: ", sizeFileHidden


bytesFileOculto = []
indexDataHidden = 0
while indexDataHidden < sizeFileHidden:
	bytesFileOculto.append(bytesFileAudioBase[indexSampleWav])
	indexSampleWav += saltos
	indexDataHidden += 1

nameFileResult = "recuperado"
if typeCipher == CIPHER_ON:
	nameFileResult = "recuperado.cipher"
	
ficheroRecuperado = open(nameFileResult, 'wb')
newFileByteArray = bytearray(bytesFileOculto)
ficheroRecuperado.write(newFileByteArray)
ficheroRecuperado.close()

if typeCipher == CIPHER_ON:
	gpg = gnupg.GPG(gnupghome='gnupg')
	with open(nameFileResult, 'rb') as f:
		status = gpg.decrypt_file(f, passphrase=passphrase_cipher, output='resultado')

	print 'ok: ', status.ok
	print 'status: ', status.status
	print 'stderr: ', status.stderr
	
