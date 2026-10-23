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
    print("Uso: ./sol-1.py <fichero-entrada> <fichero-dat>", file=sys.stderr)
    sys.exit(1)

archivo_in = ruta(sys.argv[1])
archivo_dat = ruta(sys.argv[2])
archivo_mod = os.path.join(BASE, "parte-1.mod")

# El fichero de solucion grafica se deriva del SEGUNDO argumento (el de datos) y no
# del de entrada. El enunciado permite que el fichero de datos lleve el nombre y la
# extension que se quiera, de modo que derivarlo de la entrada puede hacer que el .out
# sobrescriba al propio fichero de datos (p. ej. ./sol-N.py ejemplo.in ejemplo.out),
# que el enunciado prohibe borrar. Si el fichero de datos ya termina en .out se usa .sol.
raiz_salida, extension_datos = os.path.splitext(archivo_dat)
archivo_out = f"{raiz_salida}.out" if extension_datos.lower() != ".out" else f"{raiz_salida}.sol"

try:
    with open(archivo_in, "r", encoding="utf-8") as fichero:

        # Se descartan las lineas en blanco para que una linea vacia intercalada no
        # desplace la lectura de las filas siguientes.
        lineas = [linea for linea in fichero if linea.strip()]

        variables_pallet = lineas[0].split()
        l = int(variables_pallet[0]) # longitud de pallet

        prioridades_cajas = [int(x) for x in lineas[1].split()]

except (OSError, ValueError, IndexError) as error:
    print(f"Error leyendo el fichero de entrada {archivo_in}: {error}", file=sys.stderr)
    sys.exit(1)

# En la parte 1 el pallet se rellena siempre completamente (n = l^2)
n = len(prioridades_cajas)
if n != l * l:
    print(f"Entrada incoherente: con l = {l} hacen falta {l*l} prioridades y hay {n}.", file=sys.stderr)
    sys.exit(1)

with open(archivo_dat, "w", encoding="utf-8") as f_dat:
    f_dat.write(f"param l := {l};\n\n")
    f_dat.write("param prioridad := \n")
    for i, val in enumerate(prioridades_cajas, 1):
        f_dat.write(f"  {i} {val}\n")
    f_dat.write(";\n")
    f_dat.write("end;\n")

comando_glpk = ["glpsol", "-m", archivo_mod, "-d", archivo_dat]

try:
    corriendo_glpk = subprocess.run(comando_glpk, capture_output=True, text=True)
except FileNotFoundError:
    print("No se encuentra 'glpsol'. Comprueba que GLPK esta instalado y en el PATH.", file=sys.stderr)
    sys.exit(1)

if corriendo_glpk.returncode != 0:
    print(f"glpsol ha fallado (codigo {corriendo_glpk.returncode}) con el modelo {archivo_mod}", file=sys.stderr)
    print(corriendo_glpk.stderr or corriendo_glpk.stdout, file=sys.stderr)
    sys.exit(1)

resultados_raw = corriendo_glpk.stdout

# GLPK anuncia la infactibilidad con dos prefijos distintos segun donde se detecte:
# "PROBLEM HAS NO PRIMAL FEASIBLE SOLUTION" si la detecta el preprocesado y
# "LP HAS NO PRIMAL FEASIBLE SOLUTION" si ya lo es la relajacion lineal. Se comprueba
# el sufijo comun para reconocer ambos casos, y tambien el de la fase entera.
salida_mayus = resultados_raw.upper()
if ("HAS NO PRIMAL FEASIBLE SOLUTION" in salida_mayus
        or "NO INTEGER FEASIBLE SOLUTION" in salida_mayus
        or "HAS NO DUAL FEASIBLE SOLUTION" in salida_mayus):
    print("El problema es infactible para esta instancia.", file=sys.stderr)
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

        if fila not in almacen:
            almacen[fila] = {}

        almacen[fila][columna] = prioridades_cajas[caja - 1]

#graficacion usando vista cenital

with open(archivo_out, "w", encoding="utf-8") as f_out:
    f_out.write("--- DISPOSICIÓN DEL PALLET (Parte 1) ---\n")
    f_out.write(f"Punto de acceso por la parte superior (Fila {l})\n\n")

    for fila in range(l, 0, -1):
        f_out.write(f"Fila {fila} | ")

        if fila in almacen:
            for columna in range(1, l + 1):
                if columna in almacen[fila]:
                    prioridad = almacen[fila][columna]
                    f_out.write(f"[{prioridad:^4}] ")
                else:
                    f_out.write("[ -- ] ")
        else:
            f_out.write("[ -- ] " * l)

        f_out.write("\n")