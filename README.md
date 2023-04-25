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
Los resultados que regresa el método son: la tabla Simplex final, la solución óptima x, el valor de la función objetivo en la solución óptima z, la matriz de restricciones alterada A', el vector de recursos alterado b' y el vector de costos relativos r.

Si el P.P.L. introducido es no acotado, se alza una excepción y el método no acaba. Si el P.P.L. tiene una infinidad de soluciones óptimas, se notifica al usuario y se regresa la primer solución óptima a la que se llegó.

## Explicación

## Pseudocódigo

