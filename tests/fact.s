// computes factorial of a number stored in x0, example in DS-5 
fact:
SUBI XZR, X0, #1
B.GT else
BR X30
else:
ADD X9,X0,X3
SUBI SP, SP, #16
SUBI X0, X0, #1
BL fact
LDUR X9,[SP,#0]
LDUR X30,[SP,#8]
ADD SP, SP, #16
MUL X0, X0, X9
BR X30
