import os
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import pandas as pd
from multiprocessing.dummy import Pool as ThreadPool
import time


def generar_links_validos(file):
    #generando la base de datos
    hora = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    print('Iniciado a las ',hora)
    print('Fase 1, Obteniendo los links de NAR')
    #Haciendo el request a la pagina de NAR
    soup = BeautifulSoup(urlopen("http://www.oxfordjournals.org/nar/database/a"), "lxml")
    #parseando los links dentro de la página de NAR
    urls = [link['href'] for link in soup.find_all('a', href=True) if link.text.strip() == "database"]
    total = len(urls)
    failed = 0

    #funcion que valida si los links funcionan, regresa el url y None si funcina
    #regresa el url y un error cuando la página no funciona
    def check(url):
        try:
            r = requests.head(url, timeout=30)
            r.raise_for_status()
            return url, None
        except Exception as e:
            return url, e

    list_working = []
    
    #usando la funcion check con los urls 
    results = ThreadPool(100).imap_unordered(check, urls)

    print('Fase 2, Revisando que links estan funcionado')
    # iterando sobre los resultados y añadiendo a list_working SI el url funciona
    # añade NO si no funciona
    for url, e in results:
        if e is None:
            list_working.append('SI')
        
        else:
            list_working.append('NO')
            failed += 1

    print("{}/{} failed".format(failed, total))
    
    #Creando el dataframe 
    d={'URL':urls,'Funciona':list_working}
    data=pd.DataFrame(data=d, index=[item for item in range(0,total)])

    #usando el directorio donde esta el proyecto
    directory = os.getcwd()
    
    #guardando el archivo en la raiz del proyecto y con el nombre de file
    final_file =directory+'\\'+file+'.csv'
    data.to_csv(final_file, index=False)
    print('se creo el archivo'+' '+file+'.csv')
    
    return final_file
    
    
