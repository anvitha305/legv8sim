use iced::widget::{button, column, row, text, text_input,};
use iced::{Alignment, Element, Sandbox, Settings};

// representation of registers in legv8 - val is the value stored in them and name is x0-x31 
// [will add support for aliasing later ? x31 = xzr]

pub struct Reg{
    pub val: f32,
    pub name: String
}


