#!/usr/bin/python
# -*- coding: latin-1 -*-
#Fonction permettant de lire dans le fichier afin de savoir si le nom du parfum existe déjà
def isFragrance(name):
	if name in open('listParfum.txt', 'rt').read():
		return True
	else:
		return False

#Fonction permettant de récupérer la valeur du compteur d'un parfum 
def getValueCpt(name):
	lineValue=-1
	if isFragrance(name):
		with open('listParfum.txt', 'r') as myFile:
			for num, line in enumerate(myFile, 1):
				if name in line:
					print 'found at line:', num
					lineValue=num
				if num == (lineValue + 1):
					print line	
					return line
			myFile.close()
	else:
		print "ERROR"

#Fonction permettant d'écrire le nom d'un parfum dans le fichier
def rightParfum(name):
	with open('listParfum.txt', 'a') as myFile:
		myFile.write(name)
		myFile.write('\n')
		myFile.write("0")
		myFile.close()

#Fonction permettant de mettre à jour dans le fichier le compteur d'un parfum 
def updateCpt(name, value):
	lineValue = -2
	if isFragrance(name):
		with open('listParfum.txt', 'a+') as myFile:
			for num, line in enumerate(myFile):
				if name in line:
					lineValue = num
				if num == (lineValue+1):
					replace_line('listParfum.txt', num, str(value))


#Fonction de remplacer la ligne d'un fichier par un texte
def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text + "\n"
    out = open(file_name, 'w')
    out.writelines(lines)
    #out.write("\n")
    out.close()
			
