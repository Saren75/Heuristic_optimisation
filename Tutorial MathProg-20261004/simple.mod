#
# Giapetto's problem
#
# This finds the optimal solution for maximizing Giapetto's profit
#

/* decision variables */
var x1 >=0;  /* soldiers */
var x2 >=0;  /* trains */

/* objective function */
maximize Profit: 3*x1 + 2*x2;

/* Constraints */
s.t. Finishing : 2*x1 + x2 <= 100;
s.t. Carpentry : x1 + x2 <= 80;
s.t. Demand    : x1 <= 40;

end;
