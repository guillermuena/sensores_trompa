# Importamos la paquteria necesaria

import RPi.GPIO as GPIO
import time

TRIG1 = 4 #Variable que contiene el GPIO al cual conectamos la señal TRIG del sensor
TRIG2 = 17
TRIG3 = 27
TRIG4 = 22
ECHO1 = 18 #Variable que contiene el GPIO al cual conectamos la señal ECHO del sensor
ECHO2 = 23
ECHO3 = 24
ECHO4 = 25

# Distancias minimas en cm
dist_min_lat=500
dist_min_fron=40
alto=0 #0=distancia mayor a la minima - 1=distancia menor a la minima


GPIO.setmode(GPIO.BCM)     #Establecemos el modo según el cual nos refiriremos a los GPIO de nuestra RPi
GPIO.setup(TRIG1, GPIO.OUT) #Configuramos el pin TRIG como una salida
GPIO.setup(TRIG2, GPIO.OUT)
GPIO.setup(TRIG3, GPIO.OUT)
GPIO.setup(TRIG4, GPIO.OUT)
GPIO.setup(ECHO1, GPIO.IN)  #Configuramos el pin ECHO como una entrada
GPIO.setup(ECHO2, GPIO.IN)
GPIO.setup(ECHO3, GPIO.IN)
GPIO.setup(ECHO4, GPIO.IN)

#Contenemos el código principal en un estructura try para limpiar los GPIO al terminar o presentarse un error
try:
    #Implementamos un loop infinito
	while True:

        # Ponemos en bajo el pin TRIG y después esperamos 0.5 seg para que el transductor se estabilice
		GPIO.output(TRIG1, GPIO.LOW)
		GPIO.output(TRIG2, GPIO.LOW)
		GPIO.output(TRIG3, GPIO.LOW)
		GPIO.output(TRIG4, GPIO.LOW)
		time.sleep(0.5)

        #Ponemos en alto el pin TRIG esperamos 10 uS antes de ponerlo en bajo
		GPIO.output(TRIG1, GPIO.HIGH)
		GPIO.output(TRIG2, GPIO.HIGH)
		GPIO.output(TRIG3, GPIO.HIGH)
		GPIO.output(TRIG4, GPIO.HIGH)
		time.sleep(0.00001)
		GPIO.output(TRIG1, GPIO.LOW)
		GPIO.output(TRIG2, GPIO.LOW)
		GPIO.output(TRIG3, GPIO.LOW)
		GPIO.output(TRIG4, GPIO.LOW)

        # En este momento el sensor envía 8 pulsos ultrasónicos de 40kHz y coloca su pin ECHO en alto
        # Debemos detectar dicho evento para iniciar la medición del tiempo

		while True:
			pulso_inicio1 = time.time()
			if GPIO.input(ECHO1) == GPIO.HIGH:
				break
		while True:
			pulso_inicio2 = time.time()
			if GPIO.input(ECHO2) == GPIO.HIGH:
				break
		while True:
			pulso_inicio3 = time.time()
			if GPIO.input(ECHO3) == GPIO.HIGH:
				break
		while True:
			pulso_inicio4 = time.time()
			if GPIO.input(ECHO4) == GPIO.HIGH:
				break

        # El pin ECHO se mantendrá en HIGH hasta recibir el eco rebotado por el obstáculo.
        # En ese momento el sensor pondrá el pin ECHO en bajo.
	# Procedemos a detectar dicho evento para terminar la medición del tiempo

		while True:
			pulso_fin1 = time.time()
			if GPIO.input(ECHO1) == GPIO.LOW:
				break

        # Tiempo medido en segundos
		duracion1 = pulso_fin1 - pulso_inicio1

        #Obtenemos la distancia considerando que la señal recorre dos veces la distancia a medir y que la velocidad del sonido es 34300cm/s
		distancia1 = (34300 * duracion1) / 2

        # Imprimimos resultado
		print( "Distancia1: %.2f cm" % distancia1)

		while True:
			pulso_fin2 = time.time()
			if GPIO.input(ECHO2) == GPIO.LOW:
				break

		duracion2 = pulso_fin2 - pulso_inicio2
		distancia2 = (34300 * duracion2) / 2
		print( "Distancia2: %.2f cm" % distancia2)

		while True:
			pulso_fin3 = time.time()
			if GPIO.input(ECHO3) == GPIO.LOW:
				break

		duracion3 = pulso_fin3 - pulso_inicio3
		distancia3 = (34300 * duracion3) / 2
		print( "Distancia3: %.2f cm" % distancia3)

		while True:
			pulso_fin4 = time.time()
			if GPIO.input(ECHO4) == GPIO.LOW:
				break

		duracion4 = pulso_fin4 - pulso_inicio4
		distancia4 = (34300 * duracion4) / 2
		print( "Distancia4: %.2f cm" % distancia4)

	#control de distancia para frenado

		if distancia1<dist_min_lat or distancia2<dist_min_fron or distancia3<dist_min_fron or distancia4<dist_min_lat:
			alto=1
		else:
			alto=0
		print ("alto= %d "% alto)
finally:
    # Reiniciamos todos los canales de GPIO.
    GPIO.cleanup()
