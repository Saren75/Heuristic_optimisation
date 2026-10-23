##
# Diseño para conseguir la solucion optima al problema de organizar cajas cuando hay una cantidad ilimitada de pallets disponibles, cada uno con un maximo de h niveles y con las mismas normas de la parte 3, pero donde montar cada pallet cuesta una cantidad fija, de modo que ahora se minimiza el coste total y no el medio
##


/*Parámetros*/
param l, integer, >= 1;   #lado del pallet, parametro que viene dado en los datos
param h, integer, >= 1;   #numero maximo de niveles de cada pallet
param coste_palet, >= 0;   #coste fijo de preparar un pallet, el enunciado lo llama P pero aqui P ya es la variable de prioridad



/*SETS*/
set CAJAS; #enumeracion de las cajas, viene dada en los datos porque n no se calcula
set FILAS:= 1..l ;  # este set son las filas que van de 1 a l
set COLUMNAS:= 1..l ;# este set son las columnas que van de 1 a l
set NIVELES:= 1..h ;# este set son los niveles que van de 1 a h, el 1 es el de abajo y el h el de arriba

param n := card(CAJAS); #numero de cajas, se saca del cardinal del set para que no pueda descuadrar con las listas de datos
param q := ceil(n / l); #cota del numero de pallets, no vale acotar por donde caben las cajas porque al optimo le puede convenir abrir mas pallets para que mas cajas queden en la fila de acceso, con ceil(n/l) se pueden poner l cajas por pallet en la fila de acceso del nivel 1 con coste de disposicion 0, asi que el optimo vale como mucho coste_palet*ceil(n/l) y ninguna solucion con mas pallets puede ser optima

set PALETS:= 1..q ;# este set son los pallets disponibles, como mucho hacen falta q

param prioridad {k in CAJAS}, integer, >= 1; # la prioridad dependiendo de cada caja
param peso {k in CAJAS}, >= 0; # el peso en gramos de cada caja
param capacidad {k in CAJAS}, >= 0; # el peso maximo en gramos que cada caja aguanta encima


/*Parámetros derivados, se calculan solos para no perder generalidad*/
param prioridad_max := max{k in CAJAS} prioridad[k]; #la peor prioridad que hay en la instancia
param prioridad_inf := prioridad_max + 1; #valor finito con el que representamos el infinito del hueco vacio
param beta {i in FILAS: i < l} := (l - i) * prioridad_max; #cota del coste que puede acumular un hueco de la fila i


/*Variables */
var abierto{s in PALETS} >= 0, <= 1; #variable que vale 1 si el pallet s se monta y 0 si no se usa

var y{i in FILAS, j in COLUMNAS, m in NIVELES, s in PALETS} >= 0, <= 1; #variable de ocupacion, 1 si el hueco (i,j,m) del pallet s tiene caja y 0 si esta vacio

var P{i in FILAS, j in COLUMNAS, m in NIVELES, s in PALETS} >= 0; #variable de prioridad a efectos de coste, 0 si el hueco esta vacio

var Q{i in FILAS, j in COLUMNAS, m in NIVELES, s in PALETS} >= 0; #variable de prioridad a efectos de orden, prioridad_inf si el hueco esta vacio

var W{i in FILAS, j in COLUMNAS, m in NIVELES, s in PALETS} >= 0; #variable de peso en el hueco

var Gam{i in FILAS, j in COLUMNAS, m in NIVELES, s in PALETS} >= 0; #variable de capacidad en el hueco

var c{i in FILAS, j in COLUMNAS, m in NIVELES, s in PALETS: i < l} >= 0; #coste imputado al hueco, no hace falta en la fila de acceso porque ahi no hay nadie delante


var x {k in CAJAS, i in FILAS, j in COLUMNAS, m in NIVELES, s in PALETS} binary; # variable que nos da 1 si la caja K esta en el hueco (i,j,m) del pallet s


/*Funcion objetivo */

minimize COSTE_TOTAL: sum {i in FILAS, j in COLUMNAS, m in NIVELES, s in PALETS: i < l} c[i,j,m,s] + coste_palet * sum{s in PALETS} abierto[s]; #ahora es un coste total y no medio, la suma del coste de todas las cajas mas el coste de montar cada pallet usado


