import subprocess
import sys
import re
import os

if len(sys.argv) != 3:
    print("Uso: python sol-4.py <fichero_in> <fichero_dat")
    sys.exit(1)
archivo_in = sys.argv[1]
archivo_dat = sys.argv[2]

nombre_archivo = os.pàth.splitext(archivo_in)[0]
archivo_out = f"{nombre_archivo}.out"

with open(archivo_in, "r",encoding="utf-8") as fichero:
    
    variables_pallet = fichero.readline().strip().split()
    
    l = int(variables_pallet[0]) #longitud de pallet
    h = int(variables_pallet[1]) #número de niveles
    P = int(variables_pallet[2]) #coste de montaje de un pallet
    
    
    prioridades_cajas = [int(x) for x in fichero.readline().strip().split()]
    pesos_cajas = [int(x) for x in fichero.readline().strip().split()]
    capacidades_cajas = [int(x) for x in fichero.readline().strip().split()]

with open(archivo_dat, "w", encoding="utf-8") as f_dat:
    f_dat.write(f"param l := {l};\n")
    f_dat.write(f"param h := {h};\n")
    f_dat.write(f"param P := {P};\n")
   
comando_glpk = ["glpsol", "-m", "parte_4.mod", "-d", archivo_dat]    

corriendo_glpk = subprocess.run(comando_glpk, capture_output = True, text = True)

if corriendo_glpk.returncode != 0:
    sys.exit(1)

resultados_raw = corriendo_glpk.stdout


    
    
"""
Aquí va el código que interpreta la salida y la convierte en un diccionario
todavia no lo podemos programar porque no sabemos que forma tendrá la salida 








"""
#ejemplo de como podría verse resultados
resultados = [
    {"caja": 1, "pallet": 1, "nivel": 1, "fila": 1, "columna": 1},
    {"caja": 2, "pallet": 1, "nivel": 1, "fila": 1, "columna": 2},
    {"caja": 3, "pallet": 1, "nivel": 2, "fila": 1, "columna": 1}
]

almacen={}

for x in resultados:
    num_caja = x["caja"]
    num_pallet = x["pallet"]
    num_nivel = x["nivel"]
    num_fila = x["fila"]
    num_columna = x["columna"]
    
    if num_pallet not in almacen:
        almacen [num_pallet] = {}
    if num_nivel not in almacen[num_pallet]:
        almacen[num_pallet][num_nivel]= {}
    if num_fila not in almacen[num_pallet][num_nivel]:
        almacen[num_pallet][num_nivel][num_fila] = {} 
    
     
    almacen[num_pallet][num_nivel][num_fila][num_columna]=num_caja
    
#codigo de salida y graficar

with open(archivo_out, "w", encoding = "utf-8") as f_out:

    for pallet, niveles in almacen.items():
        f_out.write(f"---Pallet {pallet}---\n")
        for nivel in range  (h,0,-1):
            f_out.write(f" --Nivel {nivel}--\n")
        
            if nivel in niveles:
                for fila, columnas in  niveles[nivel].items():
                    for columna, caja in columnas.items():
                        f_out.write(f"Caja {caja} en nivel {nivel} y coordenadas {fila}, {columna}\n ")
            
            else: 
                f_out.write("Nivel vacío\n")

f_out.write("\n")