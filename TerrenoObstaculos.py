#!/usr/bin/python
# -*- coding: utf-8 -*-
import math 
from apiTFG import *
from Cv_Sv import *

#TODO EL CÓDIGO Y FUNCIONES EXTERNAS ESTAN PROGRAMADAS PARA PYTHON 2.7 POR MARIA LAO CAÑADAS

"""Funcion que calcula el numero de obstaculos y guarda la distancia al TX y al RX a la que se encuentra,
la altura que tienen, su latitud y longitud, asi como el despejamiento frente a la linea recta que une ambas 
antenas""" 
def numero_obstaculos(dis,latitud,longitud,elevacion,wave_len,a_e,muestras):
    #Variables
    n_obs=0    
    latTX=latitud[0]
    lonTX=longitud[0]
    latRX=latitud[muestras-1]
    lonRX=longitud[muestras-1]
    h_TX=elevacion[0]
    h_RX=elevacion[muestras-1]
    #Tablas donde se guardarán los resultados que son devueltos
    d1=[]
    d2=[]
    elev=[]
    lat=[]
    lon=[]
    despej=[]
    #Listas donde se guardan los datos de los posibles obstáculos
    posibles=[[],[],[]]
 


    """Bucle que recorre toda la tabla de elevacion y guarda en posibles aquellos puntos que son mayor que el punto anterior y 
    mayor que el punto siguiente, es decir es un pico. Se guarda su altura, latitud y longitud"""
    for n in range(1,muestras-1,1):
        if elevacion[n]>elevacion[n-1] and elevacion[n]>elevacion[n+1]:
            posibles[0].append(elevacion[n])
            posibles[1].append(latitud[n])
            posibles[2].append(longitud[n])              

    """Una vez filtrada la lista, con los valores de posibles se analiza cual de ellos obstruyen el radioenlace y solo aquellos
    que estan entre -0.6 y 0.5 e contaran como obstáculos. Si supera el 60% de obstrucción se devolverá error y se saldrá del 
    programa, pues el radioenlace es inviable"""
    for b in range(len(posibles[0])):
        dis_TX=GetDistance(latitud[0],longitud[0],posibles[1][b],posibles[2][b],a_e)
        dis_RX=GetDistance(posibles[1][b],posibles[2][b],latitud[muestras-1],longitud[muestras-1],a_e)
        
        y_i=((h_RX-h_TX)/dis)*(dis_TX)+h_TX
        
        despejamiento=posibles[0][b]-y_i
            
            #Calculamos el radio del elipsoide de fresnel en ese punto
        Fresnel_rad= math.sqrt((wave_len*dis_TX*dis_RX)/dis)    

        if despejamiento/Fresnel_rad>0.5:
            n_obs="error"
            print "Este enlace no es viable. El primer elipsoide de Fresnel se encuentra obstruido mas del 60% en el punto (", posibles[1][b],",",posibles[2][b],")"
            break

        elif (despejamiento/Fresnel_rad>=-0.6) and (despejamiento/Fresnel_rad<=0.5):
            
            #Calculamos las distancias desde el TX al obstaculo y al RX desde el obstaculo 
            distancia1=GetDistance(latTX,lonTX,posibles[1][b],posibles[2][b],a_e)
            distancia2=GetDistance(posibles[1][b],posibles[2][b],latRX,lonRX,a_e)
                #Si la obstruye el numero de obstaculos se incrementará en 1, y se guardaran las distancias calculadas    
            n_obs+=1
            d1.append(distancia1)
            d2.append(distancia2)
            elev.append(posibles[0][b])
            lat.append(posibles[1][b])
            lon.append(posibles[2][b])
            despej.append(despejamiento)

    return [n_obs,d1,d2,elev,lat,lon,despej]
  


#Si solo hay un obstáculo 
def unico_obs(wave_len,dis,d1,d2,despejamiento):
    #parámetros
    v=despejamiento*math.sqrt((2/wave_len)*((1/d1)+(1/d2)))
    radio = raw_input("¿Se conoce el radio del obstáculo? s o n: ")
    #si no se conoce el radio->filo de cuchillo
    if radio =="n":
        #las perdidas son igual a J(v)
        perdidas=calc_Jv(v)
    #si se conoce el radio 
    elif radio=="s":
        #calculo J(v)
        J_v=calc_Jv(v)
        #se pide el radio pues es conocido
        radio = float(raw_input("Introduzca el valor del radio en metros: "))
        #se calcula T(m,n)
        T_mn=calc_Tmn(radio,wave_len,d1,d2,despejamiento)
        #se suman los valores para calcular las perdidas
        perdidas=J_v+T_mn
    else:
        #si no se introdujo ni s ni n
        perdidas="error"        
    return perdidas          


