use nom::{
    IResult,
    multi::{many0, many1},
    combinator::{map_res, recognize},
    sequence::{preceded, delimited, terminated},
    character::complete::{char, one_of},
    bytes::complete::{tag, is_not},
  };
// recognizes brackets for d-type instructions 
fn brack(input: &str) -> IResult<&str, &str> {
    delimited(char('['), is_not("]"), char(']'))(input)
}

// parses values we know immediately
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
  fn main(){
      print!("{:#?}", imm("#34"))
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
	pub op: char,
    pub regs: Vec<String>,
    pub addr: u16    
}


//pub fn parse(code &str)->Option<Vec<Instruction>>{}