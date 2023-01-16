#![windows_subsystem = "windows"] 
use iced::widget::{button, container, column, row, text, text_input, scrollable};
use iced::{Alignment, Element, Length, Sandbox, Settings};
use std::fs::File;
use std::io::prelude::*;
mod legv8;
mod registers;
use registers::registers as regs;
use crate::regs::registers;
pub fn main() -> iced::Result {
    Simulator::run(Settings::default())
}

fn readfile(fname: &str) -> std::io::Result<String>{
    let mut file = File::open(fname.to_string().trim())?;
    let mut code = String::new();
    file.read_to_string(&mut code)?;
    Ok(code)
}


struct Simulator{
   regs: Vec<registers::Reg>,
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
            a.push(registers::Reg{val: 0.0, name: format!("x{}", i)})
        }
        Self { regs: a, main_mem:Vec::new(), value:32, 
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
                    Err(_err) => "Error reading your file.".to_string()
                };
                let v: Vec<&str> = self.st.split('.').collect();
                if v.len() != 2 || v[1].ne("asm"){
                    self.code = "Please use a .asm file to simulate.".to_string();
                }
            }

        }
    }

    fn view(&self) -> Element<Message> {
        let content: Element<_> = container(
            row![text(&self.code)].align_items(Alignment::Start).padding(30))
            .width(Length::Fill)
        .into();
        Element::from(column![column![
            row![text("File viewer").size(30)].align_items(Alignment::Center), 
            row![text("Name of file to be simulated:").size(20)].align_items(Alignment::Center),
            row![text_input(&String::new(), &self.st, Message::Input), 
            button("Ok").on_press(Message::FileOpen),].align_items(Alignment::Center)].padding(30),container(scrollable(content)).height(Length::FillPortion(3)), row![registers(self.regs.clone(), 500.0, 300.0), text("hiii 2").size(100)]].padding(20))
    }
}