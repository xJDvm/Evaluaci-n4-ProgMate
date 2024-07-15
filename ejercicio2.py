import pandas as np
from pulp import *
from pandas import DataFrame

### Ciudades
origen = ['A','B','C']
destino = ['1','2','3','4']

oferta = {'A': 500, 'B' : 700, 'C':800}
demanda = {'1': 400, '2' : 900, '3':200, '4':500}

costo_envio ={'A':{'1': 12, '2' : 13, '3': 4, '4':6},
             'B':{'1': 6, '2' : 4, '3': 10, '4':11},
             'C':{'1': 10, '2' : 9, '3': 12, '4':4}}

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
print("Status:", LpStatus[prob.status])

### Imprimimos la solución
for v in prob.variables():
    if v.varValue > 0:
        print(v.name, "=", v.varValue)
print('El costo mínimo es:', value(prob.objective))