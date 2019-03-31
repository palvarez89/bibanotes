import requests
import urllib.request
import time
from bs4 import BeautifulSoup


url = "http://web.mta.info/developers/turnstile.html"
url = "http://www.bicibadajoz.es/estado/EstadoactualBis.asp"
print("get url")
response = requests.get(url)
print("got url")

soup = BeautifulSoup(response.text, "html.parser")
print("find all trs")
tables = soup.findAll('tr')
print(len(tables))


#for i in range(len(tables)):
#    print(i)
#    print(i)
#    print(i)
#    print(type(tables[i]))
#    print(type(tables[i]))
#    print(type(tables[i]))
#    print(tables[i])

print("deal with trs")
#for i in range(4, len(tables)):
#    if "APARCAMIENTO" in str(tables[i]):
#        #print(tables[i])
#        titulo = tables[i].findAll("td", {"class": "titulo"})
#        print(titulo)
#    else:
#        if "ESTADO" in str(tables[i]):
#            estado = tables[i].findAll('td', {'class': 'lat2'})
#            print(estado)

titulos = soup.findAll("td", {"class": "titulo"})[1:]
estados = soup.findAll("td", {"class": "lat2"})
for i in range(len(titulos)):
    print(titulos[i].contents[0])
    print(estados[i*2+1].contents[0])
