// Fahrenheit to Celsius converter, Patterson and Hennessy ARM edition ch 3
f2c:
LDURS X16, [X27,#5] // S16 = 5.0 (5.0 in memory)
LDURS X18, [X27, #9] // S18 = 9.0 (9.0 in memory)
FDIVS X18, [X27, #32] // S18 = 32.0
FSUBS X18, X12, X18 // S18 = fahr – 32.0
FMULS X0, X16, X18 // S0 = (5/9)*(fahr – 32.0)
BR LR // return
