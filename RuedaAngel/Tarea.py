import argparse

class Objeto:
    def __init__(self, num_lados, radio, ancho):
        self.num_lados = num_lados
        self.radio = radio
        self.ancho = ancho

    def __str__(self):
        return f"Objeto con {self.num_lados} lados, radio {self.radio} y ancho {self.ancho}"

def main():
    # Configurar los argumentos de línea de comandos
    parser = argparse.ArgumentParser()
    parser.add_argument("--num_lados", type=int, default=8, help="Número de lados del círculo")
    parser.add_argument("--radio", type=float, default=1, help="Radio del círculo")
    parser.add_argument("--ancho", type=float, default=0.5, help="Ancho de la rueda")
    args = parser.parse_args()

    # Crear el objeto
    objeto = Objeto(args.num_lados, args.radio, args.ancho)

    # Imprimir el objeto
    print(objeto)

if __name__ == "__main__":
    main()
