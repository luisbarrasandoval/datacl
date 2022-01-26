from bs4 import BeautifulSoup

def Spyder(document, datos, donde_buscar, omitir=None):
    document = BeautifulSoup(document.text, features="lxml")
    _ = document.table.find_all("td")
    
    for k in datos.keys():
        if k == omitir:
            continue
        datos[k] = _[donde_buscar[k]].text
    
    
    return _