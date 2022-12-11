from random import randint
from random import random
from random import randrange
from copy import copy
import json

# lista de productos, calorias y peso en respectivo orden
productos = ["manzana", "naranja", "pan_dulce",
             "refresco", "chocolate", "pera", "melon", "papitas"]
calorias = [52, 45, 276, 180, 250, 57, 300, 312]
peso = [0.15, 0.15, 0.169, 0.4, 0.052, 0.25, 0.9, 0.1]

# poblacion inicial
tamanioPoblacion = 50
# tasa de perdida de energia cinetica
tasaPerdidaEnergiaCinetica = 0.85
# energia cinetica inicial
energiaCineticaActual = 1000
# probabilidad de colision entre moleculas
probabilidadColisionIntermolecular = 0.5
# controlador de iteraciones
totalColisiones = 500
# probabilidad de usar descomposicion
umbralDescomposicion = 0.5
# probabilidad de usar sintesis
umbralSintesis = 0.5

# peso objetivo
pesoObjetivo = 1.4

# calorias objetivo
calsObjetivo = 800

# calcula el peso total de la mochila
def total_peso(prods: list):
    total = 0
    for x in range(len(prods)):
        total = total + (peso[x] * prods[x])
    return total

# calcula el peso total de las calorias
def total_calorias(prods: list):
    total = 0
    for x in range(len(prods)):
        total = total + (calorias[x] * prods[x])
    return total

class Solucion:
    def __init__(self, prods: list, enCinetica: float, enCineticaInicial: float):
        self.prods = prods
        self.cals = total_calorias(prods)
        self.grams = total_peso(prods)
        self.enCinetica = enCinetica
        self.enPotencial = self.calificar() * enCineticaInicial

    def calificar(self):
        # en caso de que el peso o calorias
        # sea mayor al objetivo
        # se ajusta para considerar que tan cerca esta
        calificacionPeso = self.grams / pesoObjetivo
        calificacionCals = self.cals / calsObjetivo

        if self.grams > pesoObjetivo:
            calificacionPeso = -calificacionPeso

        if self.cals >= calsObjetivo:
            calificacionCals = 2 - calificacionCals
        else:
            calificacionCals = -calificacionCals

        return (calificacionPeso + calificacionCals) / 2


    def __str__(self):
        selfDiccionario = {
            "prods": self.prods,
            "cals": self.cals,
            "grams": self.grams,
            "enCinetica": self.enCinetica,
            "enPotencial": self.enPotencial
        }

        return json.dumps(selfDiccionario)

