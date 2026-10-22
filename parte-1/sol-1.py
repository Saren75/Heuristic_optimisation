import subprocess
import sys
import re
import os

if len(sys.argv) != 3:
    print("Uso: python sol-1.py <fichero_in> <fichero_dat>")
    sys.exit(1)
    
archivo_in = sys.argv[1]
archivo_dat = sys.argv[2]

nombre_archivo = os.path.splitext(archivo_in)[0]
archivo_out = f"{nombre_archivo}.out"

with open(archivo_in, "r", encoding="utf-8") as fichero:
    
    variables_pallet = fichero.readline().strip().split()
    l = int(variables_pallet[0]) # longitud de pallet
    
    prioridades_cajas = [int(x) for x in fichero.readline().strip().split()]
    
    # En la parte 1 el pallet se rellena siempre completamente (n = l^2)
    n = len(prioridades_cajas)

with open(archivo_dat, "w", encoding="utf-8") as f_dat:
    f_dat.write(f"param l := {l};\n")
    f_dat.write(f"param n := {n};\n\n")

    f_dat.write("param p := \n")
    for i, val in enumerate(prioridades_cajas, 1):
        f_dat.write(f"  {i} {val}\n")
    f_dat.write(";\n")
    
comando_glpk = ["glpsol", "-m", "parte-1.mod", "-d", archivo_dat]    

corriendo_glpk = subprocess.run(comando_glpk, capture_output=True, text=True)

if corriendo_glpk.returncode != 0:
    sys.exit(1)

resultados_raw = corriendo_glpk.stdout

# Extracción de variables, restricciones y valor objetivo
try:
    num_restricciones = re.search(r"Rows:\s+(\d+)", resultados_raw).group(1)
    num_variables = re.search(r"Columns:\s+(\d+)", resultados_raw).group(1)
    val_objetivo = re.search(r"Objective:\s+.*=\s+([\d\.]+)", resultados_raw).group(1)
    
    print(f"{num_variables} {num_restricciones} {val_objetivo}")
except AttributeError:
    pass

almacen = {}

for linea in resultados_raw.splitlines():
    if linea.startswith("RES_CAJA"):
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
    f_out.write("Punto de acceso por la parte inferior (Fila 1)\n\n")
    
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