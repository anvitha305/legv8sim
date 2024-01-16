// Fahrenheit to Celsius converter, Patterson and Hennessy ARM edition ch 3
f2c:
STUR X16, [X27,#5] // S16 = 5.0 (5.0 in memory)
LDUR X16, [X27, #5] // S18 = 9.0 (9.0 in memory)
FSUBD X18, X12, X18 // S18 = fahr – 32.0
FMULD X0, X16, X18 // S0 = (5/9)*(fahr – 32.0)
BR LR // return