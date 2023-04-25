from Simplex import simplex_dos_fases
import numpy as np

# Número de variables
n = 8
# Número de restricciones
m = 4
# Costos
costos = [[3.,6,-1,2,0,0,0,0]]
costos = np.array(costos)
# Restricciones
matriz = [[1.,1,-1,0,-1,0,0,0],[1,1,2,3,0,1,0,0],[1,2,-1,2,0,0,1,0],[0,1,0,2,0,0,0,-1]]
matriz = np.array(matriz)
# Recursos (añadir z_0 = 0 al final de la lista)
recursos = [[2.,10,6,5,0]]
recursos = np.array(recursos)

# Ejecución
resultados = simplex_dos_fases(m , n, matriz, costos, recursos, debug=False)
llaves = ['Tabla final', 'x', 'z', 'A\'', 'b\'', 'r']
resultados = dict(zip(llaves, resultados))

print(resultados['Tabla final'])
print(resultados['x'])
print(resultados['z'])