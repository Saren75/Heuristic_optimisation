/* 
   Parte 2: un palet, varios niveles, pesos y capacidades
   Programación lineal entera mixta (x binarias; P, W, Gam continuas) */

/*Parámetros*/
param l, integer, >= 1;   # lado del palet
param h, integer, >= 1;  # número de niveles
param n := h * l * l;   # número de cajas

/* Conjuntos  */
set K := 1..n;   # cajas
set I := 1..l;   # filas (1 = fondo, l = acceso)
set J := 1..l;  # columnas
set M := 1..h;    # niveles (1 = inferior, h = superior)

param p{K}, >= 1;   # prioridad (1 = máxima)
param w{K}, >= 0;   # peso (omega_k), en gramos
param g{K}, >= 0;   # capacidad: peso máximo que soporta encima , en gramos

/* Variable de decisión  */
var x{K, I, J, M}, binary;    # nos da 1 si la caja k ocupa el hueco (i,j,m)

/* Variables auxiliares  */
var P{I, J, M}, >= 0; # prioridad de la caja en el hueco (i,j,m)
var W{I, J, M}, >= 0;  # peso de la caja en el hueco (i,j,m)
var Gam{I, J, M}, >= 0; # capacidad de la caja en el hueco (i,j,m)

/* Función objetivo */ 

minimize coste_medio:
    (1 / n) * sum{k in K, i in I, j in J, m in M} (i - 1) * p[k] * x[k,i,j,m];


/* Definición de las auxiliares (3*l^2*h restricciones)*/
s.t. defP{i in I, j in J, m in M}:
    P[i,j,m] = sum{k in K} p[k] * x[k,i,j,m];

s.t. defW{i in I, j in J, m in M}:
    W[i,j,m] = sum{k in K} w[k] * x[k,i,j,m];

s.t. defGam{i in I, j in J, m in M}:
    Gam[i,j,m] = sum{k in K} g[k] * x[k,i,j,m];

/*restricciones */
/*  cada hueco tiene exactamente una caja (l^2*h) */
s.t. cajaporhueco{i in I, j in J, m in M}:
    sum{k in K} x[k,i,j,m] = 1;

/*  cada caja está en exactamente un hueco (n) */
s.t. huecoporcaja{k in K}:
    sum{i in I, j in J, m in M} x[k,i,j,m] = 1;

/* orden por prioridad, dentro de cada columna y nivel (l*(l-1)*h) */
s.t. orden{i in 1..l-1, j in J, m in M}:
    P[i+1,j,m] <= P[i,j,m];

/* resistencia acumulada de todas las cajas de encima (l^2*(h-1)) */
s.t. resistencia{i in I, j in J, m in 1..h-1}:
    sum{mm in m+1..h} W[i,j,mm] <= Gam[i,j,m];


/*resolver*/
solve;

/* Salida */
printf "\nCoste medio = %.4f\n", coste_medio;
for {m in M} {
    printf "\nNivel %d (filas de fondo a acceso)\n", m;
    for {i in I} {
        for {j in J} {
            for {k in K: x[k,i,j,m] > 0.5} printf "  caja %2d", k;
        }
        printf "\n";
    }
}
printf "\n";

end;
