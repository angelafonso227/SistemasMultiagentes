import sys
import math

def generate_model(cant_lados, radio, ancho):
    if (cant_lados < 3 or cant_lados > 360):
        cant_lados = 8
    if radio <= 0.0:
        radio = 1.0
    if ancho <= 0.0:
        ancho = 0.5

    vertices = []
    for i in range(cant_lados):
        angulo = ((2 * math.pi * i)/ cant_lados)
        x = (math.cos(angulo) * radio)
        y = (math.sin(angulo) * radio)
        vertices.append((x, y, 0.0))
        vertices.append((x, y, ancho))
    
    vertices.append((0.0, 0.0, ancho)) # Vértice de la base superior
    vertices.append((0.0, 0.0, 0.0)) # Vértice de la base inferior

    # Escribe el modelo en un archivo OBJ
    with open("ruedish.obj", "w") as file:
        file.write(f"#Vertices: {len(vertices)} \n")
        
        for vertice in vertices:
            file.write(f"v {vertice[0]:.3f} {vertice[1]:.3f} {vertice[2]:.3f} \n")
            
        file.write(f"#Normales: {cant_lados + 2} \n")
        
        for i in range(cant_lados):
            angulo = (2 * math.pi * i / cant_lados)
            x = math.cos(angulo)
            y = math.sin(angulo)
            file.write(f"vn {x:.3f} {y:.3f} 0.00000\n")
        
        file.write("vn 0.00000 0.00000 1.00000\n")
        file.write("vn 0.00000 0.00000 -1.00000\n")
        
        file.write(f"# Caras: {cant_lados * 2 + 2}\n")
        for i in range(cant_lados):
            Vector1 = (2 * i + 1)
            Vector2 = (2 * i + 2)
            Vector3 = (2 * ((i + 1) % cant_lados) + 2)
            Vector4 = (2 * ((i + 1) % cant_lados) + 1)
            
            
            file.write(f"f {Vector1}//{i+1} {Vector3}//{i+1} {Vector2}//{i+1}\n")
            file.write(f"f {Vector3}//{i+1} {Vector1}//{i+1} {Vector4}//{i+1}\n")
        
        for i in range(cant_lados):
            Vector1 = (2 * i + 1)
            Vector2 = (2 * ((i + 1) % cant_lados) + 1)
            file.write(f"f {len(vertices)}//{cant_lados+1} {Vector2}//{cant_lados+1} {Vector1}//{cant_lados+1}\n")
        
        for i in range(cant_lados):
            Vector1 = (2 * i + 2)
            Vector2 = (2 * ((i + 1) % cant_lados) + 2)
            file.write(f"f {len(vertices) - 1}//{cant_lados+2} {Vector1}//{cant_lados+2} {Vector2}//{cant_lados+2}\n")

# Verifica si el script se está ejecutando directamente
if __name__ == "__main__":
    if len(sys.argv) <= 4:
        cant_lados = 8
        radio = 1.0
        ancho = 0.5

    generate_model(cant_lados, radio, ancho)

    # Abre el archivo OBJ y muestra su contenido
    with open("ruedish.obj", "r") as file:
        print(file.read())