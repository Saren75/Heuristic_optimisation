set MONEDAS;

param COBRE {i in MONEDAS};
param LATON {i in MONEDAS};
param VALOR {i in MONEDAS};
param MIN_MONEDAS;
param MAX_COBRE;
param MAX_LATON;

var fabricadas {i in MONEDAS}, integer, >= 0;

maximize valor_total: sum {i in MONEDAS} VALOR[i] * fabricadas[i]; 

s.t. MIN_FABRICADAS: sum {i in MONEDAS} fabricadas[i] >= MIN_MONEDAS;
s.t. COBRE_USADO: sum {i in MONEDAS} COBRE[i] * fabricadas[i] <= MAX_COBRE;
s.t. LATON_USADO: sum {i in MONEDAS} LATON[i] * fabricadas[i] <= MAX_LATON;
