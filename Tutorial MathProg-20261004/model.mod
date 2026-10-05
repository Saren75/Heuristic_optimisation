#
# Giapetto's problem
#
# This finds the optimal solution for maximizing Giapetto's profit
#

/* set of toys */
set TOY;

/* parameters */
param Finishing_hours {i in TOY};
param Carpentry_hours {i in TOY};
param Demand_toys     {i in TOY};
param Profit_toys     {i in TOY};

/* decision variables */
var units {i in TOY} >=0; 

/* objective function */
maximize Profit: sum{i in TOY} Profit_toys[i]*units[i];

/* Constraints */
s.t. Fin_hours : sum{i in TOY} Finishing_hours[i]*units[i] <= 100;
s.t. Carp_hours : sum{i in TOY} Carpentry_hours[i]*units[i] <= 80;
s.t. Dem {i in TOY} : units[i] <= Demand_toys[i];

end;
