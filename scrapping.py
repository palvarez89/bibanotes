import requests
from bs4 import BeautifulSoup

url = "http://www.bicibadajoz.es/estado/EstadoactualBis.asp"

latitude =  [38.8787,38.8769,38.8753,38.8760,38.8730,38.8706,38.8707,38.8662,38.8669,38.8737,38.8792,38.8788,38.8951,38.8902,38.8856,38.8851,38.8855,38.8866,38.8829,38.8830,38.8855,38.8437,38.8621,38.8836]
longitude = [-6.9698,-6.9712,-6.9740,-6.9769,-6.9743,-6.9822,-6.9888,-6.9845,-6.9741,-6.9647,-6.9611,-6.9556,-6.9695,-6.9822,-6.9799,-6.9919,-6.9942,-6.9994,-7.0004,-7.0052,-7.0110,-6.9684,-7.0039,-7.0227]

# Ejemplo html a leer
# <td class="titulo" colspan="100" nowrap="">02 - PLAZA SAN ATÓN - FUERA DE LÍNEA</td>
# <td width="100" class="lat2" nowrap="">POSICION</td>
# <td width="100" class="lat2" nowrap="">ESTADO - (2/10)</td>

def get_estaciones():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Titulos de estacion tienen la clase "titulo", ignoramos el primer resultado
    titulos_html = soup.findAll("td", {"class": "titulo"})[1:]
    estados_html = soup.findAll("td", {"class": "lat2"})

    to_return = []
    for i in range(len(titulos_html)):
        titulo_completo = titulos_html[i].contents[0]
        disp_total_completo = estados_html[i*2+1].contents[0]


        n, nombre, estado_estacion = titulo_completo.split('-')
        n = n.strip()
        nombre = nombre.strip()
        estado_estacion = estado_estacion.strip()

        _, disp_total = disp_total_completo.split('-')
        disp_total = disp_total.strip()[1:-1]
        disp, total = disp_total.split('/')

        detalles_estacion = {
            "n": n,
            "name": nombre,
            "lat": latitude[int(n)-1],
            "lon": longitude[int(n)-1],
            "state": estado_estacion,
            "avail": disp,
            "total": total
        }
        to_return.append(detalles_estacion)

    return to_return;
