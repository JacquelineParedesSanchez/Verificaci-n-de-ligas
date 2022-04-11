import urllib.request
import os
from urllib.request import urlopen
from urllib.error import *
import csv
import requests
# importing module
from pandas import *
 
# reading CSV file
# open the file in read mode
filename = open('NAR Database Summary Paper Alphabetic List.csv', 'r')
 
# creating dictreader object
file = csv.DictReader(filename)
 
# creating empty lists
month = []
ligas_act=[]
ligas_inac=[]
# iterating over each row and append
# values to empty list
for col in file:
    month.append(col['Ligas']) 
# printing lists
#print('Month:', month)
#response = requests.head('http://www.brenda-enzymes.org/')
#print(response.status_code)
cont=0
wtr = csv.writer(open ('Ligas.csv', 'w'), delimiter=',', lineterminator='\n')
for col in month:
    try:
        response = requests.head(col)
        if (response.status_code>=200 and response.status_code<=399):
            print(response.status_code,'true',col,cont)
            ligas_act.append(col)
            cont=cont+1
            wtr.writerow ([col])
        else:
            print(response.status_code,'false',col,cont)
            cont=cont+1
    except requests.ConnectionError as e:
        print('imposible abrir',col,cont)
        cont=cont+1

#wtr = csv.writer(open ('Ligas.csv', 'w'), delimiter=',', lineterminator='\n')
#for x in ligas_act : wtr.writerow ([x])