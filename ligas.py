import urllib.request
import os
from urllib.request import urlopen
from urllib.error import *
import csv
import requests
# importing module
from pandas import *
 
# Leyendo el archivo CVS
filename = open('NAR Database Summary Paper Alphabetic List.csv', 'r')
file = csv.DictReader(filename)

ligas = [] #Archivo donde se guardan las ligas del CVS

#Guardado de ligas en el arreglo
for col in file:
    ligas.append(col['Ligas']) 

#Ceración del archivo donde se guardan las ligas activas
wtr = csv.writer(open ('Ligas.csv', 'w'), delimiter=',', lineterminator='\n')

#Guardamos las lligas activas en CVS
for col in ligas:
    try:
        r = requests.head(col, timeout=30)
        r.raise_for_status()
        print( col, 'Liga activa')
        wtr.writerow ([col])
    except Exception as e:
        print( col, 'Liga ligas inactiva')