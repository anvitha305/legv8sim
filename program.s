.globl isPrimeAssembly
isPrimeAssembly:
//your code for iterating through arrays here
//base addresses of arrays in X0 - X2, length in X3
// increments stack pointer so we can save the parameters
// to be reused after function calls to iX28rime()
add X4, XZR, XZR // initialize i
add X5, XZR, XZR // initialize j
add X6, XZR, XZR // initialize k
add X7, XZR, XZR // initialize d
add X8, XZR, XZR // initialize temp
bl L1
L1:
subs X11, X4, X3 // checking if i < len
b.GT End // if not, leave program
lsl X12, X3, #3 // getting offset for geting the i-th integer
add X12, X12, X0 // getting the address for a[i]
ldur X0, [X12, #0] // putting in correct parameters for iX28rime()
bl isPrime
add X7, X1, XZR // set d to result of iX28rime()
ldur X0, [X28, #16]
ldur X1, [X28, #32] // restoring old values of parameters overwritten in
iX28rime()
ldur X2, [X28, #48]
ldur X3, [X28, #64]
add X12, X12, X1 // address of prime[j] calculated with base address
lsl X13, X4, #3 // byte offset to index into a[i]
add X13, X13, X0 // address of a[i] calculated with base address
ldur X19, [X13, #0] // getting value at a[i]
cbz X7, Else
lsl X12, X5, #3 // byte offset to index into prime[j]
add X12, X12, X1 // address of prime[j] calculated with base address
stur X19, [X12, #0] // storing value from a[i] in prime[j]
add X5, X5, #1 // j++
bl Increment // reiterate
Increment:
add X4, X4, #1 // i++, begin loop again
bl L1
Else:
lsl X12, X6, #3 // byte offset to index into prime[j]
add X12, X12, X2 // address calculated with base address
stur X19, [X12, #0] // storing value of a[i] in composite[k]
add X6, X6, #1 // k++
bl Increment // reiterate
End:
ldur X30, [X28, #0]
sub X28, X28, #80
br X30
isPrime:
//Your code for detecting a prime number here
// base address of n is in X0
sub sp, sp, #16
stur X30, [sp, #0]
stur X0, [sp, #8]
mov X1, #2
sdiv X2, X0, X1
bl L2
L2:
subs X3, X1, X2
b.GT Prime
sdiv X14, X0, X1
mul X15, X1, X14
sub X15, X0, X15
cbz X15, notPrime
add X1, X1, #1
bl L2
Prime:
mov X9, #1
ldur X0, [sp, #8]
ldur X30, [sp, #0]
add sp, sp, #16
br X30
notPrime:
add X9, XZR, XZR
ldur X0, [sp, #8]
ldur X30, [sp, #0]
add sp, sp, #16
br X30