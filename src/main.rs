use iced::widget::{button, column, text};
use iced::{Alignment, Element, Sandbox, Settings};
use bitvec::prelude::*;
mod legv8;

pub fn main() -> iced::Result {
    Registers::run(Settings::default())
}
struct Reg{
    val: i32,
    name: String

}
struct Simulator {
   registers: Registers,
   mainMem: Memory
}

struct Memory {
   mem: Vec<BitArr>
}
struct Registers {
    regs: Vec<Reg>,
    value: u32
}

#[derive(Debug, Clone, Copy)]
enum Message {
    IncrementPressed,
    DecrementPressed,
}

impl Sandbox for Registers{
    type Message = Message;

    fn new() -> Self {
        let mut a = Vec::new();
        for i in 0..32 {
            a.push(Reg{val: 0, name: format!("x{}", i)})
        }
        Self { value: 0, regs: a}
        
    }

    fn title(&self) -> String {
        String::from("LEGV8 Simulator ")
    }

    fn update(&mut self, message: Message) {
        match message {
            Message::IncrementPressed => {
                self.value += 1;
            }
            Message::DecrementPressed => {
                self.value -= 1;
            }
        }
    }

    fn view(&self) -> Element<Message> {
        column![
            text(self.value).size(500),
            
        ]
        .padding(20)
        .align_items(Alignment::Center)
        .into()
    }
}