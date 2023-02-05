use nom::{
  IResult,
  multi::{many0, many1},
  combinator::{map_res, verify, value, opt, recognize},
  sequence::{preceded, pair, delimited, tuple, terminated},
  character::complete::{char, digit1, one_of},
  branch::{alt},
  bytes::complete::{tag, is_not},
};
// recognizes brackets for d-type instructions 
fn brack(input: &str) -> IResult<&str, &str> {
    delimited(char('['), is_not("]"), char(']'))(input)
}

// recognizes comments 
fn comment(input: &str) -> IResult<&str, &str> {
    value(
      "", // Output is thrown away.
      pair(tag("//"),
      is_not("\n\r"
      )
    )
    )(input)
}

// recognizes values we know immediately
fn imm(input: &str) -> IResult<&str, u16> {
    map_res(
      preceded(
        tag("#"),
        recognize(
          many1(
            terminated(one_of("0123456789"), many0(char('_')))
          )
        )
      ),
      |out: &str| u16::from_str_radix(&str::replace(&out, "_", ""), 10)
    )(input)
}

// recognizes one of the numbered registers
fn numreg(input: &str) -> IResult<&str, &str> {
    recognize(
      pair(
        tag("x"), 
        verify(
          digit1, 
          |s: &str| (0..31).contains(&(s.parse().unwrap())
      )
    )
  )
    )(input)
}

// recognizes one of the named registers and converts it to the numbered registers
fn altreg(input: &str) -> IResult<&str, &str> {
    alt((
      value("sp", tag("x28")), 
      value("fp", tag("x29")), 
      value("lr", tag("x30")), 
      value("xzr", tag("x31"))
    )
  )(input)
}

// combined parser for registers [both numbered and non numbered]
fn reg(input: &str) -> IResult<&str, &str> {
  alt ((
    altreg,
    numreg,
  )
  )(input)
}

// Type of instruction being used.
// R: R-type, register based operations
// I: I-type, immediate instructions working with an immediate memory address.
// D: D-type, load/store operations
// B: B-type, unconditional branching
// C: CB-type, conditional branching
// M: IM-type, moving shifted immediate to register

pub enum Typ {R, I, D, B, C, M}

pub struct Instruction{
	pub typ: Typ,
	pub instr: String,
  pub regs: Vec<String>,
  pub addr: u16    
}

pub struct Branch{
  pub name: String,
  pub inst: Vec<Instruction>
}

//pub fn parse(code &str)->Option<Vec<Instruction>>{}