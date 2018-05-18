#!/usr/bin/python
# -*- coding: latin-1 -*-
import RPi.GPIO as GPIO
from bluetooth import *
from fonctions import *
from bouton import *
from compteur import *
import time
import sys
from subprocess import call

#Déclaration des variables
nomParfum=""
dureeDiffusion=0
intensiteDiffusion=0
progDiffusion=""
IDParfumActif=0
NomDiffuseur="Odyscent"
#On récupère le nom du parfum via la ligne de commande
nomParfum = str(sys.argv[1])
GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(38, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setmode(GPIO.BOARD)
btn = Bouton()
btn.start()

try:
	#Boucle infinie
	while True:
		#Connection bluetooth
		stateCapsule = False
		server_sock=BluetoothSocket(RFCOMM)
		server_sock.bind(("",PORT_ANY))
		server_sock.listen(1)
		port = server_sock.getsockname()[1]
		uuid = "7be1fcb3-5776-42fb-91fd-2ee7b5bbb86d"
		advertise_service( server_sock, "SampleServer",
		                   service_id = uuid,
		                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
		                   profiles = [ SERIAL_PORT_PROFILE ])
		
		print "Waiting for connection on RFCOMM channel %d" % port
	
		client_sock, client_info = server_sock.accept()
		print "Accepted connection from ", client_info
		cptDiff = 0
		try:
		     while True:
			#On récupère la donnée envoyé par le client
		        data = client_sock.recv(1024)
			#Si la donnée est vide, on ne fait rien
			#if (len(data) == 0): break
			#Si le client souhaite lancer le programme Zen
			if data : 
				if data == 'PlayZen': 
					#On envoie un signal à la sortie 13 de la RPI
					GPIO.setup(13, GPIO.OUT, initial=GPIO.HIGH)
					#On test si le parfum existe dans le fichier
					if isFragrance(nomParfum):
						#S'il existe, on récupère la valeur du compteur de parfum
						print "Parfum deja dans le fichier"
						cptDiff = int(getValueCpt(nomParfum))
						#Et on lance le compteur avec cette valeur
						compteur = TimerClass(cptDiff)
						compteur.start()
					#Si le parfum n'existe pas
					else:	
						#On écrit le parfum dans le fichier et on lance le compteur
						print "Ecriture parfum fichier"
						rightParfum(nomParfum)
						compteur = TimerClass("0")
						compteur.start()
				#Si l'utilisateur souhaite arrêter la diffusion du programme Zen
				if data == 'PauseZen':
					#On envoie un signal à la sortie 13 de la RPI
	        	                GPIO.setup(13, GPIO.OUT, initial=GPIO.LOW)
					#Puis on récupère la valeur du compteur et on l'écrit dans le fichier
					cptDiff = compteur.stop()
					print ("VALUE : ", cptDiff)
					if isFragrance(nomParfum):
						updateCpt(nomParfum, cptDiff)
					else:
						print "Error when writing in the file"		
				#Si l'utilisateur souhaite recevoir le nom du parfum
				if data == 'getNomParfum':
					#On envoie le nom du parfum
					print "Send NomParfum"
					client_sock.send(nomParfum)
				#Si l'utilisateur souhaite modifier le nom du diffuseur
				if  'setNameDiffuseur' in data:
					#On remplace dans le fichier le nom du diffuseur
					print "Set nom diffuseur"
					replace_line('nomDiffuseur.txt',0, data.split('setNameDiffuseur ',1)[1])
				#Si l'utilisateur souhaite recevoir l'état de la capsule
				if data == 'getStateCapsule':
					#On envoie l'état de la capsule
					print "Get state capsule"
					client_sock.send(str(cptDiff))
				if GPIO.input(38) == 1:
					print "OK"
				#else:
				#	GPIO.setup(22, GPIO.OUT, initial=GPIO.HIGH)
				#	time.sleep(.300)
				#	GPIO.setup(22, GPIO.OUT, initial=GPIO.LOW)
			        print "received [%s]" % data
		except IOError:
		    pass
		#Si la connection se coupe, on ferme la socket puis on relance la connection
		print "disconnected"
		try:
	 		compteur
		except NameError:
			print "Variable not defined"
		else:
	 		compteur.stop()
		client_sock.close()
		server_sock.close()
		GPIO.cleanup()
		print "all done"
		call(['./script.sh', nomParfum])
except KeyboardInterrupt:
	btn.stop()

