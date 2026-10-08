set TOYS;

param Finishing_hours {i in TOYS};
param Carpentry_hours {i in TOYS};
param Demand_toys {i in TOYS};
param Profit_toys {i in TOYS};
param Time_limit_fin;
param Time_limit_carpentry;

var units {i in TOYS}, >= 0;

maximize Profit:
	sum{i in TOYS} Profit_toys[i] * units[i];
	
s.t. Fin_hours: sum{i in TOYS} Finishing_hours[i] * units[i] <= Time_limit_fin;

s.t. Carp_hours: sum{i in TOYS} Carpentry_hours[i] * units[i] <= Time_limit_carpentry;

s.t. Demand {i in TOYS}: units[i] <= Demand_toys[i];

solve;

printf {i in TOYS} "Unidades de %s: %d\n", i, units[i]; 
printf "Beneficio total: %d\n", Profit;

end;
