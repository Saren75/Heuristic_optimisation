import subprocess
import sys
import re
import os

if len(sys.argv) != 3:
    print("Uso: python sol-2.py <fichero_in> <fichero_dat>")
    sys.exit(1)
archivo_in = sys.argv[1]
archivo_dat = sys.argv[2]

nombre_archivo = os.path.splitext(archivo_in)[0]
archivo_out = f"{nombre_archivo}.out"

with open(archivo_in, "r",encoding="utf-8") as fichero:
    
    variables_pallet = fichero.readline().strip().split()
    
    l = int(variables_pallet[0]) #longitud de pallet
    h = int(variables_pallet[1]) #número de niveles
    
    
    
    prioridades_cajas = [int(x) for x in fichero.readline().strip().split()]
    pesos_cajas = [int(x) for x in fichero.readline().strip().split()]
    capacidades_cajas = [int(x) for x in fichero.readline().strip().split()]

    n = len(prioridades_cajas) 
    
with open(archivo_dat, "w", encoding="utf-8") as f_dat:
    f_dat.write(f"param l := {l};\n")
    f_dat.write(f"param h := {h};\n")
    f_dat.write(f"param n := {n};\n")

    f_dat.write("param p := \n")
    for i, val in enumerate(prioridades_cajas, 1): f_dat.write(f"  {i} {val}\n")
    f_dat.write(";\n\n")
    
    f_dat.write("param w := \n")
    for i, val in enumerate(pesos_cajas, 1): f_dat.write(f"  {i} {val}\n")
    f_dat.write(";\n\n")
    
    f_dat.write("param gamma := \n")
    for i, val in enumerate(capacidades_cajas, 1): f_dat.write(f"  {i} {val}\n")
    f_dat.write(";\n")
    
    
comando_glpk = ["glpsol", "-m", "parte-2.mod", "-d", archivo_dat]    

corriendo_glpk = subprocess.run(comando_glpk, capture_output = True, text = True)

if corriendo_glpk.returncode != 0:
    sys.exit(1)

resultados_raw = corriendo_glpk.stdout


    
    

#Aquí va el código que interpreta la salida y la convierte en un diccionario
 


try:
    num_restricciones = re.search(r"Rows:\s+(\d+)", resultados_raw).group(1)
    num_variables = re.search(r"Columns:\s+(\d+)", resultados_raw).group(1)
    val_objetivo = re.search(r"Objective:\s+.*=\s+([\d\.]+)", resultados_raw).group(1)
    
    print(f"{num_variables} {num_restricciones} {val_objetivo}")
except AttributeError:
    pass







almacen={}


#cambiar una cosa del mod para que esto funcione
for linea in resultados_raw.splitlines():
    if linea.startswith("RES_CAJA"):
        partes = linea.split()
        caja = int(partes[1])
        nivel = int(partes[2])
        fila = int(partes[3])
        columna = int(partes[4])
        
        if nivel not in almacen:
            almacen[nivel] = {}
        if fila not in almacen[nivel]:
            almacen[nivel][fila] = {}
        
        almacen[nivel][fila][columna] = caja
     
    
#codigo de salida y graficar

with open(archivo_out, "w", encoding="utf-8") as f_out:
    f_out.write("--- Pallet Único Completamente Lleno (Parte 2) ---\n")
    
    for nivel in range(h, 0, -1):
        f_out.write(f" -- Nivel {nivel} --\n")
        
        if nivel in almacen:
            for fila in sorted(almacen[nivel].keys()):
                for columna in sorted(almacen[nivel][fila].keys()):
                    caja = almacen[nivel][fila][columna]
                    f_out.write(f"Caja {caja} en coordenadas ({fila}, {columna})\n")
        else:
            f_out.write("Nivel vacío\n")
        f_out.write("\n")