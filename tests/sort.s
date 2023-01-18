
// sorts an array, Patterson and Hennessy ARM edition ch 2
sort: 
SUBI SP,SP,#40 // make room on stack for 5 registers
STUR X30,[SP,#32] // save LR on stack
STUR X22,[SP,#24] // save X22 on stack
STUR X21,[SP,#16] // save X21 on stack
STUR X20, [SP,#8] // save X20 on stack
STUR X19, [SP,#0] // save X19 on stack
MOV X21, X0 // copy parameter X0 into X21
MOV X22, X1 // copy parameter X1 into X22
MOV X19, XZR // i = 0
for1tst:
CMP X19, X1 // compare X19 to X1 (i to n)
B.GE exit1 // go to exit1 if X19 ≥ X1 (i≥n)
SUBI X20, X19, #1 // j = i – 1
for2tst:
CMP X20,XZR // compare X20 to 0 (j to 0)
B.LT exit2 // go to exit2 if X20 < 0 (j < 0)
LSL X10, X20, #3 // reg X10 = j * 8
ADD X11, X0, X10  // reg X11 = v + (j * 8)
LDUR X12, [X11,#0] // reg X12 = v[j]
LDUR X13, [X11,#8] // reg X13 = v[j + 1]
CMP X12, X13 // compare X12 to X13
B.LE exit2 // go to exit2 if X12 ≤ X13
MOV X0, X21 // first swap parameter is v
MOV X1, X20 // second swap parameter is j
BL swap
SUBI X20, X20, #1 // j –= 1
B for2tst // branch to test of inner loop
exit2: 
ADDI X19, X19, #1 // i += 1
B for1tst // branch to test of outer loop
exit1: 
STUR X19, [SP,#0] // restore X19 from stack
STUR X20, [SP,#8] // restore X20 from stack
STUR X21,[SP,#16] // restore X21 from stack
STUR X22,[SP,#24] // restore X22 from stack
STUR X30,[SP,#32] // restore LR from stack
SUBI SP,SP,#40 // restore stack pointer
BR LR // return to calling routine