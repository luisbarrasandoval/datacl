from bs4 import BeautifulSoup
from browser import Session
from spyder import Spyder

# search for names
URL_FOR_NAME = "https://rutificador.app/rutificador-20/nombre.php"

##############


URL = "https://rutificador.app/rutificador-20/rut.php"  # term=19.944.403-4
_browser = Session("app.details.rutificadorapp")
_donde_buscar = {
    "nombre": 4, "rut": 2, "genero": 6,
    "direccion": 8, "comuna": 10, "edad": 12
}

"""Realiza la peticion al servidor"""


def _requests(pyload, url=None):
    if url is None:
        url = URL
    document = _browser.post(url, params=pyload)
    if document.status_code != 200:
        raise Exception("Error al cargar la web de personas")

    return document


class Persona:

    def __init__(self, nombre=None, rut=None):
        # if rut == None:
        #    raise Exception("No se puede crear una persona vacia")
        self._rut = None
        self.nombre = nombre
        self.rut = rut

        self._datos = {
            "nombre": self.nombre,
            "rut": self.rut,
            "genero": None,
            "direccion": None,
            "comuna": None,
            "edad": None
        }

        self._ok = False

    @property
    def rut(self):
        return self._rut

    @rut.setter
    def rut(self, rut):
        if rut is None:
            return
        elif len(rut) == 10:
            rut = rut[0:2] + "." + rut[2:-5] + "." + rut[5:-2] + "-" + rut[-1]
        elif len(rut) == 9:
            rut = rut[0] + "." + rut[1:-5] + "." + rut[-5:-2] + "-" + rut[-1]
        else:
            raise Exception("Esto no deveria pasar rut: {}".format(rut))

        self._rut = rut

    @property
    def datos(self):
        if self._ok:
            return self._datos

        Spyder(_requests({
            "term": self.rut
        }), self._datos, _donde_buscar)

        self._ok = True
        return self._datos

    def update_data(self, data):
        self._ok = True
        self._datos.update(data)
        return self._datos

    @staticmethod
    def by_nombre(name):
        persons = []

        _ = BeautifulSoup(_requests({
            "term": name
        }, URL_FOR_NAME).text, features="lxml")

        _ = _.table
        for person in _.find_all("tr")[1:]:
            tds = person.select("td")
            p = Persona(
                nombre=tds[1].text
            )

            p.update_data({
                "nombre": tds[1].text,
                "rut": tds[0].text,
                "genero": tds[2].text,
                "direccion": tds[3].text,
                "comuna": tds[4].text,
                "edad": "0"

            })

            persons.append(p)

        return persons

    def __repr__(self) -> str:
        return str(self._datos)
