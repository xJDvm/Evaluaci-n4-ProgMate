    # Juan Valdes y Jennire Vetri


import pandas as np
from pulp import *
from pandas import DataFrame
from munkres import Munkres

"""
"""
flag = True

def aplicar_metodo_hungaro():
   
    # Pedir la cantidad de filas y columnas de la matriz de costos
    while True:
        try:
            m = int(input("Ingrese la cantidad de filas de la matriz de costos: "))
            n = int(input("Ingrese la cantidad de columnas de la matriz de costos: "))
            if m <= 0 or n <= 0:
                raise ValueError
            break
        except ValueError:
            print("Las cantidades deben ser números enteros positivos.")

    # Pedir la matriz de costos
    matriz_costos = []
    for i in range(m):
        fila = []
        for j in range(n):
            fila.append(int(input("Ingrese el costo de la fila {} y la columna {}: ".format(i + 1, j + 1))))
        matriz_costos.append(fila)

    # Crear instancia del algoritmo de asignación óptima de Munkres
    m = Munkres()

    # Aplicar el algoritmo de asignación óptima en la matriz de costos
    asignacion = m.compute(matriz_costos)

    # Obtener las asignaciones óptimas y los costos totales
    asignacion_optima = []
    costo_total = 0

    for row, col in asignacion:
        costo = matriz_costos[row][col]
        asignacion_optima.append((row, col))
        costo_total += costo

    # Devolver las asignaciones óptimas y el costo total
    return asignacion_optima, costo_total




def resolver_transporte():
    m = int(input("Ingrese la cantidad de ciudades de origen: "))
    n = int(input("Ingrese la cantidad de ciudades de destino: "))

    # Pedir los nombres de las ciudades
    origen = []
    destino = []
    for i in range(m):
        origen.append(input("Ingrese el nombre de la ciudad de origen {}: ".format(i + 1)))
    for i in range(n):
        destino.append(input("Ingrese el nombre de la ciudad de destino {}: ".format(i + 1)))

    # Pedir la oferta y demanda
    oferta = {}
    demanda = {}
    for i in origen:
        oferta[i] = int(input("Ingrese la oferta de la ciudad {}: ".format(i)))
    for i in destino:
        demanda[i] = int(input("Ingrese la demanda de la ciudad {}: ".format(i)))

    # Pedir la matriz de costos
    costo_envio = {}
    for i in origen:
        costo_envio[i] = {}
        for j in destino:
            costo_envio[i][j] = int(input("Ingrese el costo de envío de {} a {}: ".format(i, j)))


    ### Declaramos la función objetivo... nota que buscamos minimizar el costo(LpMinimize)
    prob = LpProblem('Transporte', LpMinimize)

    rutas = [(i,j) for i in origen for j in destino]
    cantidad = LpVariable.dicts('Cantidad de Envio',(origen,destino),0)
    prob += lpSum(cantidad[i][j]*costo_envio[i][j] for (i,j) in rutas)
    for j in destino:
        prob += lpSum(cantidad[i][j] for i in origen) == demanda[j]
    for i in origen:
        prob += lpSum(cantidad[i][j] for j in destino) <= oferta[i]
    ### Resolvemos e imprimimos el Status, si es Optimo, el problema tiene solución.
    prob.solve()
    print("Status:", LpStatus[prob.status], '\n')

    ### Imprimimos la solución
    for v in prob.variables():
        if v.varValue > 0:
            print(v.name, "=", v.varValue)
    print('\nEl costo mínimo es:', value(prob.objective), ' \n\n')


while (flag == True):
    selector = input('Seleccione un tipo de problema\n  1) Problema de transporte\n  2) Problema de asignacion\n  0) Salir\n')

    if (selector == '1'):
        resolver_transporte()
    elif (selector == '2'):
        asignacion_optima, costo_total = aplicar_metodo_hungaro()
        print("\nAsignación óptima:", asignacion_optima)
        print("Costo total:", costo_total, '\n')
    elif (selector == '0'):
        flag = False
    else:
        print(selector + ' No es un comando valido, intente nuevamente')