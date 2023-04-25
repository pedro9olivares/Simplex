from typing import List, Tuple
import numpy as np
np.set_printoptions(precision=3, suppress=True) # Imprimimos en terminal hasta tres dígitos

"""
Código del algoritmo Simplex y del método de las dos fases para Programación Lineal (Prim. 2023)
Desarrollado por P. Olivares, J. Watson, R. Uribe, S. Ibarra y C. Guerrero. 
"""

# De estilo:
# para renglones, usar m, i
# para columnas, usar n, j

# TODO: Pasar de un PPL cualquiera a su forma estándar

def _is_canonical_vector(x):
    """
    Función privada para checar si un arreglo de numpy es vector canónico.
    Generada por ChatGPT.
    """
    # Check if the array has only one non-zero element
    if np.count_nonzero(x) != 1:
        return False
    # Check if the non-zero element is equal to 1
    if x[np.nonzero(x)[0][0]] != 1:
        return False
    
    return True

def simplex_estandar(m: int , n: int, matriz: np.array, 
               costos: np.array, recursos: np.array, fase_1: bool = False,
               debug: bool = False) -> Tuple[np.array, np.array, int, np.array, np.array, np.array]: 
    """
    Función que aplica el algoritmo Simplex a un PPL en forma estándar
    que contiene a la identidad en sus restricciones.

    Argumentos:
        m (int): número de renglones
        n (int): número de columnas
        matriz (np.array): matriz mxn que representa las
            restricciones del problema.
        costos (np.array): arreglo de tamaño n los costos de la
            función objetivo.
        recursos (np.array): arreglo de tamaño m con los recursos
            de las restricciones.
        fase_1 (bool): bandera a prender si se está programando
            el método de las dos fases.
        debug (bool): encender esta bandera si quiere que se imprima
            cada tabla en terminal.
    
    Regresa:
        Tupla que contiene:
        tabla_final (np.array): matriz resultante de aplicar Simplex.
        x (np.array): solución óptima. Si hay infinitas soluciones óptimas, 
            regresa la primera a la que llega y avisa en consola.
            Si el problema es no acotado, alza una excepción.
        z (int): valor de la función objetivo evaluada en la solución óptima.
        A (np.array): matriz resultante sin costos ni recursos.
        b (np.array): recursos resultantes
        r (np.array): costos relativos resultantes
    """
    # Acondicionamiento
    A = matriz
    A = np.append(A, costos, axis=0)
    A = np.append(A, recursos.transpose(), axis=1)

    if debug: print(A,', tabla 0\n')
    # Pasa de la tabla 0 a la tabla 1
    for j in range(n):
        if _is_canonical_vector(A[:-1,j]) and A[m,j] != 0:
            # Vuelve cero el costo relativo
            indice_renglon = np.nonzero(A[:-1,j])[0][0]
            A[m, :] = A[m, :]  + (-A[m,j])*A[indice_renglon,:]

    cont_tablas = 1
    
    # Simplex (con regla de Bland)
    # Aplica Simplex mientras haya costos relativos negativos
    while np.min(A[m,:-1]) < 0:
        # Si hacemos más de 100,000 iteraciones, alzamos una excepción
        # ya que el problema podría ser no acotado
        if cont_tablas > 100000: raise Exception('Parece ser que el problema es no acotado.')
        # Obtén el índice de la columna entrante
        entrante = np.argwhere(A[m,:-1] < 0)[0][0]
        # Obtén el índice del renglón a pivotear 
        divisiones = []
        divisiones_idx = []
        for p in np.where(A[:-1, entrante] > 0)[0]:
            divisiones.append(A[p,n] / A[p,entrante])
            divisiones_idx.append(p)
        # A su vez, si no pudimos hacer división porque todas las entradas eran negativas,
        # alzamos una excepción que indica que el problema es no acotado.
        try:
            pivote = divisiones_idx[divisiones.index(min(divisiones))]
        except ValueError:
            raise Exception('Parece ser que el problema es no acotado.')
        if debug: 
            print(A,f', tabla {cont_tablas}, entra col: {np.argwhere(A[m,:-1] < 0)[0][0]} sobre ren: {pivote}.\n') 
            cont_tablas += 1
        # Realiza el pivoteo
        A[pivote, :] = (1/A[pivote, entrante])*A[pivote, :]
        for i in range(m+1):
            if i != pivote:
                A[i, :] = A[i, :] + (-A[i,entrante])*A[pivote, :]
        # Para evitar bugs, pasamos de -0 a 0
        for j in range(len(A[m, :-1])):
            if A[m, j] > -2e-15 and A[m,j] < 0: 
                A[m, j] = 0
        if A[m, -1] > -2e-15 and A[m,-1] < 0: 
            A[m, -1] = 0

    if debug: print(A,f', tabla final\n') 
    tabla_final = A

    # Obtención de solución óptima
    x = np.zeros(n)
    columnas_basicas = np.where(A[m,:-1] == 0)[0]
    if len(columnas_basicas) > m and not fase_1:
        print('¡Existen infinitas soluciones óptimas!')
    elif not fase_1:
        print('Se encontró una solución óptima.')
    for j in columnas_basicas:
        indice_sol = np.argmax(A[:,j])
        x[j] = A[indice_sol,n]
    
    # Valor de la función objetivo en solución óptima
    z = -A[m,n]

    return tabla_final, x, z, A[:-1,:-1], A[:-1,n], A[m, :-1]

