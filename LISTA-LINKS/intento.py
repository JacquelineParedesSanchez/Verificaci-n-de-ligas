import urllib.request
import os
from urllib.request import urlopen
from urllib.error import *
import csv
import requests
from datetime import datetime

from bs4 import BeautifulSoup


from pandas import *
 
directory = os.getcwd()
# Leyendo el archivo CVS
ligas_csv = read_csv('NAR Database Summary Paper Alphabetic List.csv')
#ligas_csv = pandas.read_csv(directory+'\\links.csv')

ligas = [] #Archivo donde se guardan las ligas del CVS


print('parte 1 , buscando los links que funcionan')
#Agreganso uana lista a "ligas" que contiene el link y un true si la 
#liga esta activa, false en caso contrario
for col in ligas_csv['Ligas']:
    try:
        r = requests.head(col, timeout=30)
        r.raise_for_status()
        #si el link funcina, agrega el link y un true
        ligas.append([col,True])
    except Exception as e:
        #si el link NO funcina, agrega el link y un false
        ligas.append([col,False])
    
print('parte 1.5, guarnando link que si funcionen')

string_ligas='URL\tFunciona\n'
for liga in ligas:
    if(liga[1]):
        string_ligas+= liga[0]+'\tOn\n'
    else:
        string_ligas+= liga[0]+'\tOFF\n'
print('guardando el archivo')
file = open(directory+'\\ligas_validas.csv', "w",encoding='utf-8')
file. write(string_ligas)
file. close()


    
    
    
#iteramos las ligas 
print('parte 2, obteniendo el titulo')
for liga in ligas:
    #validando si las ligas estan activas
    if(liga[1]):
        try:
            #buscamos con y parseamos a html con beautiflsoup
            soup_link = BeautifulSoup(urlopen(liga[0]), "lxml")
            #buscamos el titulo
            title =  soup_link.find('title').string
            #cambiamos el estado de true a "on"
            liga[1]='On'
            #agreganos el titulo a la lista que contiene el url y el estado 
            liga.append(title)
        except:
            #hacemos esta validacion, pues aveces no se puede obtener el titulo
            #posiblemente es un problema con la pagina en si
            liga[1]='On'
            #agreganos la leyenda "algo salio mal" a la lista que contiene el url y el estado 
            liga.append('algo salio mal')
            
            
    else:
        #si era de las ligas que no fucionan, ponemos el estatus como off
        liga[1]='Off'
        #y agregamos el titulo como "No tiene"
        liga.append('No tiene')
        
#hacemo ls cabecera del csv
string_csv = 'Nombre\turl\tActivo\n'
print('parte 3 generando el documento')
for db in ligas:
    try:
        string_csv += '\t'.join(db)+'\n'
    except:
        string_csv+= db[0]+'\t\t\n'
    
#generamos la fecha 
now = datetime.now()

#agregamos la fecha
string_csv+='\n\n\n\n\n\n'+str(now)

#generamos el directorio actual 
directory = os.getcwd()

#guardamos el documento en la carpeta y con el nombre
file = open(directory+'\\test.csv', "w",encoding='utf-8')
file. write(string_csv)
file. close()



