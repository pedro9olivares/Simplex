# Simplex
Implementación del método Simplex (de dos fases) para el proyecto de Programación Lineal, primavera 2023.

Desarrollado por:
- Pedro Olivares 190198
- Sebastián Ibarra 193992
- Rodrigo Uribe 196134
- Claudio Guerrero 192617
- Juan Pablo Macías 192984

## Contenido
- [Cómo usar](#cómo-usar)
- [Explicación](#explicación)
- [Pseudocódigo](#pseudocódigo)
- [Problemas](#problemas)

## Cómo usar
1. Instalar numpy: `pip install numpy`.
2. Descargar el archivo `Simplex.py` y colocarlo en la misma carpeta donde se trabajará.
3. En un archivo de Python, importar el método Simplex de las dos fases (`from Simplex import simplex_dos_fases`), e importar numpy (`import numpy as np`).
4. Especificar los parámetros que usará el Simplex. Estos son `m`, el número de restricciones; `n`, el número de variables objetivo; `matriz`, una matriz de numpy que representa las restricciones del problema (sin recursos); `costos`, una matriz de numpy que representa el vector de costos y `recursos`, una matriz de numpy que representa el vector columna de recursos del problema (para que el método funcione, es necesario agregar manualmente un 0 al final de este vector, el cual representa la entrada z_0 de nuestra tabla Simplex).
5. Ejecutar `simplex_dos_fases()` con estos parámetros.

Ejemplo de uso:

<img width="444" alt="image" src="https://user-images.githubusercontent.com/61219691/234157265-1b3f6970-bf4a-4b2c-a2a3-dac25596121b.png">

Los resultados que regresa el método son: la **tabla Simplex final** (`np.array`), la solución óptima **x** (`np.array`), el valor de la función objetivo en la solución óptima **z** (`int`), la matriz de restricciones alterada **A'** (`np.array`), el vector de recursos alterado **b'** (`np.array`) y el vector de costos relativos **r** (`np.array`).

El parámetro `debug` en `True` hará que se impriman todas las tablas Simplex usadas para llegar a la solución (si existe). Si solo se desea obtener el resultado final, ponerlo en `False`.

Si el P.P.L. introducido es **no acotado,** se alza una excepción y el método no acaba. Si el P.P.L. tiene una **infinidad de soluciones óptimas,** se notifica al usuario y se regresa la primer solución óptima a la que se llegó.

## Explicación

Se decidió implementar el método Simplex de dos fases en Python por su simplicidad y por el poder que nos otorga el cálculo vectorizado la librería numpy. 

A su vez, se optó por implementar el método de las dos fases en lugar del método de la gran M por la posibilidad de modularizar el código: tener una implementación del Simplex estándar permitiría casi inmediatamente implementar el método de las dos fases, pues cada fase utiliza el Simplex, pero con diferentes parámetros.

### Supuestos
- Desarrollamos nuestros métodos pensando en que siempre se introducirán los P.P.L.s en su forma estándar.
- No manejamos problemas de programación lineal entera.
- Para el correcto funcionamiento del algoritmo, se debe agregar manualmente un 0 al vector de recursos; este representará el **z_0** en nuestra tabla Simplex inicial.

### Caveats
- Por cómo numpy maneja la aritmética de punto flotante, fue necesario introducir un redondeo manual cuando hay operaciones con resultados en el intervalo (-2 x 10^-15, 0). Numpy representa aquellos valores que están muy cerca del 0 (valores menores a -1 x 10^-16) como -0.0, lo que hacía al algoritmo fallar al momento de seleccionar qué variable habría de entrar; por ello fue necesario redondear. 
- Las matrices y arreglos de numpy deben ser de tipo `float`.

## Pseudocódigo

Nuestro módulo `Simplex.py` cuenta con tres funciones que están debidamente comentadas. Ellas son:

**Función para revisar si un arreglo de numpy es un vector canónico** `_is_canonical_vector(x: np.array) -> bool` 
1. Si el vector x tiene más de un elemento distinto a cero, regresa `False`.
2. Si el vector x tiene solo un elemento distinto a cero, pero este no es uno, regresa `False`.
3. En otro caso, regresa `True`.

**Función que resuelve un P.P.L. en su forma estándar via el método Simplex con regla de Bland** `simplex_estandar(m: int , n: int, matriz: np.array, costos: np.array, recursos: np.array, fase_1: bool = False, debug: bool = False) -> Tuple[np.array, np.array, int, np.array, np.array, np.array]`
1. Usando los parámetros `matriz`, `costos` y `recursos`, arma la tabla Simplex inicial.
2. Si `debug` está en `True`, imprimir en consola cada tabla que se vaya generando e indicar que variables entran y salen.
3. Pasar de la tabla incial a la tabla 1: apoyándose de la función `_is_canonical_vector()`, vuelve cero el costo relativos de las columnas canónicas.
4. Mientras haya costos relativos negativos, aplicar Simplex con regla de Bland.
    - Si ya se hicieron más de 100,000 iteraciones Simplex parar y alzar excepción: casi seguramente el problema es no acotado.
    - Obtener el índice de la columna entrante: aquella con costo relativo 0 y que esté más a la izquierda.
    - Obtener el índice del renglón que pivoteará: aquel con división positiva entre el correspondiente elemento de la columna de recursos menor. Si hay empate, seleccionar el índice menor entre estos.
    - Pivotear sobre la columna y renglón.
    - En el renglón de costos relativos, pasar de -0.0 a 0.0
5. Obtener la solución óptima.
    - Si hay más de `m` columnas básicas y no se está aplicando el método como **fase 1** (para esto, se utiliza una bandera booleana `fase_1`), imprimir en consola que existen infinitas soluciones óptimas.
    - En otro caso, imprimir en consola que se encontró una solución óptima y armar el vector correspondiente.
6. Regresar los resultados relevantes (la tabla Simplex final, la solución óptima x, el valor de la función objetivo en la solución óptima z, la matriz de restricciones alterada A', el vector de recursos alterado b' y el vector de costos relativos r).

**Función que implementa el método de las dos fases** `simplex_dos_fases(m: int , n: int, matriz: List[List[float]], costos: List[List[float]], recursos: List[List[float]], debug:bool = False) -> Tuple[np.array, np.array, int, np.array, np.array, np.array]`
1. Fase 1
    - Armar la tabla Simplex que contiene a la identidad gracias a las y's. 
    - Generar el vector de costos correspondiente a la suma de las y's.
    - Aplicar `simplex_estandar`, usando los dos objetos generados en lugar de `matriz` y `costos`: Si obtenemos que **z** es diferente de 0, parar,pues la región factible del P.P.L. es vacía. Si no, continuar a la Fase 2
2. Fase 2
    - Con la matriz **A'** y vector de recursos **b'** obtenidos de la Fase 1, correr Simplex y regresar sus resultados. 
 
 ## Problemas
 ### Problema A
 <img width="194" alt="image" src="https://user-images.githubusercontent.com/61219691/234179490-f1b66a2e-6fdc-4de7-89d5-e9c85a31515c.png">
 
 Una vez traducido a su forma estándar
 
 <img width="448" alt="image" src="https://user-images.githubusercontent.com/61219691/234362502-f52df373-b88b-46fa-9351-fa2631d9fd25.png">

obtenemos que se llega a un punto en el cual no podemos determinar sobre que renglón pivotear, pues la columna entrante tiene puras entradas negativas. Por lo tanto, alzamos una excepción y paramos (si intentamos elegir otra columna entrante más hacia la derecha, la regla de Bland se rompe y el Simplex cicla infinitamente).
 
 ### Problema B
 <img width="178" alt="image" src="https://user-images.githubusercontent.com/61219691/234179445-2b5f88d7-7c6b-437d-a55c-f66ccd07151a.png">
 
 Una vez traducido a su forma estándar
 
 <img width="513" alt="image" src="https://user-images.githubusercontent.com/61219691/234180324-4b6b05de-5d12-49ee-82bc-4aa5a7896fe1.png">
 
obtenemos que

<img width="379" alt="image" src="https://user-images.githubusercontent.com/61219691/234180372-79f1935e-f43e-4fa4-abdb-8fbeefe8d8ed.png">


 
 ### Problema C
 <img width="199" alt="image" src="https://user-images.githubusercontent.com/61219691/234179477-7ef07c79-f606-476f-984a-b22b4461b039.png">
 
 Una vez traducido a su forma estándar
 
 <img width="522" alt="image" src="https://user-images.githubusercontent.com/61219691/234183411-a267f7a8-ddb0-42d8-8ac6-7f0444485cb2.png">

obtenemos que 

<img width="390" alt="image" src="https://user-images.githubusercontent.com/61219691/234183466-dffd886a-ef8d-4caa-aef6-d6bff90eccaa.png">

## Ápendice
En esta sección ponemos algunos cálculos que estaban muy largos para ponerlos en la documentación principal.

<img width="470" alt="image" src="https://user-images.githubusercontent.com/61219691/234363421-66a97726-720f-4a46-af00-b894eb95ed6c.png">





