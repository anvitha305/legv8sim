use iced::widget::{button, column, row, text, text_input,};
use iced::{Alignment, Element, Sandbox, Settings};
use bitvec::prelude::*;
use std::fs::File;
use std::io::prelude::*;
mod legv8;

pub fn main() -> iced::Result {
    Simulator::run(Settings::default())
}

fn readfile(fname: &str) -> std::io::Result<String>{
    let mut file = File::open(fname)?;
    let mut code = String::new();
    file.read_to_string(&mut code)?;
    Ok(code)
}

struct Reg{
    val: f32,
    name: String

}
struct Simulator{
   registers: Vec<Reg>,
   main_mem: Vec<f32>,
   value: u32,
   st: String,
   code: String
}

#[derive(Debug, Clone)]
enum Message {
    Input(String),
    FileOpen,
}

impl Sandbox for Simulator{
    type Message = Message;
    fn new() -> Self {
        let mut a = Vec::new();
        for i in 0..32 {
            a.push(Reg{val: 0.0, name: format!("x{}", i)})
        }
        Self { registers: a, main_mem:Vec::new(), value:32, 
        st:"".to_string(), code:"".to_string()}
        
    }
     
    fn title(&self) -> String {
        String::from("LEGV8 Simulator ")
    }

    fn update(&mut self, message: Message) {
        match message {
            Message::Input(s) => {
                self.value +=1;
                self.st = s;
            }
            Message::FileOpen => {
                self.value-=1;
                let result = readfile(&self.st);
                self.code = match result {
                    Ok(val) => val,
                    Err(err) => panic!("Error with reading your file.")
                }
            }

        }
    }

    fn view(&self) -> Element<Message> {
        column![
            row![text("Name of file to be simulated:").size(30)].align_items(Alignment::Center),
            row![text_input(&String::new(), &self.st, Message::Input), 
            button("Ok").on_press(Message::FileOpen),].align_items(Alignment::Center),
            row![text(&self.code)].align_items(Alignment::Start).padding(50)
        ]
        .padding(20)
        .into()
        
    }
}