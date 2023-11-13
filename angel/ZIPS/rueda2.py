import sys
import math

def generarVertices(num_lados, radio, anchura_rueda):
    #verificamos que se cumplan con las reglas, si estas fallan se le asigan los valores propuestos
    if num_lados < 3 or num_lados > 360:
        num_lados = 8 #valor propuesto
    if radio <= 0.0:
        radio = 1.0 #valor propuesto
    if anchura_rueda <= 0.0:
        anchura_rueda = 0.5 #valor propuesto

    vertices = [] #lista de vertices que representan la rueda
    for i in range(num_lados):
        angle = 2 * math.pi * i / num_lados
        x = math.cos(angle) * radius
        y = math.sin(angle) * radius
        vertices.append((x, y, 0.0))
        vertices.append((x, y, anchura))

    vertices.append((0.0, 0.0, anchura))
    vertices.append((0.0, 0.0, 0.0))

    return vertices

# función para que se generen los vertices de la función pasada en OBJ
def escribirOBJ(vertices, num_lados):
    with open("ruedaPrueba.obj", "w") as obj_file:
        obj_file.write("# Modelado de la rueda\n")
        obj_file.write(f"# Vertices: {len(vertices)}\n")
        for vertex in vertices:
            obj_file.write(f"v {vertex[0]:.3f} {vertex[1]:.3f} {vertex[2]:.3f}\n")
        obj_file.write(f"# Normales: {num_lados + 2}\n")
        for i in range(num_lados):
            angle = 2 * math.pi * i / num_lados
            x = math.cos(angle)
            y = math.sin(angle)
            obj_file.write(f"vn {x:.3f} {y:.3f} 0.0000\n")
        
        obj_file.write("vn 0.0000 0.0000 1.0000\n")
        obj_file.write("vn 0.0000 0.0000 -1.0000\n")

        obj_file.write(f"# Caras: {num_lados * 2 + 2}\n")
        for i in range(num_lados):
            v1 = 2 * i + 1
            v2 = 2 * i + 2
            v3 = 2 * ((i + 1) % num_lados) + 2
            v4 = 2 * ((i + 1) % num_lados) + 1
            obj_file.write(f"f {v3}//{i+1} {v1}//{i+1} {v2}//{i+1}\n")
            obj_file.write(f"f {v3}//{i+1} {v4}//{i+1} {v1}//{i+1}\n")

        for i in range(num_lados):
            v1 = 2 * i + 1
            v2 = 2 * ((i + 1) % num_lados) + 1
            obj_file.write(f"f {len(vertices)}//{num_lados+1} {v1}//{num_lados+1} {v2}//{num_lados+1}\n")

        for i in range(num_lados):
            v1 = 2 * i + 2
            v2 = 2 * ((i + 1) % num_lados) + 2
            obj_file.write(f"f {len(vertices) - 1}//{num_lados+2} {v2}//{num_lados+2} {v1}//{num_lados+2}\n")

if __name__ == "__main__":
    if len(sys.argv) == 4:
        num_lados = int(sys.argv[1])
        radius = float(sys.argv[2])
        anchura = float(sys.argv[3])
    else:
        num_lados = 8
        radius = 1.0
        anchura = 0.5

    vertices = generarVertices(num_lados, radius, anchura)
    escribirOBJ(vertices, num_lados)

    with open("ruedaPrueba.obj", "r") as obj_file:
        print(obj_file.read())