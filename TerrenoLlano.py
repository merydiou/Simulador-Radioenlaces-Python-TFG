#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
import sys

#TODO EL CÓDIGO Y FUNCIONES EXTERNAS ESTAN PROGRAMADAS PARA PYTHON 2.7 POR MARIA LAO CAÑADAS

def medio_llano(a_e,h_TX,h_RX,dis,wave_len,freq):
#Se calcula la distancia limite 
	d_los=(math.sqrt(2*a_e*1e3))*(math.sqrt(h_TX)+math.sqrt(h_RX))
	#Si la distancia del enlace es mayor a la d_los se calcula K y la fuerza de difraccion del campo en dBs 
	if dis>=d_los:
		#Se calcula E en dBs
		K=admitancia_superficie(wave_len,a_e)
		difraccion_campo_E=fuerza_difraccion_campo(K,dis,wave_len,a_e,freq,h_TX,h_RX)
		if K=="Error" or difraccion_campo_E=="Error":
			sys.exit()	
		else:
			perdidas_total=difraccion_campo_E
	else:
		#Cuando d es menor que dlos se continua con el otro metodo y se imprimen las perdidas
		perdidas_total=h_curvatura_rayo(dis,h_TX,h_RX,a_e,wave_len,freq)		
		return perdidas_total

#Funcion que calcula K
def admitancia_superficie(wave_len, a_e):
	#polarizacion
	polarizacion=raw_input("Polarización de la antena TX(introducir h, para indicar horizontal, o v, para vertical): ")
	#solo se tiene en cuenta el primer termino de la serie
	#Si la polarizacion es horizontal
	if polarizacion=="h" or polarizacion=="H":
		#Se tiene que introducir la permitividad y conductividad adecuadas a esa frecuencia y medio
		permitividad_relativa=float(raw_input("Permitividad relativa: "))
		conductividad=float(raw_input("Conductividad en S/m: "))
		#Se calcula K
		K=((2*math.pi*a_e*1000)/wave_len)**(float(-1)/float(3))*(((permitividad_relativa-1)**2+(60*wave_len*conductividad)**2)**(float(-1)/float(4)))
	
	#Si la polarizacion es vertical
	elif polarizacion=="v" or polarizacion=="V":
		#Se tiene que introducir la permitividad y conductividad adecuadas a esa frecuencia y medio
		permitividad_relativa=float(raw_input("Permitividad relativa: "))
		conductividad=float(raw_input("Conductividad en S/m: "))
		#Se calcula K_h y tras esto K
		K_h=((2*math.pi*a_e*1e3)/wave_len)**(float(-1)/float(3))*((permitividad_relativa-1)**2+(60*wave_len*conductividad)**2)**(float(-1)/float(4))
		K=K_h*math.sqrt(permitividad_relativa**2+(60*wave_len*conductividad)**2)
	
	#Si no se ha introducido un valor correcto
	else:
		print ("Introduce un valor correcto de polarización")
		K="Error"
	return K


#Funcion que calcula la fuerza de difraccion del campo
def fuerza_difraccion_campo(K, dis, wave_len, a_e, freq,h_TX,h_RX):
	#Si K fue error la fuerza de difraccion del campo tambien lo sera
	if K=="Error":
		f_dif_camp="Error"
	#Si K es menor que determinado valor, la fuerza sera 0	
	elif K<0.001:
		f_dif_camp=0
	#Si K es mayor que 1 habrá que utiliar el programa de la ITU GRWAVE	
	elif K>1:
		print("Utiliza el programa GRWAVE de la ITU-R ya que la frecuencia de trabajo es menor a 10MHz y el medio a tratar es llano")
		f_dif_camp="Error"
	#En otro caso, se calculan el resto de parametros necesarios para saber la fuerza de difraccion del campo	
	else:
		tierra_o_mar=raw_input("¿La distancia que separa las antenas es por tierra o mar? Introduce t o w: ")
		#Si se introdujo un valor correcto
		if tierra_o_mar=="t" or tierra_o_mar=="T" or tierra_o_mar=="w" or tierra_o_mar=="W":
			#Se llama a la funcion que calcula Beta, parametro imprescindible para continuar
			beta=calc_beta(K,tierra_o_mar,freq)
			print "El parametro beta que depende del tipo de terreno toma el valor:",beta
			#longitud normalizada del terreno entre ambas antenas
			X=beta*dis*(math.pi/(wave_len*(a_e*1e3)**2))**(float(1)/float(3))
			#altura normalizada
			Y_TX=2*beta*h_TX*((math.pi)**2/(wave_len**2*a_e*1e3))**(float(1)/float(3))
			Y_RX=2*beta*h_RX*((math.pi)**2/(wave_len**2*a_e*1e3))**(float(1)/float(3))
			#termino que depende de la distancia
			if X<1.6:
				F=-20*math.log10(X)-5.6488*(X**float(1.425))
				print "F(X) en dB:",F
			else:
				F=11+10*math.log10(X)-17.6*X
				print "F(X) en dB:",F
			#Ganancia de alturas	
			G_TX=calc_G(Y_TX,beta,K)
			print "La ganacia de altura de la antena transmisora,G(Y_1), toma el valor en dB:",G_TX
			G_RX=calc_G(Y_RX,beta,K)
			print "La ganacia de altura de la antena receptora,G(Y_2), toma el valor en dB:",G_RX
			f_dif_camp=F+G_TX+G_RX
		#Si el valor introducido no fue correcto
		else:
			f_dif_camp="Error"	

	return f_dif_camp	
	


