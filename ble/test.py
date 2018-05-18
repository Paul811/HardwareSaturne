import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

while True:
	GPIO.setup(13, GPIO.OUT, initial=GPIO.LOW)
