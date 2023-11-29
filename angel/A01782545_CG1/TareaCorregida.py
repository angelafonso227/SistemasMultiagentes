import sys
import math


def calculate_normal(v1, v2, v3):
    Vector1 = (v2[0] - v1[0], v2[1] - v1[1], v2[2] - v1[2])
    Vector2 = (v3[0] - v1[0], v3[1] - v1[1], v3[2] - v1[2])
    normal = (Vector1[1]*Vector2[2] - Vector1[2]*Vector2[1], Vector1[2]*Vector2[0] - Vector1[0]*Vector2[2], Vector1[0]*Vector2[1] - Vector1[1]*Vector2[0])
    length = math.sqrt(normal[0]**2 + normal[1]**2 + normal[2]**2)
    return (normal[0]/length, normal[1]/length, normal[2]/length)


def verticesGenerator(lados, radio, ancho):
    vertices = []
    angle_increment = 2 * math.pi / lados
    for i in range(lados):
        angulo = angle_increment * i
        y = radio * math.cos(angulo)
        z = radio * math.sin(angulo)
        # Frontal y Trasera
        vertices.extend([(ancho / 2, y, z), (-ancho / 2, y, z)])
    # Centro frontal y Centro trasero
    vertices.extend([(ancho / 2, 0, 0), (-ancho / 2, 0, 0)])
    return vertices


def facesNormals(vertices, lados):
    caras = []
    normales = {}
    for i in range(0, lados * 2, 2):
        indiceFrontal, indiceAtras = i, i + 1
        indiceFrontalNext, indiceAtrasNext = (i + 2) % (lados * 2), (i + 3) % (lados * 2)

        n1 = calculate_normal(vertices[indiceFrontal], vertices[indiceAtras], vertices[indiceFrontalNext])
        n2 = calculate_normal(vertices[indiceAtras], vertices[indiceAtrasNext], vertices[indiceFrontalNext])

        caras.extend([(indiceFrontal, indiceAtras, indiceFrontalNext), (indiceAtras, indiceAtrasNext, indiceFrontalNext)])

        if n1 not in normales:
            normales[n1] = len(normales) + 1

        if n2 not in normales:
            normales[n2] = len(normales) + 1

    frontalCentro, atrasCentro = lados * 2, lados * 2 + 1
    for i in range(0, lados * 2, 2):
        indiceFrontal, indiceFrontalNext = i, (i + 2) % (lados * 2)

        normalFrontal = calculate_normal(vertices[frontalCentro], vertices[indiceFrontal], vertices[indiceFrontalNext])
        normalAtras = calculate_normal(vertices[atrasCentro], vertices[indiceFrontalNext + 1], vertices[indiceFrontal + 1])

        caras.extend([(frontalCentro, indiceFrontal, indiceFrontalNext), (atrasCentro, indiceFrontalNext + 1, indiceFrontal + 1)])

        if normalFrontal not in normales:
            normales[normalFrontal] = len(normales) + 1

        if normalAtras not in normales:
            normales[normalAtras] = len(normales) + 1

    return caras, normales


def objFile(filename, vertices, caras, normales):
    with open(filename, 'w') as file:
        file.write("# OBJ file\n")
        for vertex in vertices:
            file.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")
        for n, indice in normales.items():
            file.write(f"vn {n[0]} {n[1]} {n[2]}\n")
        for i, f in enumerate(caras):
            file.write(f"f {f[0]+1}//{normales[calculate_normal(vertices[f[0]], vertices[f[1]], vertices[f[2]])]} "
                       f"{f[1]+1}//{normales[calculate_normal(vertices[f[1]], vertices[f[2]], vertices[f[0]])]} "
                       f"{f[2]+1}//{normales[calculate_normal(vertices[f[2]], vertices[f[0]], vertices[f[1]])]}\n")


lados = 8
radio = 1.0
ancho = 0.5

# Generar vértices y caras
vertices = verticesGenerator(lados, radio, ancho)
caras, normales = facesNormals(vertices, lados)

# Escribir el archivo OBJ
objFile("ruedilla.obj", vertices, caras, normales)
