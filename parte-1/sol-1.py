import sys
import subprocess
import re
import os

def main():
    if len(sys.argv) != 3:
        print("Uso incorrecto. Formato esperado: python sol-1.py <fichero_entrada> <fichero_salida>")
        sys.exit(1)    
    
    archivo_in = sys.argv[1] 
    archivo_out = sys.argv[2]
    
    
    base_nombre = os.path.splitext(archivo_out)[0]
    archivo_dat = f"{base_nombre}.dat"
    archivo_temp_glpk = f"{base_nombre}_glpk_out.txt"
    
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
            f_dat.write(f"param l := {l};\n\n")
            f_dat.write("param prioridad :=\n")
            for k in range(len(prioridades)):
                f_dat.write(f"{k+1} {prioridades[k]}\n")
            f_dat.write(";\n")

        
        comando_glpk = [
            "glpsol", 
            "-m", "parte-1.mod", 
            "-d", archivo_dat, 
            "-o", archivo_temp_glpk 
        ]
        
        
        resultado_proceso = subprocess.run(comando_glpk, capture_output=True, text=True)
        salida_consola_glpk = resultado_proceso.stdout
        
        if resultado_proceso.returncode != 0:
            print("Error durante la ejecución de GLPK:")
            print(resultado_proceso.stderr)
            sys.exit(1)

        
        num_variables = 0
        num_restricciones = 0
        valor_objetivo = 0.0
        
        match_vars = re.search(r"(\d+)\s+variables?", salida_consola_glpk)
        if match_vars:
            num_variables = match_vars.group(1)
            
        match_restr = re.search(r"(\d+)\s+constraints?", salida_consola_glpk)
        if match_restr:
            num_restricciones = match_restr.group(1)
            
        match_obj = re.search(r"Objective:\s+\w+\s+=\s+([+-]?\d+\.?\d*)", salida_consola_glpk)
        if match_obj:
            valor_objetivo = match_obj.group(1)
            
        print(f"{num_variables} {num_restricciones} {valor_objetivo}")

        
        matriz_solucion = [[0 for _ in range(l)] for _ in range(l)]
        
        with open(archivo_temp_glpk, "r") as f_sol:
            for linea in f_sol:
            
                if "x[" in linea:
        
                    match_x = re.search(r"x\[(\d+),(\d+),(\d+)\]\s+\*?\s+([01])", linea)
                    if match_x:
                        k_val = int(match_x.group(1))
                        i_val = int(match_x.group(2))
                        j_val = int(match_x.group(3))
                        valor_binario = int(match_x.group(4))
                        
                        if valor_binario == 1:
                            prioridad_caja = prioridades[k_val - 1]
                            matriz_solucion[i_val - 1][j_val - 1] = prioridad_caja

        
        with open(archivo_out, "w", encoding="utf-8") as f_out:
            f_out.write("DISPOSICION DEL PALLET (Vista Cenital)\n")
            f_out.write("======================================\n")
            f_out.write("Punto de acceso por la parte SUPERIOR (Fila " + str(l) + ")\n\n")
            

            for i in range(l - 1, -1, -1):
                f_out.write("Fila " + str(i+1) + " |")
                for j in range(l):
                    f_out.write(f" {matriz_solucion[i][j]:>4} |")
                f_out.write("\n")
                f_out.write("-------+" + "-" * (7 * l) + "\n")
            
    
            f_out.write("       |")
            for j in range(l):
                f_out.write(f" Col{j+1:>2} |")
            f_out.write("\n")

        
        if os.path.exists(archivo_temp_glpk):
            os.remove(archivo_temp_glpk)

    except FileNotFoundError:
        print(f"Error: El archivo '{archivo_in}' no se pudo encontrar.")https://blitzapp.gg/v3.0.12/premium?utm_source=blitz&utm_medium=ad&utm_campaign=blitz_ad_1&ref=ad-1
        sys.exit(1)
    except Exception as e:
        print(f"Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()