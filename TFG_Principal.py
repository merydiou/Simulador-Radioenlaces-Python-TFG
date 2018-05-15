#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from Terreno import *
from TerrenoLlano import *
from TerrenoObstaculos import *

#TODO EL CÓDIGO Y FUNCIONES EXTERNAS ESTAN PROGRAMADAS PARA PYTHON 2.7 POR MARIA LAO CAÑADAS

c=float(3e8)

print "Bienvenido al simulador de radioenlaces con obstáculos. Se necesitan los siguientes datos para el estudio:"
#frecuencia
freq = float(raw_input("Frecuencia en Hz: "))	
h_TXm = float(raw_input("Altura de la antena TX (mástil) en m: "))
h_RXm = float(raw_input("Altura de la antena RX (mástil) en m: "))	
#radio efectivo de la tierra
a_e= float(raw_input("Radio efectivo de la tierra en km: "))

latTX = raw_input('Introduce la latitud de la antena TX en formato decimal: ')
lonTX = raw_input('Introduce la longitud de la antena TX en formato decimal: ')
latRX = raw_input('Introduce la latitud de la antena RX en formato decimal: ')
lonRX = raw_input('Introduce la longitud de la antena RX en formato decimal: ')  

    
#wave lenght
wave_len=c/freq

#numero de muestras que se cogen en el enlace
muestras=500
#Se llama a la funcion que nos devuelve el perfil del enlace y del cual se obtendra la elevacion en cada punto asi como su latitud y longitud.
hobst_lat_lon=perfil_terreno(latTX,lonTX,latRX,lonRX,muestras)

elevacion=hobst_lat_lon[0]
latitud=hobst_lat_lon[1]
longitud=hobst_lat_lon[2]

"""Esta funcion imprime un enlace que lleva a una grafica del perfil que se esta estudiando, esta comentada porque no se hace uso de ella,
pero se deja propuesta por si hiciera falta en un futuro:
#print getChart(chartData=elevacion)
"""

#Distancia total del enlace
dis=GetDistance(latitud[0],longitud[0],latitud[muestras-1],longitud[muestras-1],a_e)
#Si la antena trasmisora y receptora estan en el mismo punto
if dis==0:
	print "ERROR: La distancia entre ambas antenas es 0."
	#Salimos del programa y se finaliza
	sys.exit()
#Se comprueba cual de las dos antenas se encuentra mas alta
#En el caso de ser la primera
if elevacion[0]>elevacion[muestras-1]:
	#Se modifican las alturas tomando como 0 absoluto la antena que se encuentra a menor altura
	h_RX=h_RXm
	h_TX=h_TXm+elevacion[0]-elevacion[muestras-1]
	elevacion_abs=elevacion[muestras-1]
#En otro caso
else:
	#Se modifican las alturas tomando como 0 absoluto la antena que se encuentra a menor altura
	h_TX=h_TXm
	h_RX=h_RXm+elevacion[muestras-1]-elevacion[0]
	elevacion_abs=elevacion[0]

#Se modifican el resto de elevaciones del terreno para que todas esten bajo el mismo sistema de referencia
for n in range(len(elevacion)):
	elevacion[n]=elevacion[n]-elevacion_abs

#La altura final de las antenas es la calculada anteriormente, hay que sobreescribir en sus posiciones correspondientes
elevacion[0]=h_TX
elevacion[muestras-1]=h_RX
 # Create the chart passing the array of elevation data

#tipo de terreno
tierra=terrain_type(dis,elevacion,wave_len,a_e,h_TX,h_RX,latitud,longitud,muestras)

#Si el medio que nos encontramos es llano y su frecuencia es mayor a 10MHz
if tierra=="medio_llano" and freq>=10e6 and a_e>0:
	perdidas_total=medio_llano(a_e,h_TX,h_RX,dis,wave_len,freq)
	#Se imprime el resultado
	print "Las pérdidas totales producidas por la difracción en este radioenlace que no se encuentra obstruido por ningun obstáculo, son en dB:",perdidas_total
#Si el medio que nos encontramos es llano y su frecuencia es menor a 10MHz se utilizará el programa de la ITU-R GRWAVE
elif (freq<=10e6 or a_e<=0) and tierra=="medio_llano":
	print("Utiliza el programa GRWAVE de la ITU-R ya que la frecuencia de trabajo es menor a 10MHz y el medio a tratar es llano")
	#Se finaliza el programa
	sys.exit()	

#Si el radioenlace se encuentra en un medio con obstaculos que obstreuyen se calculará el numero de obstáculos y se procede
elif tierra=="medio_obstaculos":
	#Se calcula el numero de obstáculos 
	obstaculos=numero_obstaculos(dis,latitud,longitud,elevacion,wave_len,a_e,muestras)
	"""Esta función devuelve 6 parametros imprescindibles para el cálculo de las pérdidas: el numero de obstaculos, la distancia de
	estos al TX y al RX, la altura que tienen, su latitud y longitud, asi como el despejamiento frente a la linea recta que une ambas 
	antenas""" 
	num_obs=obstaculos[0]
	d1=obstaculos[1]
	d2=obstaculos[2]
	elev=obstaculos[3]	
	lat=obstaculos[4]
	lon=obstaculos[5]
	despejamiento=obstaculos[6]

	if num_obs==0:
		perdidas_total=medio_llano(a_e,h_TX,h_RX,dis,wave_len,freq)
		
		#Se imprime el resultado
		print "Las pérdidas totales producidas por la difracción en este radioenlace que no se encuentra obstruido por ningun obstáculo, son en dB:",perdidas_total
	#Si el numero de obstaculos es 1
	elif num_obs==1:
		#Se calculan las perdidas que produce este obstaculo
		print "Este enlace presenta 1 obstáculo que produce perdidas"
		perdidas=unico_obs(wave_len,dis,d1[0],d2[0],despejamiento[0])
		print "Las pérdidas producidas por el obstáculo que se encuentra en las coordenadas (",lat[0],",",lon[0],") y cuya altura es de",elev[0]+elevacion_abs,"m toman un valor de:",perdidas,"dB"
	#Si el numero de obstáculos es 2 
	elif num_obs==2:
		print "Este enlace presenta 2 obstáculos que producen perdidas"
		if GetDistance(lat[0],lon[0],lat[1],lon[1],a_e)<250:
			print "Los obstáculos que se encuentran en las coordenadas (",lat[0],",",lon[0],") y (",lat[1],",",lon[1],") cuyas alturas son de",elev[0]+elevacion_abs,"m y",elev[1]+elevacion_abs,"m están separados menos de 250m por lo que no se puede aplicar el método de dos obstáculos aislados."	
		else:
			#Se calculan las perdidas que producen estos obstaculos
			perdidas=dos_obs(wave_len,dis,d1,d2,despejamiento,elev,lat,lon,a_e,h_RX)
			print "Las pérdidas producidas por los obstáculos que se encuentran en las coordenadas (",lat[0],",",lon[0],") y (",lat[1],",",lon[1],") cuyas alturas son de",elev[0]+elevacion_abs,"m y",elev[1]+elevacion_abs,"m toman un valor de:",perdidas,"dB"	
	#ERROR y se sale del programa
	elif num_obs=="error":
		sys.exit()		
	#En el caso de ser mas de 2 obstáculos no se realiza nada
	else:
		print "El número de obstáculos de este enlace para esta frecuencia y altura de antenas es de:",num_obs

	if perdidas=="error":
		print "No ha introducido un valor correcto"
		sys.exit()








