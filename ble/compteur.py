#!/usr/bin/python
# -*- coding: latin-1 -*-
import threading
import time

#Classe permettant de créer un thread afin de décremmenter une variable chaque 15 seoondes
class TimerClass(threading.Thread):
    def __init__(self, cpt):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.count = cpt

    def run(self):
        while self.count < 5000 and not self.event.is_set():
            print self.count
            self.count += 1
            self.event.wait(15)

    def stop(self):
        self.event.set()
	return self.count
