############################################################
# SETS
############################################################
set WORKERS;
set HOUSES;

############################################################
# PARAMS
############################################################
param LABOR_COST{i in WORKERS};
param MAX_WORK{i in WORKERS};
param PAINT_TIME{i in WORKERS, j in HOUSES};

param PAINTER_HOUSE_COST {i in WORKERS, j in HOUSES} := LABOR_COST[i] * PAINT_TIME[i,j];

############################################################
# VARIABLES
############################################################
var assigned {i in WORKERS, j in HOUSES} binary;

############################################################
# OBJECTIVE
############################################################
minimize Total_cost: sum{i in WORKERS, j in HOUSES} PAINTER_HOUSE_COST[i,j] * assigned[i,j];

############################################################
# CONSTRAINTS
############################################################
/* A painter’s availability cannot be exceeded */ 
s.t. Max_availability {i in WORKERS}:
	sum{j in HOUSES} PAINT_TIME[i,j] * assigned[i,j] <= MAX_WORK[i];

/* Each house must be assigned to exactly one painter */
s.t. One_painter_per_house {j in HOUSES}:
	sum{i in WORKERS} assigned[i,j] = 1;
    


############################################################
# SOLVE AND PRINT SOLUTION
############################################################
solve;
printf {i in WORKERS, j in HOUSES: assigned[i, j]} "%s pinta la casa %s \n", i, j;
display Total_cost;
end;
