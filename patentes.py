from persona import Persona
from browser import Session
from spyder import Spyder
import json

# Nota
""""
La idea es guardar cada patente consultada en una base de datos
(sqlite3) para reducir el tiempo de carga para futuras consultas
de la misma. Otro motivo, aun mas importante es generar una bases
de datos propia.
"""
# IDEA
"""
Contratar una vps barato por un mes y realizar peticiones de manera masiva
con patentes generadas automaticamente con el fin de crear la base de datos
propia.
"""

URL = "https://www.patentechile.com/resultados"
_browser = Session()
_donde_buscar = {"rut"         : 2,  "nombre"          : 4, "patente": 8, "tipo"  : 10,
                 "marca"       : 12, "modelo"          : 14, "year"  : 16, "color": 18,
                 "numero motor": 20, "numero de chasis": 22, "multas": 24}


"""Realiza la peticion al servidor"""
def _requests(pyload):
    document = _browser.post(URL, data=pyload)
    if document.status_code != 200:
        raise Exception("Error al cargar la web de patentes")

    return document


"""Extrae la informacion de la pagina"""
def _spyder(document, datos):
    _ = Spyder(document, datos, _donde_buscar, "propietario")

    # propietario
    datos["propietario"] = Persona(
        nombre=_[_donde_buscar["nombre"]].text,
        rut=_[_donde_buscar["rut"]].text)

    return datos

class Patente:

    @staticmethod
    def rut(rut: str) ->  list:
        return []


    def __init__(self, patente, tipo=None):
        self.patente = patente

        if (tipo == None or tipo == "v" or tipo == "vehiculo"):
            tipo = "vehiculo"
        elif tipo == "m" or tipo == "moto":
            tipo = "moto"
        else:
            print ("Clase: Patente. El tipo no es valido! Esto nunca debio pasar..")

        self.tipo = tipo
        self._datos = {
            "patente"         : patente,
            "tipo"            : tipo,
            "marca"           : None,
            "modelo"          : None,
            "color"           : None,
            "numero de chasis": None,
            "numero motor"    : None,
            "year"            : None,
            "multas"          : None,
            "propietario"     : None,
        }

        self._ok = False

    @property
    def datos(self):
        if self._ok:
            return self._datos

        _spyder(_requests({
            "frmTerm": self.patente,
            "frmOpcion": self.tipo}), self._datos)

        self._ok = True
        return self._datos

    def __repr__(self) -> str:
        return str(self._datos)


def tojson(patente):
    _ = patente.datos
    _ = _.copy()
    _["propietario"] = {
        "nombre": patente.datos["propietario"].nombre,
        "rut": patente.datos["propietario"].rut}
    return _


