from random import randint
from random import random
from math import exp
from copy import copy
from copy import deepcopy
import json

# lista de productos, calorias y peso en respectivo orden
productos = ["manzana", "naranja", "pan_dulce",
             "refresco", "chocolate", "pera", "melon", "papitas"]
calorias = [52, 45, 276, 180, 250, 57, 300, 312]
peso = [0.15, 0.15, 0.169, 0.4, 0.052, 0.25, 0.9, 0.1]

# peso objetivo
pesoObjetivo = 1.4

# calorias objetivo
calsObjetivo = 800

# la temperatura inicial, se usa para el control del ciclo
# temperaturaInicial = 1000
temperaturaInicial = 100

# la temperatura objetivo, se usa para salir del ciclo
temperaturaObjetivo = 0.001

# controla que tan rapido se mueve el ciclo
factorEnfriamiento = 0.9

# cuenta de iteraciones del ciclo de metropolis por cada iteracion
iteracionesMetropolis = 100

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
    def __init__(self, prods: list):
        self.prods = prods
        self.cals = total_calorias(prods)
        self.grams = total_peso(prods)
        self.calificacion = self.calificar()

    def calificar(self):
        # en caso de que el peso o calorias
        # sea mayor al objetivo
        # se ajusta para considerar que tan cerca esta
        calificacionPeso = self.grams / pesoObjetivo
        calificacionCals = self.cals / calsObjetivo

        if self.grams > pesoObjetivo:
            calificacionPeso = 0

        if self.cals >= calsObjetivo:
            calificacionCals = 2 - calificacionCals
        else:
            calificacionCals = 0

        return (calificacionPeso + calificacionCals) / 2

    def __str__(self):
        selfDiccionario = {
            "prods": self.prods,
            "cals": self.cals,
            "grams": self.grams,
            "calificacion": self.calificacion,
        }
        return json.dumps(selfDiccionario)


def recocido():
    global mejorSolucion
    global solucionActual
    global temperatura

    solucionActual = generarSolucion()
    mejorSolucion = deepcopy(solucionActual)
    temperatura = temperaturaInicial

    def perturbar(original: Solucion):
        p = copy(original.prods)
        # selecciono un objeto random de la mochila para modificar
        productoAfectado = randint(0, len(p) - 1)
        # depende el valor que contenga lo cambio por el contrario
        p[productoAfectado] = 0 if p[productoAfectado] == 1 else 1
        return Solucion(p)

    def cicloMetropolis():
        global mejorSolucion
        global solucionActual
        global temperatura

        for n in range(0, iteracionesMetropolis):
            nuevaSolucion = perturbar(solucionActual)
            print(nuevaSolucion)

            diferencia = nuevaSolucion.calificacion - solucionActual.calificacion

            # si la diferencia es favorable
            # hago una coopea y la asigna a la solucion actual
            if diferencia > 0:
                solucionActual = deepcopy(nuevaSolucion)

                # si ademas esta nueva solucion es mejor a la anterior mejor guardada
                # la asigno como mejor
                if nuevaSolucion.calificacion > mejorSolucion.calificacion:
                    mejorSolucion = deepcopy(nuevaSolucion)
            else:
                # si no calculo su probabilidad
                probabilidadAceptacion = exp( diferencia / temperatura)
                # y si esta probabilidad es menor a un random
                # se acepta como la solucion
                if probabilidadAceptacion <= random():
                    solucionActual = deepcopy(nuevaSolucion)

    # print(mejorSolucion)

    # se sigue iterando y mandando a llamar hasta que la temperatura
    # alcance la temperatura objetico
    while temperatura > temperaturaObjetivo:
        cicloMetropolis()
        # se actualiza la temperatura para que no corra infinitamente
        # T = alpha * T
        temperatura = temperatura * factorEnfriamiento

    print("---")
    return mejorSolucion


def generarSolucion():
    prods = []
    for i in range(0, len(productos) - 1):
        prods.append(randint(0, 1))
    return Solucion(prods)


if __name__ == "__main__":
    test = recocido()
    print(test)