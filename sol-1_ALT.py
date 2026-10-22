#!/usr/bin/env python3
import sys
import subprocess
import re
import os

# Carpeta donde esta este script: aqui se busca el modelo y los ficheros sin ruta
DIR_SCRIPT = os.path.dirname(os.path.abspath(__file__))
MODELO = os.path.join(DIR_SCRIPT, "parte-1.mod")


def resolver_ruta(ruta):
    # Si el fichero no lleva ninguna ruta, se asume la carpeta del script (enunciado)
    if os.path.dirname(ruta) == "":
        return os.path.join(DIR_SCRIPT, ruta)
    return ruta


def main():
    if len(sys.argv) != 3:
        print("Uso incorrecto. Formato esperado: ./sol-1.py <fichero_entrada> <fichero_dat>")
        sys.exit(1)

    archivo_in = resolver_ruta(sys.argv[1])
    # El segundo argumento es el nombre exacto del fichero .dat que hay que generar
    archivo_dat = resolver_ruta(sys.argv[2])

    # Fichero con la solucion grafica: mismo nombre que el .dat pero con extension .out
    base_nombre = os.path.splitext(archivo_dat)[0]
    archivo_out = f"{base_nombre}.out"
    if archivo_out == archivo_dat:
        archivo_out = f"{base_nombre}.sol.out"

    try:
        with open(archivo_in, "r", encoding="utf-8") as f_in:
            linea_lado = f_in.readline().strip()
            if not linea_lado:
                print("Error: El fichero de entrada está vacío")
                sys.exit(1)

            l = int(linea_lado)

            linea_prioridades = f_in.readline().strip()
            prioridades = [int(p) for p in linea_prioridades.split()]

            if len(prioridades) != l * l:
                print(f"Error: Se esperaban {l*l} prioridades, pero se leyeron {len(prioridades)}")
                sys.exit(1)

        with open(archivo_dat, "w", encoding="utf-8") as f_dat:
            f_dat.write("data;\n\n")
            f_dat.write(f"param l := {l};\n\n")
            f_dat.write("param prioridad :=\n")
            for k in range(len(prioridades)):
                f_dat.write(f"{k+1} {prioridades[k]}\n")
            f_dat.write(";\n\nend;\n")

        comando_glpk = ["glpsol", "-m", MODELO, "-d", archivo_dat]

        resultado_proceso = subprocess.run(comando_glpk, capture_output=True, text=True)
        salida_consola_glpk = resultado_proceso.stdout

        if resultado_proceso.returncode != 0:
            print("Error durante la ejecución de GLPK:")
            print(salida_consola_glpk + resultado_proceso.stderr)
            sys.exit(1)

        if "INTEGER OPTIMAL SOLUTION FOUND" not in salida_consola_glpk:
            print("GLPK no ha encontrado una solución óptima (problema infactible o no acotado)")
            sys.exit(1)

        # Tamaño del problema: primera linea "N rows, M columns" (antes del preprocesado).
        # GLPK cuenta la funcion objetivo como una fila mas, por eso se resta 1.
        match_tam = re.search(r"(\d+) rows, (\d+) columns", salida_consola_glpk)
        num_restricciones = int(match_tam.group(1)) - 1
        num_variables = int(match_tam.group(2))

        # Valor objetivo y posiciones: lineas escritas con printf en parte-1.mod
        valor_objetivo = float(re.search(r"^OBJ (\S+)", salida_consola_glpk, re.M).group(1))

        print(f"{num_variables} {num_restricciones} {valor_objetivo:.2f}")

        matriz_solucion = [[0 for _ in range(l)] for _ in range(l)]
        for k_val, i_val, j_val in re.findall(r"^SOL (\d+) (\d+) (\d+)", salida_consola_glpk, re.M):
            matriz_solucion[int(i_val) - 1][int(j_val) - 1] = prioridades[int(k_val) - 1]

        with open(archivo_out, "w", encoding="utf-8") as f_out:
            f_out.write("DISPOSICION DEL PALLET (Vista Cenital)\n")
            f_out.write("======================================\n")
            f_out.write("Punto de acceso por la parte SUPERIOR (Fila " + str(l) + ")\n\n")

            for i in range(l - 1, -1, -1):
                f_out.write(f"Fila {i+1:>2} |")
                for j in range(l):
                    f_out.write(f" {matriz_solucion[i][j]:>5} |")
                f_out.write("\n")
                f_out.write("--------+" + "-" * (8 * l) + "\n")

            f_out.write("        |")
            for j in range(l):
                f_out.write(f" Col{j+1:>2} |")
            f_out.write("\n\n")
            f_out.write(f"Coste medio: {valor_objetivo:.4f}\n")

    except FileNotFoundError:
        print(f"Error: El archivo '{archivo_in}' no se pudo encontrar.")
        sys.exit(1)
    except Exception as e:
        print(f"Error inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