def simplex_dos_fases(m: int , n: int, matriz: List[List[float]], 
               costos: List[List[float]], recursos: List[List[float]],
               debug:bool = False) -> Tuple[np.array, np.array, int, np.array, np.array, np.array]:
    """
    Función que aplica el algoritmo de las dos fases a un PPL en forma estándar.

    Argumentos:
        m (int): número de renglones
        n (int): número de columnas
        matriz (np.array): matriz mxn que representa las
            restricciones del problema.
        costos (np.array): arreglo de tamaño n los costos de la
            función objetivo.
        recursos (np.array): arreglo de tamaño m con los recursos
            de las restricciones.
        debug (bool): encender esta bandera si quiere que se imprima
            cada tabla en terminal.
    
    Regresa:
        Tupla que contiene:
        tabla_final (np.array): matriz resultante de aplicar la fase 1 si paró, o la
            fase 2, si acabó.
        x (np.array): solución óptima.
        z (int): valor de la función objetivo evaluada en la solución óptima.
        A (np.array): matriz resultante sin costos ni recursos.
        b (np.array): recursos resultantes
        r (np.array): costos relativos resultantes
    """
    # Fase 1. Si la region factible es vacía, para y avisa.
    # Agregamos la identidad (las y's) a la matriz que nos dan
    matriz_con_y = np.append(matriz, np.eye(m), axis=1)
    # Generamos el vector de costos con 1's en las y's, 0's en lo demás
    costos_de_y = np.append(np.zeros(n), np.ones(m)).reshape(1,m+n)
    res_f1 = simplex_estandar(m,n+m,matriz_con_y, costos_de_y, recursos, fase_1=True, debug=debug)
    llaves = ['Tabla final', 'x', 'z', 'A\'', 'b\'', 'r']
    resultados_f1 = dict(zip(llaves, res_f1))
    if resultados_f1['z'] != 0:
        print(f'El método de las dos fases nos dice que la región factible es vacía. {resultados_f1["z"]}')
        return res_f1
    else:
        # Fase 2, te indica si hay infinitas soluciones óptimas o si el problema es no acotado.
        # A la matriz A le quitamos las m y's que agregamos
        matriz = resultados_f1['A\''][:,:-m]
        # Y al vector de recursos le damos formas de matriz, añadiendo que z_0 = 0
        recursos = np.append(resultados_f1['b\''],0).reshape(1,m+1)
        return simplex_estandar(m,n,matriz,costos,recursos,debug=debug)
    
     

"""
Pruebas
Cuida pasar todos los arreglos como arreglos de floats!
"""
"""
# ----- Simplex de forma estándar -----

print()
print('----- Simplex de forma estándar -----')
m = 3
n = 5

matriz = [[-7.,20,1,0,0],[9,10,0,1,0],[1,0,0,0,1]]
A = np.array(matriz)

costos = [[-18.,-20,0,0,0]]  
costos = np.array(costos)

recursos = [[20.,90,7,0]] # A recursos se añade manualmente z_0 = 0
recursos = np.array(recursos)

res = simplex_estandar(m , n, matriz, costos, recursos)
llaves = ['Tabla final', 'x', 'z', 'A\'', 'b\'', 'r']
resultados = dict(zip(llaves, res))

print(resultados['Tabla final'])
print(resultados['x'])
print(resultados['z'])

# ----- Método de las dos fases -----
print()
print('----- Simplex dos fases -----')

m = 3
n = 5

matriz = [[-1.,1,-1,0,0],[2,1,0,1,0],[1,1,0,0,1]]
A = np.array(matriz)

costos = [[-1.,-2,0,0,0]]  
costos = np.array(costos)

recursos = [[1.,4, 3, 0]] # A recursos se añade manualmente z_0 = 0
recursos = np.array(recursos)

res = simplex_dos_fases(m , n, matriz, costos, recursos, debug=False)
llaves = ['Tabla final', 'x', 'z', 'A\'', 'b\'', 'r']
resultados = dict(zip(llaves, res))

print(resultados['Tabla final'])
print(resultados['x'])
print(resultados['z'])
"""