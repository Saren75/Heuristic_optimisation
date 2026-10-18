############################
# SETS
############################
set JUICES;

############################
# PARAMETERS
############################
param CONCENTRADO{i in JUICES};
param PRICES{i in JUICES};
param MAX_JUICE;
param MAX_CONCETRADO;

############################
# Variables
############################
var production{i in JUICES}, >= 0;

############################
# F.O
############################
maximize PROFIT:
    sum{i in JUICES} PRICES[i] * production[i];

############################
# CONSTRAINTS
############################
s.t. max_liters:
    sum{i in JUICES} production[i] <= MAX_JUICE;

s.t. max_concentrado:
    sum{i in JUICES} production[i] * CONCENTRADO[i] <= MAX_CONCETRADO;

############################
# SOLVE
############################
solve;
printf {i in JUICES: production[i]} "%s millones de %s \n", production[i], i;
display PROFIT;
end;