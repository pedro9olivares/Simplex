from Simplex import simplex_dos_fases
import numpy as np

# Número de variables
n = 6
# Número de restricciones
m = 4
# Costos
costos = [[-3.,-2,0,0,0,0]]
costos = np.array(costos)
# Restricciones
matriz = [[1.,1, 1,0,0,0],
          [3,1,  0,1,0,0],
          [1,0,  0,0,1,0],
          [0,1,  0,0,0,1]]
matriz = np.array(matriz)
# Recursos (añadir z_0 = 0 al final de la lista)
recursos = [[9.,18,7,6,0]]
recursos = np.array(recursos)

# Ejecución
resultados = simplex_dos_fases(m , n, matriz, costos, recursos, debug=False)
llaves = ['Tabla final', 'x', 'z', 'A\'', 'b\'', 'r']
resultados = dict(zip(llaves, resultados))

print(resultados['Tabla final'])
print(resultados['x'])
print(resultados['z'])