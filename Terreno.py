#!/usr/bin/python
# -*- coding: utf-8 -*-
from apiTFG import *
import math 

#TODO EL CÓDIGO Y FUNCIONES EXTERNAS ESTAN PROGRAMADAS PARA PYTHON 2.7 POR MARIA LAO CAÑADAS

#Funcion que devuelve la elevacion del terreno y la latitud y longitud de esos puntos donde se mide
def perfil_terreno(latTX,lonTX,latRX,lonRX,muestras):
	#Se guardan en un formato concreto la latitud y la longitud para poder llamar a la API
	locTX=str(latTX)+","+str(lonTX)
	locRX=str(latRX)+','+str(lonRX)
    #Se unen las variables anteriores
	enlace = locTX + "|" + locRX
	#Tabla donde se va a guardar los resultados
	hobst_lat_lon=[]
	#Llamada a la API que nos devuelve los resultados del radioenlace
	hobst_lat_lon=getElevation(enlace,muestras)
	return hobst_lat_lon


#En esta funcion se decide que tipo de terreno es: llano o con obstaculos
def terrain_type(dis,elevacion, wave_len,a_e,h_TX,h_RX,latitud,longitud,muestras):
	"""En este bucle se va analizando cada uno de los puntos en los que se ha medido el radioenlace y se analiza la distancia al TX,
	la distancia al RX y otros parametros para saber si obstruye o no"""
	for n in range(1,len(elevacion)-1,1):
		dis_TX=GetDistance(latitud[0],longitud[0],latitud[n],longitud[n],a_e)
		dis_RX=GetDistance(latitud[n],longitud[n],latitud[muestras-1],longitud[muestras-1],a_e)
		#Se calcula el punto de la recta que une ambas antenas a esa distancia
		y_i=((h_RX-h_TX)/dis)*(dis_TX)+h_TX
		#Se calcula el despejamiento con la altura del punto y la elevacion del terreno
		despejamiento=elevacion[n]-y_i
		#Se calcula el radio del primer elipsoide de fresnel a esa distancia
		Fresnel_rad= math.sqrt((wave_len*dis_TX*dis_RX)/dis)
		#Si el despejamiento se encuentra entre -0.6 y 0.5 tendremos al menos un obstaculo 
		if (despejamiento/Fresnel_rad>=-0.6) and (despejamiento/Fresnel_rad<=0.5):
				medio= "medio_obstaculos"
				break
		#Si obstruye mas del 0.5 habrá al menos un punto que no permite que el radioenlace sea viable 		
		elif despejamiento/Fresnel_rad>0.5:
				medio="medio_obstaculos"
				break
		#Si no obstruye, estaremos ante un medio llano
		else:
			medio="medio_llano"		
	return medio	