#En esta funcion se calcula J(v)
def calc_Jv(v):
    #Si es mayor a -0.78
    if v>=(-0.78):
        J_v=6.9+20*math.log10(math.sqrt((v-0.1)**2+1)+v-0.1)
    else:
        #en otro caso, se redondea y se deja el v introducido como un valor con dos decimales
        v_mod="{0:.2f}".format(round(v,2))
        #Los valores de Cv y Sv se cogen del diccionario que se encuentra en el otro archivo que relaciona v con los valores correspondientes
        J_v=-20*math.log10((math.sqrt((1-Cv_Sv[v_mod][0]-Cv_Sv[v_mod][1])**2)+(Cv_Sv[v_mod][0]-Cv_Sv[v_mod][1])**2)/2)
    return J_v    


#En esta función se calcula el valor de T(m,n) necesario para las perdidas
def calc_Tmn(r, wave_len,d1,d2,h):
    #Se calcula m
    m=(r*(d1+d2)/(d1*d2))/(((math.pi*r)/wave_len)**(float(1)/float(3)))
    #Se calcula n
    n=(h*((math.pi*r)/wave_len)**(float(2)/float(3)))/(r)

    #Se calcula dependiendo del valor de m y n
    if m*n<=4:
        T_mn=7.2*math.sqrt(m)-(2-12.5*n)*m+3.6*m**float(3/2)-0.8*m**2

    else:
        T_mn=-6-20*math.log10(m*n)+7.2*math.sqrt(m)-(2-17*n)*m+3.6*m**float(3/2)-0.8*m**2

    return T_mn   

#Funcion que calcula las perdidas si hay dos obstaculos    
def dos_obs(wave_len,dis,d1,d2,despejamiento,elev,lat,lon,a_e,h_RX):
    #Se calcula cada una de las v
    v=despejamiento[0]*math.sqrt((2/wave_len)*((1/d1[0])+(1/d2[0])))
    #Perdidas del obstaculo 1 suponiendo filo de cuchillo
    L_1=calc_Jv(v)
    #calculamos la distancia del obstaculo 2 al 1
    dis_obs1=GetDistance(lat[0],lon[0],lat[1],lon[1],a_e)
    #punto en el que se encuentra el obstaculo 2 frente a la linea recta que une el obstaculo 1 con el RX
    y_i=((h_RX-despejamiento[0])/d2[0])*(dis_obs1)+despejamiento[0]
    #Nuevo despejamiento entre ese punto y la elevacion del obstaculo 2
    h_2_nueva=elev[1]-y_i
    v2=h_2_nueva*math.sqrt((2/wave_len)*((1/dis_obs1)+(1/d2[1])))
    #Perdidas producidas por el obstaculo 2 suponiendo filo de duchillo
    L_2=calc_Jv(v2)
    #Calculo del termino de correccion
    T_c=calc_Tc(wave_len,d1,d2,dis_obs1,despejamiento)

    #Si se conoce el radio, habrá que calcular Tmn y tenerlo en cuenta en el resultado final
    radio = raw_input("¿Se conoce el radio del obstáculo? s o n: ")
    if radio=="n":
        #Perdidas suponiendo filo de duchillo
        perdidas=L_1+L_2-T_c
    elif radio=="s":
        radio1 = float(raw_input("Introduzca el valor del radio del primer obstáculo en metros: ")) 
        T_mn1=calc_Tmn(radio1,wave_len,d1[0],d2[0],despejamiento[0])
        radio2 = float(raw_input("Introduzca el valor del radio del segundo obstáculo en metros: ")) 
        T_mn2=calc_Tmn(radio2,wave_len,dis_obs1,d2[1],h_2_nueva) 
        #Perdidas teniendo en cuenta el radio
        perdidas=L_1+T_mn1+L_2+T_mn2-T_c 
    else:
        perdidas="error"    

    return perdidas        

#Funcion que calcula el termino de correccion
def calc_Tc(wave_len,d1,d2,dis_obs,despejamiento):
    despejamiento[0]=abs(despejamiento[0])
    despejamiento[1]=abs(despejamiento[1])
    #Variable p
    p=math.sqrt((2*(d1[0]+dis_obs+d2[1]))/(wave_len*(dis_obs+d2[1])*d1[0]))*despejamiento[0]
    #Variable q
    q=math.sqrt((2*(d1[0]+dis_obs+d2[1]))/(wave_len*(dis_obs+d1[0])*d2[1]))*despejamiento[1]
    #parametro alpha
    alpha=math.atan(math.sqrt((dis_obs*(d1[0]+dis_obs+d2[1]))/(d1[0]*d2[1])))
    #Calculo del termino con los datos calculado anteriormente
    T_c=(12-20*math.log10(2/(1-alpha/math.pi)))*(q/p)**(2*p)
    return T_c  
    
    

