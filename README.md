# Simplex
Implementación del método Simplex (de dos fases) para el proyecto de Progrmación Lineal (primavera 2023).

## Contenido
- [Cómo usar](#cómo-usar)
- [Explicación](#protos)
- [Pseudocódigo](#protos)

## Cómo usar
1. Instalar numpy: `pip install numpy`.
2. Descargar el archivo `Simplex.py` y colocarlo en la misma carpeta donde se trabajará.
3. En un archivo de Python, importar el método Simplex de las dos fases (`from Simplex import simplex_dos_fases`), e importar numpy (`import numpy as np`).
4. Especificar los parámetros que usará el Simplex. Estos son `m`, el número de restricciones; `n`, el número de variables objetivo; `matriz`, una matriz de numpy que representa las restricciones del problema (sin recursos); `costos`, una matriz de numpy que representa el vector de costos; `recursos`, una matriz de numpy que representa el vector columna de recursos del problema (para que el método funcione, es necesario agregar manualmente un 0 al final de este vector, el cual representa la entrada z_0 de nuestra tabla Simplex). 

Ejemplo de uso:

<img width="444" alt="image" src="https://user-images.githubusercontent.com/61219691/234157265-1b3f6970-bf4a-4b2c-a2a3-dac25596121b.png">

El parámetro `debug` en `True` hará que se impriman todas las tablas Simplex usadas para llegar a la solución (si existe). Si solo se desea obtener el resultado final, ponerlo en `False`.
Los resultados que regresa el método son: la **tabla Simplex final**, la solución óptima **x**, el valor de la función objetivo en la solución óptima **z**, la matriz de restricciones alterada **A'**, el vector de recursos alterado **b'** y el vector de costos relativos **r.**

Si el P.P.L. introducido es **no acotado,** se alza una excepción y el método no acaba. Si el P.P.L. tiene una **infinidad de soluciones óptimas,** se notifica al usuario y se regresa la primer solución óptima a la que se llegó.

## Explicación

Se decidió implementar el método Simplex de dos fases en Python por su simplicidad y por el poder que nos otorga el cálculo vectorizado la librería numpy. A su vez, se optó por implementar el método de las dos fases en lugar del método de la gran M por la posibilidad de modularizar el código: tener una implementación del Simplex estándar permitiría casi inmediatamente implementar el método de las dos fases, pues cada fase utiliza el Simplex con unas pocas restricciones.

### Supuestos
- Desarrollamos nuestros métodos pensando en que siempre se introducirán los P.P.L.s en su forma estándar.
- No manejamos problemas de programación lineal entera.
- Para el correcto funcionamiento del algoritmo, se debe agregar manualmente un 0 al vector de recursos; este representará el **z_0** en nuestra tabla Simplex inicial.

### Caveats
- Por cómo numpy maneja la aritmética de punto flotante, fue necesario introducir un redondeo manual cuando hay operaciones con resultados en el intervalo (-2 x 10^-15, 0). Numpy representa aquellos valores que están muy cerca del 0 (valores menores a -1 x 10^-16) como -0.0, lo que hacía al algoritmo fallar al momento de seleccionar qué variable habría de entrar; por ello fue necesario redondear. 

## Pseudocódigo

Nuestro módulo `Simplex.py` cuenta con tres funciones que están debidamente comentadas. Ellas son:

Función para revisar si un arreglo de numpy es un vector canónico: `is_canonical_vector(x: np.array) -> bool` 
1. Si el vector x tiene más de un elemento distinto a cero, regresa `False`.
2. Si el vector x tiene solo un elemento distinto a cero, pero este no es uno, regresa `False`.
3. En otro caso, regresa `True`.

Función que resuelve un P.P.L. en su forma estándar via el método Simplex con regla de Bland: `simplex_estandar(m: int , n: int, matriz: np.array, costos: np.array, recursos: np.array, fase_1: bool = False, debug: bool = False) -> Tuple[np.array, np.array, int, np.array, np.array, np.array]`
1. Usando los parámetros `matriz`, `costos` y `recursos`

