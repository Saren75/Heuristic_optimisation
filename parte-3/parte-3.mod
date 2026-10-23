##
# Diseño para conseguir la solucion optima al problema de organizar cajas en un pallet de varios niveles cuando el numero de cajas puede ser menor que el numero de huecos, de modo que pueden quedar posiciones vacias, que tienen capacidad 0, prioridad infinita y coste 0, y sobre las que no se puede poner ninguna caja aunque si otras posiciones vacias
##


/*Parámetros*/
param l, integer, >= 1;   #lado del pallet, parametro que viene dado en los datos
param h, integer, >= 1;   #numero maximo de niveles que se montan sobre el pallet



/*SETS*/
set CAJAS; #enumeracion de las cajas, viene dada en los datos porque ahora n no se calcula
set FILAS:= 1..l ;  # este set son las filas que van de 1 a l
set COLUMNAS:= 1..l ;# este set son las columnas que van de 1 a l
set NIVELES:= 1..h ;# este set son los niveles que van de 1 a h, el 1 es el de abajo y el h el de arriba

param n := card(CAJAS); #numero de cajas, se saca del cardinal del set para que no pueda descuadrar con las listas de datos

param prioridad {k in CAJAS}, integer, >= 1; # la prioridad dependiendo de cada caja
param peso {k in CAJAS}, >= 0; # el peso en gramos de cada caja
param capacidad {k in CAJAS}, >= 0; # el peso maximo en gramos que cada caja aguanta encima


/*Parámetros derivados, se calculan solos para no perder generalidad*/
param prioridad_max := max{k in CAJAS} prioridad[k]; #la peor prioridad que hay en la instancia
param prioridad_inf := prioridad_max + 1; #valor finito con el que representamos el infinito del hueco vacio
param beta {i in FILAS: i < l} := (l - i) * prioridad_max; #cota del coste que puede acumular un hueco de la fila i


/*Variables */
var y{i in FILAS, j in COLUMNAS, m in NIVELES} >= 0, <= 1; #variable de ocupacion, 1 si el hueco (i,j,m) tiene caja y 0 si esta vacio

var P{i in FILAS, j in COLUMNAS, m in NIVELES} >= 0; #variable de prioridad a efectos de coste en la posicion (i,j,m), 0 si esta vacio

var Q{i in FILAS, j in COLUMNAS, m in NIVELES} >= 0; #variable de prioridad a efectos de orden en la posicion (i,j,m), prioridad_inf si esta vacio

var W{i in FILAS, j in COLUMNAS, m in NIVELES} >= 0; #variable de peso en la posicion (i,j,m)

var Gam{i in FILAS, j in COLUMNAS, m in NIVELES} >= 0; #variable de capacidad en la posicion (i,j,m)

var c{i in FILAS, j in COLUMNAS, m in NIVELES: i < l} >= 0; #coste imputado al hueco (i,j,m), no hace falta en la fila de acceso porque ahi no hay nadie delante


var x {k in CAJAS, i in FILAS, j in COLUMNAS, m in NIVELES} binary; # variable que nos da 1 si la caja K esta en (i,j,m)


/*Funcion objetivo */

minimize COSTE_TOTAL_MEDIO: 1/n * sum {i in FILAS, j in COLUMNAS, m in NIVELES: i < l} c[i,j,m]; #la funcion a minimizar es la suma del coste de todos los huecos entre el numero de cajas


/*Restricciones*/
s.t. ocupacion {i in FILAS, j in COLUMNAS, m in NIVELES}: sum{k in CAJAS} x[k,i,j,m] = y[i,j,m] ;#restriccion que sustituye a la de la parte 2, ahora un hueco puede tener una caja o ninguna, y la cota y<=1 es la que impide que tenga mas de una
s.t. huecoporcaja {k in CAJAS}: sum{i in FILAS, j in COLUMNAS, m in NIVELES} x[k,i,j,m] = 1 ;#restriccion que hace que cada caja este en un hueco solo, los huecos pueden sobrar pero las cajas hay que colocarlas todas
s.t. Orden {i in FILAS, j in COLUMNAS, m in NIVELES: i < l}: Q[i,j,m] >= Q[i+1,j,m];# restriccion de orden igual que en la parte 2 pero sobre Q, que ademas obliga a que los huecos ocupados de cada columna y nivel formen un bloque pegado al acceso y los vacios queden al fondo
s.t. defprioridad {i in FILAS, j in COLUMNAS, m in NIVELES}: P[i,j,m] = sum {k in CAJAS} prioridad[k]*x[k,i,j,m]; # restriccion para la variable P, da 0 si el hueco esta vacio
s.t. defpeso {i in FILAS, j in COLUMNAS, m in NIVELES}: W[i,j,m] = sum {k in CAJAS} peso[k]*x[k,i,j,m]; # restriccion para la variable W, da 0 si el hueco esta vacio
s.t. defcapacidad {i in FILAS, j in COLUMNAS, m in NIVELES}: Gam[i,j,m] = sum {k in CAJAS} capacidad[k]*x[k,i,j,m]; # restriccion para la variable Gam, da 0 si el hueco esta vacio, que es la capacidad que el enunciado le da a la posicion vacia
s.t. resistencia {i in FILAS, j in COLUMNAS, m in NIVELES: m < h}: sum{mm in NIVELES: mm > m} W[i,j,mm] <= Gam[i,j,m];# restriccion que obliga a que el peso de todas las cajas que hay encima en la misma fila y columna no pase de la capacidad de la caja de abajo
s.t. defQ {i in FILAS, j in COLUMNAS, m in NIVELES}: Q[i,j,m] = P[i,j,m] + prioridad_inf * (1 - y[i,j,m]); # restriccion que traduce que la prioridad de un hueco vacio es infinita, si hay caja queda Q=P y si no queda Q=prioridad_inf
s.t. apoyo {i in FILAS, j in COLUMNAS, m in NIVELES: m < h}: y[i,j,m+1] <= y[i,j,m];# restriccion que impide poner una caja encima de un hueco vacio, pero deja que encima de un hueco vacio haya otro hueco vacio
s.t. defcoste {i in FILAS, j in COLUMNAS, m in NIVELES: i < l}: c[i,j,m] >= sum{t in i+1..l} P[t,j,m] - beta[i] * (1 - y[i,j,m]);# restriccion que da el coste del hueco, si hay caja es la suma de las prioridades de delante y si esta vacio el termino de correccion lo deja en 0


/*Resolver*/
solve;

/*Salida de la solucion: lineas con prefijo fijo para que sol-3.py las lea facilmente*/
printf "OBJ %.6f\n", COSTE_TOTAL_MEDIO; # valor de la funcion objetivo
printf {k in CAJAS, i in FILAS, j in COLUMNAS, m in NIVELES: x[k,i,j,m] > 0.5} "SOL %d %d %d %d\n", k, i, j, m; # caja k colocada en la fila i, columna j, nivel m
end;