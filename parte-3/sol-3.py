#!/usr/bin/env python3
import subprocess
import sys
import re
import os

# El enunciado dice que una ruta sin directorio se asume relativa a la carpeta
# en la que se encuentra el script, no al directorio desde el que se invoca.
BASE = os.path.dirname(os.path.abspath(__file__))

def ruta(nombre):
    return nombre if os.path.dirname(nombre) else os.path.join(BASE, nombre)

if len(sys.argv) != 3:
    print("Uso: ./sol-3.py <fichero-entrada> <fichero-dat>", file=sys.stderr)
    sys.exit(1)

archivo_in = ruta(sys.argv[1])
archivo_dat = ruta(sys.argv[2])
archivo_mod = os.path.join(BASE, "parte-3.mod")

nombre_archivo = os.path.splitext(archivo_in)[0]
archivo_out = f"{nombre_archivo}.out"

try:
    with open(archivo_in, "r", encoding="utf-8") as fichero:

        variables_pallet = fichero.readline().strip().split()

        l = int(variables_pallet[0]) #longitud de pallet
        h = int(variables_pallet[1]) #numero maximo de niveles

        prioridades_cajas = [int(x) for x in fichero.readline().strip().split()]
        pesos_cajas = [int(x) for x in fichero.readline().strip().split()]
        capacidades_cajas = [int(x) for x in fichero.readline().strip().split()]

except (OSError, ValueError, IndexError) as error:
    print(f"Error leyendo el fichero de entrada {archivo_in}: {error}", file=sys.stderr)
    sys.exit(1)

# En la parte 3 el pallet puede quedar incompleto (1 <= n <= h*l^2)
n = len(prioridades_cajas)
if not (1 <= n <= h * l * l):
    print(f"Entrada incoherente: con l = {l} y h = {h} caben como mucho {h*l*l} cajas y hay {n}.", file=sys.stderr)
    sys.exit(1)

if len(pesos_cajas) != n or len(capacidades_cajas) != n:
    print(f"Entrada incoherente: hay {n} prioridades, {len(pesos_cajas)} pesos y {len(capacidades_cajas)} capacidades.", file=sys.stderr)
    sys.exit(1)

with open(archivo_dat, "w", encoding="utf-8") as f_dat:
    f_dat.write(f"param l := {l};\n")
    f_dat.write(f"param h := {h};\n\n")

    # el set de cajas va explicito porque n se saca de su cardinal
    f_dat.write("set CAJAS := " + " ".join(str(i) for i in range(1, n + 1)) + ";\n\n")

    f_dat.write("param prioridad := \n")
    for i, val in enumerate(prioridades_cajas, 1): f_dat.write(f"  {i} {val}\n")
    f_dat.write(";\n\n")

    f_dat.write("param peso := \n")
    for i, val in enumerate(pesos_cajas, 1): f_dat.write(f"  {i} {val}\n")
    f_dat.write(";\n\n")

    f_dat.write("param capacidad := \n")
    for i, val in enumerate(capacidades_cajas, 1): f_dat.write(f"  {i} {val}\n")
    f_dat.write(";\n")
    f_dat.write("end;\n")


comando_glpk = ["glpsol", "-m", archivo_mod, "-d", archivo_dat]

try:
    corriendo_glpk = subprocess.run(comando_glpk, capture_output = True, text = True)
except FileNotFoundError:
    print("No se encuentra 'glpsol'. Comprueba que GLPK esta instalado y en el PATH.", file=sys.stderr)
    sys.exit(1)

if corriendo_glpk.returncode != 0:
    print(f"glpsol ha fallado (codigo {corriendo_glpk.returncode}) con el modelo {archivo_mod}", file=sys.stderr)
    print(corriendo_glpk.stderr or corriendo_glpk.stdout, file=sys.stderr)
    sys.exit(1)

resultados_raw = corriendo_glpk.stdout

# en la parte 3 el problema puede no tener solucion: si hay que apilar y las
# capacidades no lo permiten, no cabe ninguna disposicion valida
salida = resultados_raw.upper()
if "NO INTEGER FEASIBLE" in salida or "NO PRIMAL FEASIBLE" in salida or "INFEASIBLE" in salida:
    print("El problema es infactible: las capacidades no permiten colocar todas las cajas.", file=sys.stderr)
    sys.exit(1)

busca_filas = re.search(r"(\d+)\s+rows", resultados_raw, re.IGNORECASE)
busca_variables = re.search(r"(\d+)\s+columns", resultados_raw, re.IGNORECASE)
busca_objetivo = re.search(r"OBJ\s+([\d\.]+)", resultados_raw)

if not (busca_filas and busca_variables and busca_objetivo):
    print("No se ha podido interpretar la salida de glpsol.", file=sys.stderr)
    print(resultados_raw, file=sys.stderr)
    sys.exit(1)

# GLPK cuenta como fila tambien la de la funcion objetivo, que no es una
# restriccion del modelo, por eso se descuenta.
num_restricciones = int(busca_filas.group(1)) - 1
num_variables = busca_variables.group(1)
val_objetivo = busca_objetivo.group(1)

print(f"{num_variables} {num_restricciones} {val_objetivo}")


almacen = {}

for linea in resultados_raw.splitlines():
    if linea.startswith("SOL"):
        partes = linea.split()
        caja = int(partes[1])
        fila = int(partes[2])
        columna = int(partes[3])
        nivel = int(partes[4])

        if nivel not in almacen:
            almacen[nivel] = {}
        if fila not in almacen[nivel]:
            almacen[nivel][fila] = {}

        almacen[nivel][fila][columna] = prioridades_cajas[caja - 1]


#graficacion usando vista cenital de cada nivel, los huecos vacios salen en blanco

with open(archivo_out, "w", encoding="utf-8") as f_out:
    f_out.write("--- DISPOSICIÓN DEL PALLET (Parte 3) ---\n")
    f_out.write(f"Punto de acceso por la parte superior (Fila {l})\n")
    f_out.write("Cada casilla muestra la prioridad de la caja alojada, los huecos vacios van con --\n")

    for nivel in range(h, 0, -1):
        f_out.write(f"\n -- Nivel {nivel} --\n")

        for fila in range(l, 0, -1):
            f_out.write(f"Fila {fila} | ")

            for columna in range(1, l + 1):
                if nivel in almacen and fila in almacen[nivel] and columna in almacen[nivel][fila]:
                    prioridad = almacen[nivel][fila][columna]
                    f_out.write(f"[{prioridad:^4}] ")
                else:
                    f_out.write("[ -- ] ")

            f_out.write("\n")