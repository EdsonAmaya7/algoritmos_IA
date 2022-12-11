from random import randint

# lista de productos, calorias y peso en respectivo orden
productos = ["manzana", "naranja", "pan_dulce",
             "refresco", "chocolate", "pera", "melon", "papitas"]
calorias = [52, 45, 276, 180, 250, 57, 300, 312]
peso = [0.15, 0.15, 0.169, 0.4, 0.052, 0.25, 0.9, 0.1]
# numero de generaciones a usar
generaciones = 4
# numero de individuos por generacion
Indies = 16
# numero de productos
numIndiv = 8
# el punto donde cruzare las cadenas en este caso a la mitad
puntoCruza = 4

# esta clase define cada producto como un producto individual con sus atributos
class Producto:
    # inicializar los atributos del objeto
    def __init__(self, prods: list):
        self.prods = prods
        self.cals = total_calorias(prods)
        self.grams = total_peso(prods)

# calcula el peso total de la mochila
def total_peso(prods: list):
    total = 0
    for x in range(numIndiv):
        if (prods[x] == 1):
            total = total + peso[x]
    return total

# calcula el peso total de las calorias
def total_calorias(prods: list):
    total = 0
    for x in range(numIndiv):
        if (prods[x] == 1):
            total = total + calorias[x]
    return total

# genera una lista aleatoria de 0 y 1
# para formar individuos nuevos de la mochiña
def random():
    valores = []
    for x in range(numIndiv):
        valores.append(randint(0, 1))
    return valores

# recibe como argumentos dos listas de productos y los cruza generando dos individuos nuevos
def cruza(ind1: Producto, ind2: Producto):
    Tlist1 = ind1.prods
    Tlist2 = ind2.prods
    sl1 = Tlist1[0:puntoCruza]
    sl2 = Tlist1[puntoCruza:numIndiv]
    sl3 = Tlist2[0:puntoCruza]
    sl4 = Tlist2[puntoCruza:numIndiv]
    indr1 = Producto(sl1+sl4)
    indr2 = Producto(sl3+sl2)
    return indr1, indr2

# funcion principal
# que crea un diccionario
# donde guardan los individuos
# cada individuo es una generacion
def genetico():
    global puntoCruza
    generacion_guarda = {}
    generacion_guarda[0] = []

    # itero sobre los integrantes
    # de las generaciones y los guardo en la posicion 0
    # para guardar la primera generacion
    for g in range(Indies):
        IndX = Producto(random())
        generacion_guarda[0].append(IndX)
    print("Primera Generacion")
    imprimir(generacion_guarda[0])

    # sobre escribo el punto donde voy a cruzar
    # los individuos que generare
    # por cada generacion
    # y los guardo
    for x in range(1, generaciones):
        puntoCruza = randint(0, numIndiv-1)
        print("Punto de cruce en la posición: "+str(puntoCruza))
        generacion_guarda[x] = []
        apuntador = 0

        while apuntador < Indies:
            Indy1, Indy2 = cruza(generacion_guarda[x-1][apuntador],
                                 generacion_guarda[x-1][apuntador+1])
            generacion_guarda[x].append(Indy1)
            generacion_guarda[x].append(Indy2)
            apuntador = apuntador + 2
        print("Generación "+str(x+1))
        imprimir(generacion_guarda[x])
    mejorOpcion(generacion_guarda)

# busca la mejor opcion entre todos las generaciones
# implementa la funcion mejor en lista para sacar los mejores
def mejorOpcion(gen_guard: dict):
    valores = []
    for key in gen_guard:
        # gaurdo en valores la mejor generacion
        valores.extend(mejor_en_lista(gen_guard[key]))
    print("Mejores de todas las generaciones:")
    imprimir(valores)

# busca los mejores individuos de cada lista y los guarda en una lista
def mejor_en_lista(Inds: list):
    res = [x for x in Inds if x.cals >= 800 and x.grams <= 1.4]
    res = sorted(res, key=lambda x: x.cals, reverse=True)
    mejor_ejemplo = res[0]
    mejor = [x for x in res if x.cals == mejor_ejemplo.cals]
    if len(mejor) > 1:
        mejor = sorted(mejor, key=lambda x: x.grams)
        return mejor
    else:
        return [mejor_ejemplo]

# itera sobre las lista y los imprime en consola
def imprimir(Inds: list):
    datos = []
    for x in range(len(Inds)):
        ejemplo = []
        ejemplo += Inds[x].prods
        ejemplo.append(Inds[x].cals)
        ejemplo.append(Inds[x].grams)
        datos.append(ejemplo)
    # productos calorias kilos
    print(datos)

if __name__ == "__main__":
    genetico()