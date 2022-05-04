
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from multiprocessing.dummy import Pool as ThreadPool
import time

import links_funcionales as LINKS

path = LINKS.generar_links_validos('lista-links')

def main(file_path,file_name):

    #directorio del proyecto
    directory = os.getcwd()
    print('Fase 3, abriendo el archivo anterior')
    ##abriendo el archivo datas
    data_from_csv = pd.read_csv(file_path)
    data=[]

    for i, row in data_from_csv.iterrows():
        data.append(row)

    titles=[]    
    
    #Funcion que busca  los titulos de los links que tengan SI en Funciona
    def get_title(row):
        if(row['Funciona']=='SI'):
            try:
                
                r = requests.get(row['URL'], timeout=1000)
                html = BeautifulSoup(r.text,"lxml")
                title = html.title.text
                return title
            except:
                #por si pasa algo al busar el titulo
                return 'algo salio mal'
            else: 
                return  '---'

    results = ThreadPool(150).imap_unordered(get_title, data)
    print('Fase 4, Buscando los titulos correspondientes')
    #añadiendo los titulos 
    for i in results:
      
        titles.append(i)
        #Eliminando las columnas que no sean importantes
    for i in data_from_csv.columns:
        if(i!='URL' and i!='Funciona'):
            data_from_csv.pop(i)
        
    #añadiendo los titulos al csv
    data_from_csv['Titulo'] = titles

    #añadiendo espacios vacios para poder despues añadir la fecha
    white_space = {'URL':' ',"Funciona":'','Titulo':' '}
    for i in range(10):
        data_from_csv=data_from_csv.append(white_space,ignore_index=True)
    
    
    #Generando la fecha
    hora = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    
    #renglon que contiene la fecha de creacion
    fecha = {'URL':'FECHA','Funciona':'CREACION','Titulo':hora}
    data_from_csv=data_from_csv.append(fecha,ignore_index=True)

    #absolute path del archivo a guardar con el nombre
    name = directory+'\\'+file_name+'.csv'
    
    #Guardando el archivo en un csv
    data_from_csv.to_csv(name, index=False)
    
    
    print('FINALIZADO se creo el archivo',file_name +'.csv')
    
    
    
main(path,'Lista-completa')