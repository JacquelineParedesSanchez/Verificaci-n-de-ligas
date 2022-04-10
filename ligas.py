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
totalprofit = []
totalunit = []
 
# iterating over each row and append
# values to empty list
liga='liga'
for col in file:

    month.append(col['Ligas'])
 
# printing lists
#print('Month:', month)
#response = requests.head('http://combio.snu.ac.kr/aspedia')
#print(response.status_code)
for col in month:
    try:
        response = requests.head(col)         
    # check the status code
        if (response.status_code>=100 and  response.status_code<=399):
            print(response.status_code,'true',col)
        else:
            print(response.status_code,'false',col)
    except requests.ConnectionError as e:
        print(response.status_code,'imposible abrir',col)