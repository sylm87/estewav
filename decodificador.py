#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# "Esteganografía con ficheros de audio WAV"
# Autor: Christian Prieto Bustamante

import wave

# FICHERO BASE WAV DONDE LO VAMOS A OCULTAR
audioBase = "estego.wav"
fileAudioBase = wave.open(audioBase,'rb')
bytesFileAudioBase = bytearray(fileAudioBase.readframes(fileAudioBase.getnframes()))
print len(bytesFileAudioBase) / 4 #2 canales de 16 bits cada unos (por eso se divide entre 4 para compararlo con en num de frames)
print fileAudioBase.getnframes()

print fileAudioBase.getsampwidth() # bytes del tamaño del sample

inicioLectura = 0
saltos=1
if fileAudioBase.getsampwidth() == 2:
	inicioLectura = 0
	saltos = 2

bytesFileOculto = []
	
indexFileOculto = 0
indexAudioBase = inicioLectura
while indexFileOculto < 55952:
	bytesFileOculto.append(bytesFileAudioBase[indexAudioBase])
	indexAudioBase += saltos
	indexFileOculto += 1
	
print len(bytesFileOculto)
ficheroRecuperado = open("recuperado", 'wb')
newFileByteArray = bytearray(bytesFileOculto)
ficheroRecuperado.write(newFileByteArray)
ficheroRecuperado.close()
	
	
