// representation of one address in main memory in legv8 - val is the value stored in them and
// address is their address when referenced in the program. 
// the main memory will be 4 bytes per address and size is configured by a dropdown.
#[derive(Clone)]
pub struct Addr{
    pub address: u16,
    pub val: f32,
}
pub struct Stack {
    pub stack: Vec<Addr>;
    pub topaddr: u16;
}

pub trait Stackable{
    pub fn push(&self, obj);
    pub fn pop(&self)->Addr;
    pub fn peek(&self)->Addr;
}

// module that renders the memory
pub mod registers {
    use super::*;
    use crate::registers::Reg;
    use crate::Message;
    use iced::Background;
    use iced::widget::{Row, container, column, row, text};
    use iced::{Element, Length, color, Color, Font};
    use iced_native::widget::{Container};

    // generates the register representation text from the vector containing all the registers
    // regs : the registers in legv8
    // returns : the rendering of the register representation.
    pub fn memory<'a>(regs: Vec<Addr>) -> Element<'a, Message> {
        const BOLD_FONT: Font = Font::External { 
            name: "bold font",
            bytes: include_bytes!("resources/Lato-Black.ttf")};
        let mut address_view = Vec::<Element<Message>>::new();
    }
}