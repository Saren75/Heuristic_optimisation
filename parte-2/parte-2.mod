##
# Diseño para conseguir la solucion optima al problema de organizar una serie de cajas con una prioridad especifica en un pallet con varios niveles, manteniendo las normas de la parte 1 y añadiendo que cada caja tiene un peso y una capacidad de carga, de modo que ninguna puede soportar encima mas peso del que aguanta
##


/*Parámetros*/
param l, integer, >= 1;   #lado del pallet, parametro que viene dado en los datos
param h, integer, >= 1;   #numero de niveles que se montan sobre el pallet
param n := h * l^2;   #numero de cajas, el pallet se rellena siempre completamente en todos sus niveles



/*SETS*/
set CAJAS:=  1..n; #enumeracion de las cajas que sale de el numero de cajas que hay
set FILAS:= 1..l ;  # este set son las filas que van de 1 a l
set COLUMNAS:= 1..l ;# este set son las columnas que van de 1 a l
set NIVELES:= 1..h ;# este set son los niveles que van de 1 a h, el 1 es el de abajo y el h el de arriba

param prioridad {k in CAJAS}, integer, >= 1; # la prioridad dependiendo de cada caja
param peso {k in CAJAS}, >= 0; # el peso en gramos de cada caja
param capacidad {k in CAJAS}, >= 0; # el peso maximo en gramos que cada caja aguanta encima


/*Variables */
var P{i in FILAS, j in COLUMNAS, m in NIVELES} >= 0; #variable de prioridad en la posicion (i,j,m)

var W{i in FILAS, j in COLUMNAS, m in NIVELES} >= 0; #variable de peso en la posicion (i,j,m)

var Gam{i in FILAS, j in COLUMNAS, m in NIVELES} >= 0; #variable de capacidad en la posicion (i,j,m)

var x {k in CAJAS, i in FILAS, j in COLUMNAS, m in NIVELES} binary; # variable que nos da 1 si la caja K esta en (i,j,m)


/*Funcion objetivo */

minimize COSTE_TOTAL_MEDIO: 1/n * sum {k in CAJAS, i in FILAS, j in COLUMNAS, m in NIVELES} (i-1)*prioridad[k]*x[k,i,j,m]; #la funcion a minimizar es la suma del coste de todas las cajas entre el numero de estas, (i-1) son los huecos que pagan por cada caja



/*Restricciones*/
s.t. cajaporhueco {i in FILAS, j in COLUMNAS, m in NIVELES}: sum{k in CAJAS} x[k,i,j,m] = 1 ;#exactamente una caja en cada hueco asi no hay huecos vacios
s.t. huecoporcaja {k in CAJAS}: sum{i in FILAS, j in COLUMNAS, m in NIVELES} x[k,i,j,m] = 1 ;#restriccion que hace que cada caja este en un hueco solo, no en varios huecos a la vez
s.t. Orden {i in FILAS, j in COLUMNAS, m in NIVELES: i < l}: P[i,j,m] >= P[i+1,j,m];# restriccion que define la regla de orden por la que en una columna las cajas con mayor n de prioridad deben estar al fondo, el nivel queda libre porque las prioridades solo aplican dentro del mismo nivel
s.t. defprioridad {i in FILAS, j in COLUMNAS, m in NIVELES}: P[i,j,m] = sum {k in CAJAS} prioridad[k]*x[k,i,j,m]; # restriccion para la variable P, es la regla que define la variable
s.t. defpeso {i in FILAS, j in COLUMNAS, m in NIVELES}: W[i,j,m] = sum {k in CAJAS} peso[k]*x[k,i,j,m]; # restriccion para la variable W, es la regla que define la variable
s.t. defcapacidad {i in FILAS, j in COLUMNAS, m in NIVELES}: Gam[i,j,m] = sum {k in CAJAS} capacidad[k]*x[k,i,j,m]; # restriccion para la variable Gam, es la regla que define la variable
s.t. resistencia {i in FILAS, j in COLUMNAS, m in NIVELES: m < h}: sum{mm in NIVELES: mm > m} W[i,j,mm] <= Gam[i,j,m];# restriccion que obliga a que el peso de todas las cajas que hay encima en la misma fila y columna no pase de la capacidad de la caja de abajo, no hace falta para m = h porque arriba del todo no hay nada encima


/*Resolver*/
solve;

/*Salida de la solucion: lineas con prefijo fijo para que sol-2.py las lea facilmente*/
printf "OBJ %.6f\n", COSTE_TOTAL_MEDIO; # valor de la funcion objetivo
printf {k in CAJAS, i in FILAS, j in COLUMNAS, m in NIVELES: x[k,i,j,m] > 0.5} "SOL %d %d %d %d\n", k, i, j, m; # caja k colocada en la fila i, columna j, nivel m
end;