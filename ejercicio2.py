    # Juan Valdes y Jennire Vetri


from pulp import LpMinimize, LpProblem, LpStatus, LpVariable, lpSum, value

# Definición de datos
origen = ['A', 'B', 'C']
destino = ['1', '2', '3', '4']

oferta = {'A': 500, 'B': 700, 'C': 800}
demanda = {'1': 400, '2': 900, '3': 200, '4': 500}

costo_envio = {
    'A': {'1': 12, '2': 13, '3': 4, '4': 6},
    'B': {'1': 6, '2': 4, '3': 10, '4': 11},
    'C': {'1': 10, '2': 9, '3': 12, '4': 4}
}

# Crear el problema de optimización
prob = LpProblem('Transporte', LpMinimize)

# Definir rutas y variables de decisión
rutas = [(i, j) for i in origen for j in destino]
cantidad = LpVariable.dicts('Cantidad_de_Envio', (origen, destino), 0)

# Definir la función objetivo
prob += lpSum(cantidad[i][j] * costo_envio[i][j] for (i, j) in rutas), "Costo_Total"

# Agregar restricciones de demanda
for j in destino:
    prob += lpSum(cantidad[i][j] for i in origen) == demanda[j], f"Demanda_{j}"

# Agregar restricciones de oferta
for i in origen:
    prob += lpSum(cantidad[i][j] for j in destino) <= oferta[i], f"Oferta_{i}"

# Resolver el problema
prob.solve()

# Imprimir el estado del problema
print("Estado:", LpStatus[prob.status])

# Imprimir la solución
if LpStatus[prob.status] == 'Optimal':
    for i in origen:
        for j in destino:
            if cantidad[i][j].varValue > 0:
                print(f"Enviar {cantidad[i][j].varValue} unidades desde {i} a {j}")

    # Imprimir el costo total mínimo
    print('El costo mínimo es:', value(prob.objective))
else:
    print("No se encontró una solución óptima.")
