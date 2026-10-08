##
# Diseño para conseguir la solucion optima al problema de organizar una serie de cajas con una prioridad especifica en un pallet, siguiendo una serie de normas, cada caja debe estar ordenadas por prioridad en la misma columna, la caja con menor numero de prioridad estaran mas cerca de el hueco de entrada que las de numero de prioridad mayor
##


/*Parámetros*/
param l;   #lado del pallet, parametro que viene dado en los datos
param n := l^2;   #numero de cajas, se calcula con l al cuadrado



/*SETS*/
set CAJAS:=  1..n; #enumeracion de las cajas que sale de el numero de cajas que hay
set FILAS:= 1..l ;  # este set son las filas que van de 1 a l
set COLUMNAS:= 1..l ;# este set son las columnas que van de 1 a l

param prioridad {k in CAJAS}; # la prioridad dependiendo de cada caja


/*Variables */
var P{i in FILAS, j in COLUMNAS} >= 0; #variable de prioridad en la posicion (i,j) 


var x {k in CAJAS, i in FILAS, j in COLUMNAS} binary; # variable que nos da 1 si la caja K esta en (i,j)


/*Funcion objetivo */

minimize COSTE_TOTAL_MEDIO: 1/n * sum {i in FILAS, j in COLUMNAS, t in i+1..l} P[t,j]; #suma del coste de todas las cajas entre el numero de estas


/*Restricciones*/
s.t. cajaporhueco {i in FILAS, j in COLUMNAS}: sum{k in CAJAS} x[k,i,j] = 1 ;
s.t. huecoporcaja {k in CAJAS}: sum{i in FILAS, j in COLUMNAS} x[k,i,j] = 1 ;
s.t. defprioridad {i in FILAS, j in COLUMNAS}: P[i,j] = sum {k in CAJAS} prioridad[k]*x[k,i,j];
s.t. Orden { i in 1.. l-1, j in 1..l }: P[i,j] >= P[i+1,j];

/*Resolver*/
solve;
display COSTE_TOTAL_MEDIO;
end;