/*Restricciones*/
s.t. ocupacion {i in FILAS, j in COLUMNAS, m in NIVELES, s in PALETS}: sum{k in CAJAS} x[k,i,j,m,s] = y[i,j,m,s] ;#restriccion igual que en la parte 3 pero por pallet, un hueco puede tener una caja o ninguna
s.t. huecoporcaja {k in CAJAS}: sum{i in FILAS, j in COLUMNAS, m in NIVELES, s in PALETS} x[k,i,j,m,s] = 1 ;#restriccion que hace que cada caja este en un hueco solo de un pallet solo, las cajas hay que colocarlas todas
s.t. Orden {i in FILAS, j in COLUMNAS, m in NIVELES, s in PALETS: i < l}: Q[i,j,m,s] >= Q[i+1,j,m,s];# restriccion de orden igual que en la parte 3, dentro de cada columna, nivel y pallet
s.t. defprioridad {i in FILAS, j in COLUMNAS, m in NIVELES, s in PALETS}: P[i,j,m,s] = sum {k in CAJAS} prioridad[k]*x[k,i,j,m,s]; # restriccion para la variable P, da 0 si el hueco esta vacio
s.t. defpeso {i in FILAS, j in COLUMNAS, m in NIVELES, s in PALETS}: W[i,j,m,s] = sum {k in CAJAS} peso[k]*x[k,i,j,m,s]; # restriccion para la variable W, da 0 si el hueco esta vacio
s.t. defcapacidad {i in FILAS, j in COLUMNAS, m in NIVELES, s in PALETS}: Gam[i,j,m,s] = sum {k in CAJAS} capacidad[k]*x[k,i,j,m,s]; # restriccion para la variable Gam, da 0 si el hueco esta vacio
s.t. resistencia {i in FILAS, j in COLUMNAS, m in NIVELES, s in PALETS: m < h}: sum{mm in NIVELES: mm > m} W[i,j,mm,s] <= Gam[i,j,m,s];# restriccion que obliga a que el peso de todas las cajas que hay encima en la misma fila y columna del mismo pallet no pase de la capacidad de la caja de abajo
s.t. defQ {i in FILAS, j in COLUMNAS, m in NIVELES, s in PALETS}: Q[i,j,m,s] = P[i,j,m,s] + prioridad_inf * (1 - y[i,j,m,s]); # restriccion que traduce que la prioridad de un hueco vacio es infinita
s.t. apoyo {i in FILAS, j in COLUMNAS, m in NIVELES, s in PALETS: m < h}: y[i,j,m+1,s] <= y[i,j,m,s];# restriccion que impide poner una caja encima de un hueco vacio, pero deja que encima de un hueco vacio haya otro hueco vacio
s.t. defcoste {i in FILAS, j in COLUMNAS, m in NIVELES, s in PALETS: i < l}: c[i,j,m,s] >= sum{t in i+1..l} P[t,j,m,s] - beta[i] * (1 - y[i,j,m,s]);# restriccion que da el coste del hueco, si hay caja es la suma de las prioridades de delante y si esta vacio el termino de correccion lo deja en 0
s.t. apertura {i in FILAS, j in COLUMNAS, m in NIVELES, s in PALETS}: y[i,j,m,s] <= abierto[s];# restriccion que enlaza ocupacion y apertura, si algun hueco del pallet s tiene caja entonces el pallet hay que montarlo y se paga su coste


/*Resolver*/
solve;

/*Salida de la solucion: lineas con prefijo fijo para que sol-4.py las lea facilmente*/
printf "OBJ %.6f\n", COSTE_TOTAL; # valor de la funcion objetivo
printf {k in CAJAS, i in FILAS, j in COLUMNAS, m in NIVELES, s in PALETS: x[k,i,j,m,s] > 0.5} "SOL %d %d %d %d %d\n", k, i, j, m, s; # caja k colocada en la fila i, columna j, nivel m del pallet s
end;