def reaccionQuimica():
    global mejorSolucion
    global colisiones
    global bufferEnergia

    poblacion = []

    #se inicializa con la peor mochila que puede llegar a haber
    mejorSolucion = Solucion([0, 0, 0, 0, 0, 0, 0, 0], 0, -1)
    colisiones = 0
    bufferEnergia = 0

    #numero 4 de colision
    def sintesis(indice1: int, indice2: int):
        global mejorSolucion
        global colisiones
        global bufferEnergia

        #se inicializa la variable para despues sobreescribir el valor
        nuevaEstructura = []

        #del total de mi poblacion selecciono la posicion del indice seleccionado
        #se seleccionan las 2 posiciones de la mochila
        solucion1 = poblacion[indice1]
        solucion2 = poblacion[indice2]

        #itero sobre la solucion 1 para simular el choque
        ##y de manera random crear el nuevo atomo
        for i in range(0, len(solucion1.prods)):
            seleccionarArreglo = randint(0, 1)

            #para seleccionar el nuevo individui apartir del azar para ver cuall afecta
            if seleccionarArreglo:
                nuevaEstructura.append(solucion1.prods[i])
            else:
                nuevaEstructura.append(solucion2.prods[i])

        #almaceno esta solucion 
        nuevaSolucion = Solucion(nuevaEstructura, 0, energiaCineticaActual)

        #calculo que tan viable es con la formula
        # donde sumo las enerias potenciales y cineticas
        energiaOriginal = solucion1.enCinetica + solucion2.enCinetica + solucion1.enPotencial + solucion2.enPotencial
        energiaPotencialNueva = nuevaSolucion.enPotencial
        diferenciaEnergia = energiaOriginal - energiaPotencialNueva

        #condiciono el resultado para ver si es viable el intercambio
        if diferenciaEnergia >= 0:
        #si es mayor a 0 es porque la energia original
        #es mas que la energia nuevo
        #y se acepta el cambio
            if indice1 > indice2:
                # aqui se combinaron en la nueva y se eliminan los
                #antiguos indivuduis padres
                del poblacion[indice1]
                del poblacion[indice2]
            else:
                del poblacion[indice2]
                del poblacion[indice1]

            nuevaSolucion.enCinetica = diferenciaEnergia
            #guardo la nueva solucion en la poblacion
            poblacion.append(nuevaSolucion)

            #aqui checamos si la solucion es mejor que la ideal
            #hasta el momento
            if nuevaSolucion.enPotencial > mejorSolucion.enPotencial:
                mejorSolucion = copy(nuevaSolucion)

            colisiones = colisiones + 1

    #numero 3 de colicion
    def intermolecularInefectiva(indice1: int, indice2: int):
        global mejorSolucion
        global colisiones
        global bufferEnergia

        solucion1 = poblacion[indice1]
        solucion2 = poblacion[indice2]

        #para saber en que punto chocaron y como fue la afectacion
        productoAfectado = randint(0, len(solucion1.prods) - 1)

        #es un back up del objeto original
        #por si el cambio se rachaza
        prods1 = copy(solucion1.prods)
        prods2 = copy(solucion2.prods)

        #en este ternario es para hacer los cambios a las particulas
        #si tiene 0 se convierte a 1 y biceversa
        prods1[productoAfectado] = 0 if prods1[productoAfectado] == 1 else 1
        prods2[productoAfectado] = 0 if prods2[productoAfectado] == 1 else 1

        #califican las soluciones
        nuevaSolucion1 = Solucion(prods1, solucion1.enCinetica, energiaCineticaActual)
        nuevaSolucion2 = Solucion(prods2, solucion2.enCinetica, energiaCineticaActual)

        #igual comparo con la formula que tan viable es la suma de las energias 
        #de las moleculas y comparo con la suma de enerfgias de la molecula 2 modificada
        #w prima
        energiaOriginal = solucion1.enCinetica + solucion2.enCinetica + solucion1.enPotencial + solucion2.enPotencial
        energiaPotencialNueva = nuevaSolucion1.enPotencial + nuevaSolucion2.enPotencial

        diferenciaEnergia = energiaOriginal - energiaPotencialNueva

        #para ver si el cambio se puede aceptar
        if diferenciaEnergia >= 0:
            tasaTransferencia = random()

            #para la energia cinetica restante
            #se reparte entre las moleculas al azar
            nuevaSolucion1.enCinetica = diferenciaEnergia * tasaTransferencia
            nuevaSolucion2.enCinetica = diferenciaEnergia * (1 - tasaTransferencia)

            #como la solucion es viable se sobrescribe en la poblacion
            poblacion[indice1] = nuevaSolucion1
            poblacion[indice2] = nuevaSolucion2

            #checo si las nuevas soluciones son mejor a la antiua mejor
            if nuevaSolucion1.enPotencial >= mejorSolucion.enPotencial:
                mejorSolucion = copy(nuevaSolucion1)
            #igual
            if nuevaSolucion2.enPotencial >= mejorSolucion.enPotencial:
                mejorSolucion = copy(nuevaSolucion2)

            colisiones = colisiones + 1

    #numero 2 de colision
    def descomposicion(indice: int):
        global mejorSolucion
        global colisiones
        global bufferEnergia

        solucion = poblacion[indice]

        colisionPosible = True

        prods1 = []
        prods2 = []

        #parte del atomo original se conserva
        puntoMedio = len(solucion.prods) / 2
        #se suman las energias 
        energiaOriginal = solucion.enCinetica + solucion.enPotencial

        #aqui se llenan las nuevas listas de productos
        for i in range(0, len(solucion.prods)):
            productoAleatorio = randint(0, 1)
            #la primera mitas se le pone al producto 1
            #mas se llena la segunda lista al azar
            if i < puntoMedio:
                prods1.append(solucion.prods[i])
                prods2.append(productoAleatorio)
            else:
                #biceversa
                prods1.append(productoAleatorio)
                prods2.append(solucion.prods[i])

        #se generan las soluciones
        nuevaSolucion1 = Solucion(prods1, solucion.enPotencial, energiaCineticaActual)
        nuevaSolucion2 = Solucion(prods2, solucion.enPotencial, energiaCineticaActual)

        energiaPotencialNueva = nuevaSolucion1.enPotencial + nuevaSolucion2.enPotencial
        diferenciaEnergia = energiaOriginal - energiaPotencialNueva

        #se evaluan las soluciones
        if diferenciaEnergia >= 0:
            tasaTransferencia = random()
            #para la energia cinetica restante
            #se reparte entre las moleculas al azar
            nuevaSolucion1.enCinetica = diferenciaEnergia * tasaTransferencia
            nuevaSolucion2.enCinetica = diferenciaEnergia * (1 - tasaTransferencia)

        elif diferenciaEnergia + bufferEnergia >= 0:
            #si las molecuas por si solas no tiene suficiente energia
            #pero esta energia esta en el buffer se acepta el cambio
            tasa1 = random()
            tasa2 = random()
            tasa3 = random()
            tasa4 = random()
            
            # y se reparte al azar entre las 4
            nuevaSolucion1.enCinetica = (diferenciaEnergia + bufferEnergia) * tasa1 * tasa2
            nuevaSolucion2.enCinetica = (diferenciaEnergia + bufferEnergia) * tasa3 * tasa4

            #almaceno la energia perdida en el buffer para la descomposicion para saber
            #si mantenemos el cambio
            bufferEnergia = bufferEnergia + diferenciaEnergia - nuevaSolucion1.enCinetica - nuevaSolucion2.enCinetica
        else:
            #
            colisionPosible = False

        #
        if colisionPosible:
            del poblacion[indice]
            #si el cambio es viable se guardan en la poblacion
            poblacion.append(nuevaSolucion1)
            poblacion.append(nuevaSolucion2)
            #se evaluan para ver si son mejores a las actualmente mejor
            if nuevaSolucion1.enPotencial >= mejorSolucion.enPotencial:
                mejorSolucion = copy(nuevaSolucion1)

            if nuevaSolucion2.enPotencial >= mejorSolucion.enPotencial:
                mejorSolucion = copy(nuevaSolucion2)

            colisiones = colisiones + 1

    #numero 1 de colision
    def paredInefectiva(indice: int):
        global mejorSolucion
        global colisiones
        global bufferEnergia

        solucion = poblacion[indice]
        #de mi poblacion eligo  la que tiene esa posicion
        #y de manera random selecciono un bite para ser modificado
        # para generar el nuevo individuo 
        productoAfectado = randint(0, len(solucion.prods) - 1)
        #se coopea para en caso que no sea viable no se soobrescriba
        nuevaEstructura = copy(solucion.prods)
        #aqui checo que valor tiene esa posicion y la cambio por el valor contrario
        nuevaEstructura[productoAfectado] = 0 if nuevaEstructura[productoAfectado] == 1 else 1

        #instancio mi nueva molecula y paso las energias
        nuevaSolucion = Solucion(nuevaEstructura, solucion.enCinetica, energiaCineticaActual)

        energiaOriginal = solucion.enCinetica + solucion.enPotencial
        # verifico y comparo las energias para aceptar el cambio
        if energiaOriginal >= nuevaSolucion.enPotencial:
            diferenciaEnergia = energiaOriginal - nuevaSolucion.enPotencial
            #obtengo el KElostRate
            tasaPerdidaEnergia = randrange(tasaPerdidaEnergiaCinetica * 100, 99) / 100
            #que es el maximo porcentace de perdida
            nuevaSolucion.enCinetica = diferenciaEnergia * tasaPerdidaEnergia
            #guardo la energia perdida en el buffer para saber si mantengo el cambio
            bufferEnergia = bufferEnergia + diferenciaEnergia * (1 - tasaPerdidaEnergia)

            poblacion[indice] = nuevaSolucion

            if nuevaSolucion.enPotencial > mejorSolucion.enPotencial:
                mejorSolucion = copy(nuevaSolucion)
            colisiones = colisiones + 1

    #seleccionar una mochila de la poblacion de manera random
    def obtenerSolucion():

        return randint(0, len(poblacion) - 1)

    #se selecciona al azar el tipo de colicion que seleccionara
    def colisionar():
        #se obtiene la probabilidad con random de la colision
        tipoColision = random()

        #si esta probabilidad es menor a .5
        #determina si es colicion intermolecular
        if tipoColision < probabilidadColisionIntermolecular:
            #inicializo las moleculas que voy a usar
            indice1 = obtenerSolucion()
            indice2 = obtenerSolucion()

            
            while indice1 == indice2:
                indice2 = obtenerSolucion()

            #igual saco un numero rando para ver 
            #que tan viable es la sintensis
            viabilidadSintesis = random()

            if viabilidadSintesis < umbralSintesis:
                sintesis(indice1, indice2)
            else:
                intermolecularInefectiva(indice1, indice2)
        else:
            #
            indice = obtenerSolucion()

            viabilidadDescomposicion = random()

            if viabilidadDescomposicion < umbralDescomposicion:
                descomposicion(indice)
            else:
                paredInefectiva(indice)

    while len(poblacion) < tamanioPoblacion:
        nuevaSolucion = generarSolucion()
        poblacion.append(nuevaSolucion)

        if mejorSolucion is None or nuevaSolucion.enPotencial >= mejorSolucion.enPotencial:
            mejorSolucion = copy(nuevaSolucion)

    while colisiones < totalColisiones:
        colisionar()
    return mejorSolucion

#selecciona productos aleatorios de la mochila
def generarSolucion():
    prods = []

    for i in range(0, len(productos)):
        prods.append(randint(0, 1))

    return Solucion(prods, energiaCineticaActual, energiaCineticaActual)

if __name__ == "__main__":
    test = reaccionQuimica()
    print(test)