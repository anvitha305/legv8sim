use bitfield::bitfield;
use bitvec::prelude::*;

// Type of instruction being used.
// R: R-type, register based operations
// I: I-type, immediate instructions working with an immediate memory address.
// D: D-type, load/store operations
// B: B-type, unconditional branching
// C: CB-type, conditional branching
// M: IM-type, moving shifted immediate to register

enum Typ {R, I, D, B, C, M}


struct Instruction{
	typ: Typ,
	op: char,
    regs: Vec<String>,
    addr: BitVec

    
}