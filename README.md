# Simulador de radioenlaces con obstáculos

Este proyecto se ha realizado como motivo del Trabajo Fin de Grado para la Universidad de Sevilla en la titulación de Grado en Ingeniería de Tecnologías de Telecomunicación por María Laó.

## Resumen
Basándose en la recomendación de la *ITU-R P.526* este proyecto implementa distintos métodos matemáticos para tratar radioenlaces que presentan difracción en su recorrido. Se hace distinción según el tipo de medio que se está tratando, medio llano o con obstáculos y dentro de este último se adentrará en la forma de resolución para uno y dos obstáculos aislados, tanto filo de cuchillo como con radio conocido.
Simplemente introduciendo algunos parámetros que configura el usuario como la frecuencia, el radio efectivo de la tierra o la altura de los mástiles de las antenas, además de las coordenadas (latitud y longitud en formato decimal) dónde se quieren colocar las antenas, transmisora y receptora es capaz de analizar el medio y calcular sus pérdidas.
Con las coordenadas en formato decimal como parte imprescindible y haciendo uso de una *API de Google*, cuyo uso se ha adaptado a *Python* también en este trabajo, se consiguen otros datos tales como la distancia entre antenas, la distancia a posibles obstáculos, la elevación del terreno en cada uno de los puntos en los cuales se analiza, despejamiento y otros factores de carácter imprescindible en nuestro diseño del radioenlace.


## Manual de Uso
Este programa se ha probado y codificado usando Sublime, por lo que se va a explicar su uso en este mismo programa.

1. Tener instalado la versión de Python en la que se trabaja, **2.7**.
2. Instalar Sublime y tras este, el pluging de **Anaconda**.
3. Abrir el fichero principal titulado **"TFG_Principal.py"**.
4. En el menú principal de Sublime, **Tools>SublimeREPL>Python>Python - Run Current File**
5. Tras esto, se abrirá una ventana con el programa ejecutándose.
6. Introducir los valores en el formato que se indica:
		-Valores muy grandes como 300MHz serán **300e6**
		-**Coordenadas en formato decimal** y latitud y longitud por separado en distintas líneas (se indica explícitamente en la ejecución)
		-Otros datos se indica qué o cómo tienen que introducirse (cómo la polarización, *h* o *v*, o si se conoce o no el radio, *s* o *n*)
7. El programa finalizará sin errores si todo se ha introducido de forma correcta y nos devolverá las pérdidas resultantes. En otro caso nos dará error de Python.