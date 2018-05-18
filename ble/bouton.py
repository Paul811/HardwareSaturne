#!/usr/bin/python
# -*- coding: latin-1 -*-
import threading
import time
import RPi.GPIO as GPIO


#Classe permettant de créer un thread afin de commander le diffuseur via un bouton poussoir
class Bouton(threading.Thread):
    #Fonction appelée lors de l'initialisation de l'objet 
    def __init__(self):
	#Initialisation des GPIO et du thread
        threading.Thread.__init__(self)
        self.event = threading.Event()
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(40, GPIO.OUT, initial=GPIO.HIGH)
	GPIO.setup(38, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(13, GPIO.OUT, initial=GPIO.LOW)
	lastValue = 0

    #Fonction appelée lors du lancement du thread (avec la fonction start)
    def run(self):
		#Tant que la fonction n'a pas été arrêté (via la fonction stop)
		while not self.event.is_set():
			#Selon l'état du diffuseur (allumé ou éteint), on allume ou éteint le diffuseur lorsque
			#le bouton est appuyé
			state = GPIO.input(13)
			GPIO.setmode(GPIO.BOARD)
			if GPIO.input(38) == 1  and lastValue == 0:
				lastValue = 1
				if state is  0:
					GPIO.setup(13, GPIO.OUT, initial=GPIO.HIGH)
        		        if state is 1:
        		        	GPIO.setup(13, GPIO.OUT, initial=GPIO.LOW)
			elif GPIO.input(38) == 0:
				lastValue = 0

    #Fonction appelé lors de l'arrêt de la fonction
    def stop(self):
        self.event.set()
