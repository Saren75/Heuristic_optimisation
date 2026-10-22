import subprocess
import sys
import re
import os

if len(sys.argv) != 3:
    print("Uso: python sol-4.py <fichero_in> <fichero_dat>")
    sys.exit(1)
archivo_in = sys.argv[1]
archivo_dat = sys.argv[2]

nombre_archivo = os.path.splitext(archivo_in)[0]
archivo_out = f"{nombre_archivo}.out"

with open(archivo_in, "r",encoding="utf-8") as fichero:
    
    variables_pallet = fichero.readline().strip().split()
    
    l = int(variables_pallet[0]) #longitud de pallet
    h = int(variables_pallet[1]) #número de niveles
    P = int(variables_pallet[2]) #coste de montaje de un pallet
    
    
    prioridades_cajas = [int(x) for x in fichero.readline().strip().split()]
    pesos_cajas = [int(x) for x in fichero.readline().strip().split()]
    capacidades_cajas = [int(x) for x in fichero.readline().strip().split()]
    n = len(prioridades_cajas)
with open(archivo_dat, "w", encoding="utf-8") as f_dat:
    f_dat.write(f"param l := {l};\n")
    f_dat.write(f"param h := {h};\n")
    f_dat.write(f"param P := {P};\n")
    f_dat.write(f"param n := {n};\n\n")

    f_dat.write("param p := \n")
    for i, val in enumerate(prioridades_cajas, 1):
        f_dat.write(f"  {i} {val}\n")
    f_dat.write(";\n\n")
    
    f_dat.write("param w := \n")
    for i, val in enumerate(pesos_cajas, 1):
        f_dat.write(f"  {i} {val}\n")
    f_dat.write(";\n\n")
    
    f_dat.write("param gamma := \n")
    for i, val in enumerate(capacidades_cajas, 1):
        f_dat.write(f"  {i} {val}\n")
    f_dat.write(";\n")
comando_glpk = ["glpsol", "-m", "parte-4.mod", "-d", archivo_dat]    

corriendo_glpk = subprocess.run(comando_glpk, capture_output = True, text = True)

if corriendo_glpk.returncode != 0:
    sys.exit(1)

resultados_raw = corriendo_glpk.stdout



try:
    num_restricciones = re.search(r"Rows:\s+(\d+)", resultados_raw).group(1)
    num_variables = re.search(r"Columns:\s+(\d+)", resultados_raw).group(1)
    val_objetivo = re.search(r"Objective:\s+.*=\s+([\d\.]+)", resultados_raw).group(1)
    
    print(f"{num_variables} {num_restricciones} {val_objetivo}")
except AttributeError:
    pass
almacen={}

for linea in resultados_raw.splitlines():
    if linea.startswith("RES_CAJA"):
        partes = linea.split()
        caja = int(partes[1])
        pallet = int(partes[2])
        nivel = int(partes[3])
        fila = int(partes[4])
        columna = int(partes[5])
        
        if pallet not in almacen:
            almacen[pallet] = {}
        if nivel not in almacen[pallet]:
            almacen[pallet][nivel] = {}
        if fila not in almacen[pallet][nivel]:
            almacen[pallet][nivel][fila] = {}
            
        almacen[pallet][nivel][fila][columna] = caja
#codigo de salida y graficar

with open(archivo_out, "w", encoding="utf-8") as f_out:
    for pallet in sorted(almacen.keys()):
        f_out.write(f"--- Pallet {pallet} ---\n")
        
        for nivel in range(h, 0, -1):
            f_out.write(f" -- Nivel {nivel} --\n")
            
            if nivel in almacen[pallet]:
                for fila in sorted(almacen[pallet][nivel].keys()):
                    for columna in sorted(almacen[pallet][nivel][fila].keys()):
                        caja = almacen[pallet][nivel][fila][columna]
                        f_out.write(f"Caja {caja} en coordenadas ({fila}, {columna})\n")
            else: 
                f_out.write("Nivel vacío\n")
        f_out.write("\n")