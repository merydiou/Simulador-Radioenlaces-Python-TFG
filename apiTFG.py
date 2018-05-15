# Copyright Google Inc. 2010 All Rights Reserved
import json
import urllib
import math

#TODO EL CÓDIGO Y FUNCIONES EXTERNAS ESTAN PROGRAMADAS PARA PYTHON 2.7 POR MARIA LAO CAÑADAS

ELEVATION_BASE_URL = 'https://maps.google.com/maps/api/elevation/json'
CHART_BASE_URL = 'http://chart.googleapis.com/chart'

DISTANCE_BASE_URL= 'https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&mode=walking&'

#esta es mi key con mi email.
key="key=AIzaSyDQYuB_SYy__J_-lf0Xp99L86jTzww1Yg0"
key_dis="key=AIzaSyBBS1tH2mJx421DnmgtD2gwREHWsyMf4I4"

def getChart(chartData, chartDataScaling="-500,1500", chartType="lc",chartLabel="Elevation in Meters",chartSize="1000x300", chartColor="orange", **chart_args):
    chart_args.update({
        'cht': chartType,
        'chs': chartSize,
        'chl': chartLabel,
        'chco': chartColor,
        'chds': chartDataScaling,
        'chxt': 'x,y',
        'chxr': '1,-500,1500'
    })

    dataString = 't:' + ','.join(str(x) for x in chartData)
    chart_args['chd'] = dataString.strip(',')

    chartUrl = CHART_BASE_URL + '?' + urllib.urlencode(chart_args)

    print("")
    print("Elevation Chart URL:")
    print("")
    print chartUrl

#Funcion que analiza el terreno entre ambas antenas
def getElevation(path,samples,sensor="false", **elvtn_args):
    elvtn_args.update({
        'path': path,
        'samples': samples,
        'sensor': sensor
    })

    #URL base para llamar a la API de Google
    url = ELEVATION_BASE_URL + '?' + urllib.urlencode(elvtn_args) + '&' +key
    #Respuesta de la API
    response = json.load(urllib.urlopen(url))
   
    # Create a dictionary for each results[] object
    elevationArray = []
    latitudArray=[]
    longitudArray=[]

    #Bucle donde se va guardando lo que se va a devolver, la elevacion y la latitud y longitud de cada uno de los puntos
    for resultset in response['results']:
      elevationArray.append(resultset['elevation'])
      latitudArray.append(resultset['location']['lat'])
      longitudArray.append(resultset['location']['lng'])

    return [elevationArray,latitudArray,longitudArray]      


#Funcion que calcula la distancia entre dos puntos 
def GetDistance(lat1, lon1, lat2, lon2,R):
    rad=math.pi/180
    dlat=lat2-lat1
    dlon=lon2-lon1
    a=(math.sin(rad*dlat/2))**2 + math.cos(rad*lat1)*math.cos(rad*lat2)*(math.sin(rad*dlon/2))**2
    distancia=2*R*math.asin(math.sqrt(a))*1000
    return distancia


     

        
    #gradosTXlat = float(raw_input('Introduce la latitud de la antena TX. Grados: '))
     #minutosTXlat= float(raw_input('Minutos: '))
     #segundosTXlat=float(raw_input('Segundos: '))

     #gradosTXlon = float(raw_input('Introduce la longitud de la antena TX. Grados: '))
     #minutosTXlon= float(raw_input('Minutos: '))
     #segundosTXlon=float(raw_input('Segundos: '))

     #gradosRXlat = float(raw_input('Introduce la latitud de la antena RX. Grados: '))
     #minutosRXlat= float(raw_input('Minutos: '))
     #segundosRXlat=float(raw_input('Segundos: '))

     #gradosRXlon = float(raw_input('Introduce la longitud de la antena RX. Grados: '))
     #minutosRXlon= float(raw_input('Minutos: '))
     #segundosRXlon=float(raw_input('Segundos: '))

     #latTX=gradosTXlat+minutosTXlat/60+segundosTXlat/3600
     #lonTX=gradosTXlon+minutosTXlon/60+segundosTXlon/3600

     #latRX=gradosRXlat+minutosRXlat/60+segundosRXlat/3600
     #lonRX=gradosRXlon+minutosRXlon/60+segundosRXlon/3600


