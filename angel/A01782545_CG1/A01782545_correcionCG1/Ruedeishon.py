"""
Generacion de .obj de una rueda
Tarea CG1
Angel Afonso A01782545
2023-11-28
"""

import sys
import math

def calcular_normales(v1, v2, v3):
    vector1 = (v2[0] - v1[0], v2[1] - v1[1], v2[2] - v1[2])
    vector2 = (v3[0] - v1[0], v3[1] - v1[1], v3[2] - v1[2])
    normal = (vector1[1] * vector2[2] - vector1[2] * vector2[1],
              vector1[2] * vector2[0] - vector1[0] * vector2[2],
              vector1[0] * vector2[1] - vector1[1] * vector2[0])
    longitud = math.sqrt(normal[0]**2 + normal[1]**2 + normal[2]**2)
    return (normal[0] / longitud, normal[1] / longitud, normal[2] / longitud)

def generar_rueda(cantLados, radio, ancho):
    angulo_multi = 2 * math.pi / cantLados
    vertices = []

    for i in range(cantLados):
        angulo = angulo_multi * i
        y = radio * math.cos(angulo)
        z = radio * math.sin(angulo)
        vertices.extend([(ancho / 2, y, z), (-ancho / 2, y, z)])

    vertices.extend([(ancho / 2, 0, 0), (-ancho / 2, 0, 0)])

    caras = []
    normales = {}

    for i in range(0, cantLados * 2, 2):
        indiceFrontal, indiceAtras = i, i + 1
        indiceFrontalNxt, indiceAtrasNxt = (i + 2) % (cantLados * 2), (i + 3) % (cantLados * 2)

        n1 = calcular_normales(vertices[indiceFrontal], vertices[indiceAtras], vertices[indiceFrontalNxt])
        n2 = calcular_normales(vertices[indiceAtras], vertices[indiceAtrasNxt], vertices[indiceFrontalNxt])

        caras.extend([(indiceFrontal, indiceAtras, indiceFrontalNxt), (indiceAtras, indiceAtrasNxt, indiceFrontalNxt)])

        if n1 not in normales:
            normales[n1] = len(normales) + 1

        if n2 not in normales:
            normales[n2] = len(normales) + 1

    centroFrontal, centroAtras = cantLados * 2, cantLados * 2 + 1

    for i in range(0, cantLados * 2, 2):
        indiceFrontal, indiceFrontalNxt = i, (i + 2) % (cantLados * 2)

        normalFrontal = calcular_normales(vertices[centroFrontal], vertices[indiceFrontal], vertices[indiceFrontalNxt])
        normalAtras = calcular_normales(vertices[centroAtras], vertices[indiceFrontalNxt + 1], vertices[indiceFrontal + 1])

        caras.extend([(centroFrontal, indiceFrontal, indiceFrontalNxt), (centroAtras, indiceFrontalNxt + 1, indiceFrontal + 1)])

        if normalFrontal not in normales:
            normales[normalFrontal] = len(normales) + 1

        if normalAtras not in normales:
            normales[normalAtras] = len(normales) + 1

    with open("ruedish.obj", 'w') as file:
        file.write("# OBJ file\n")
        for vertex in vertices:
            file.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")
        for n, indice in normales.items():
            file.write(f"vn {n[0]} {n[1]} {n[2]}\n")
        for i, f in enumerate(caras):
            file.write(f"f {f[0]+1}//{normales[calcular_normales(vertices[f[0]], vertices[f[1]], vertices[f[2]])]} "
                       f"{f[1]+1}//{normales[calcular_normales(vertices[f[1]], vertices[f[2]], vertices[f[0]])]} "
                       f"{f[2]+1}//{normales[calcular_normales(vertices[f[2]], vertices[f[0]], vertices[f[1]])]}\n")

    with open("ruedish.obj", "r") as file:
        print(file.read())

if __name__ == "__main__":
    cantLados = 8
    radioCircu = 1.0
    anchoRueda = 0.5

    generar_rueda(cantLados, radioCircu, anchoRueda)