#Funcion que calcula el parámetro beta
def calc_beta(K, tierra_o_mar, freq):
	#Si el radioenlace es por tierra con una frecuencia mayor a 20MHz o por mar con freq mayor a 300MHz, BETA=1
	if (((tierra_o_mar=="t" or tierra_o_mar=="T") and freq>=20e6) or ((tierra_o_mar=="w" or tierra_o_mar=="W" )and freq>=300e6)):
		beta=1
	#en otro caso se calcula
	else:
		beta=(1+1.6*K**2+0.67*K**4)/(1+4.5*K**2+1.53*K**4)	
	return beta
		

#Funcion que calcula la ganancia de altura
def calc_G(Y,beta,K):
	#Parametro intermedio B que depende de beta y de Y_TX o Y_RX
	B=beta*Y
	#Se aplica la formula de la ganancia de altura en funcion del valor de B
	if B<=2:
		ganancia_altura=20*math.log10(B+0.1*B**3)
	else:
		ganancia_altura=17.6*(B-1.1)**(float(1)/float(2))-5*math.log10(B-1.1)-8

	#Excepcion
	if ganancia_altura<(2+20*math.log10(K)):
		ganancia_altura=2+20*math.log10(K)

	return ganancia_altura	


#Funcion que calcula los parametros necesarios para poder llamar a perdidas y devolver ese valor
def h_curvatura_rayo(dis,h_TX,h_RX,a_e, wave_len,freq):
	#Parametros c y m necesarios para calcular b
	#c
	c_d=(h_TX-h_RX)/(h_TX+h_RX)
	#m
	m=(dis**2)/(4*a_e*1e3*(h_TX+h_RX))
	#b, necesario para calcular d_TX

	b=(2*math.sqrt(float(m+1)/float(3*m)))*math.cos((math.pi/3)+(float(1)/float(3))*math.acos((3*c_d/2)*math.sqrt((3*m)/((m+1)**3))))
	#distancia desde el transmisor hasta el punto donde la altura desde la curvatura de la tierra hasta el rayo es mas pequeña
	d_TX=(dis/2)*(1+b)
	#distancia desde el punto donde la altura desde la curvatura de la tierra hasta el rayo es mas pequeña hasta el RX
	d_RX=dis-d_TX
	#altura minima desde la curvatura de la tierra hasta el rayo que viaja entre ambas antenas
	h=((h_TX-(d_TX**2/(2*a_e*1e3)))*d_RX+(h_RX-(d_RX**2/(2*a_e*1e3)))*d_TX)/dis
	#con estos parametros se llama a la funcion perdidas
	return perdidas(h,d_TX,d_RX,wave_len,dis,h_TX,h_RX,freq)


#Funcion que calcula las perdidas que hay en el terreno
def perdidas(h,d_TX,d_RX,wave_len,dis,h_TX,h_RX,freq):
	#Se calcula h_req para poder compararlo con el h calculado con anterioridad
	h_req=0.552*math.sqrt((d_TX*d_RX*wave_len)/dis)
	#Si el valor de h introducido es mayor, no existen perdidas
	if h>h_req:
		perdidas=0
	#en otro caso, se calcula un a_e nuevo, modificado, y con esto, se calcula K y la fuerza de difraccion
	else:
		a_emodificado=0.5*(dis/(math.sqrt(h_TX)+math.sqrt(h_RX)))**2
		#se pasa a km para que en las formulas anteriores no de errores de unidades
		a_emodificado=a_emodificado/1e3
		print "El radio efectivo de la tierra modificado es de: ",a_emodificado," km"
		K=admitancia_superficie(wave_len,a_emodificado)
		A_h=fuerza_difraccion_campo(K,dis,wave_len,a_emodificado,freq,h_TX,h_RX)
		#Si es menor que cero, no existen perdidas
		if A_h<=0:
			perdidas=0
		else:	
			perdidas=A_h*(1-(h/h_req))		
	return perdidas	
