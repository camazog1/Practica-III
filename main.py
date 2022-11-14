import requests
from bs4 import BeautifulSoup
import spacy
nlp = spacy.load("en_core_web_sm")

class TreeNode: #Arbol No Binario

    def __init__(self, val):
        self.value = val
        self.branches = []

    def add_node(self, value):
        self.branches.append(TreeNode(value))

    def travel(self):
        if self.branches == None:
            print(self.value)
        else:
            print(self.value)
            for element in self.branches:
                element.travel()

def datos(persona): #Estracción de html de persona
    item = list(map(str, persona.split(" ")))
    busqueda = "/wiki/"
    for i in range(len(item)):
        if i == len(item) - 1:
            busqueda = busqueda + str(item[i])
        else:
            busqueda = busqueda + str(item[i]) + "_"

    page = requests.get("https://wikipedia.org" + busqueda)
    return BeautifulSoup(page.content, 'html.parser')

def fill_tree(dato, tree, p1, lim):
    text = ""
    limite = 0
    listados = []
    for link in dato.find_all('a'):
        if link.get("title") == None:
            continue
        else:
            text += link.get("title") + ", "

    doc = nlp(text)

    for ent in doc.ents:
        if limite == lim:
            break
        elif ent.label_ == "PERSON" and p1 not in str(ent) and str(ent) not in listados:
            tree.add_node(str(ent))
            listados.append(str(ent))
            limite += 1
        else:
            continue

def validar(pf, dato):
    for link in dato.find_all('a'):
        if link.get("title") == pf:
            return True
        else:
            continue
    return False

def bdd(p1, pf, dato, tree):
    fill_tree(dato,tree,p1,30)
    if validar(pf, dato):
        return p1 + " -> " + pf
    else:
        for element in tree.branches:
            d = datos(element.value)
            fill_tree(d, element,element.value, 5)
            if validar(pf, d):
                return p1 + " -> " + element.value + " -> " + pf
            else:
                continue

    return "No estan conectados"


def main():

    p1 = str(input("La persona de inicio es: "))
    pf = str(input("La persona a buscar es: "))
    tree = TreeNode(p1)
    dato = datos(p1)
    print(bdd(p1, pf, dato, tree))
    n = str(input("Si desea ver los nombres analizados presione 1 si no presione cualquier otra tecla: "))
    if n == "1":
        tree.travel()
    
main()
