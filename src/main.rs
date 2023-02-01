#![windows_subsystem = "windows"] 

// iced for GUI-related things
use iced::widget::{Row, Column, button, container, column, row, text, text_input, scrollable};
use iced::{Alignment, Color, Element, Font, Length, Sandbox, Settings};
use iced::theme::{Theme};

// file i/o stuff lol
use std::fs::File;
use std::io::prelude::*;

// syntect for parsing and highlighting with the .sublime-syntax file.
use syntect::easy::HighlightLines;
use syntect::parsing::SyntaxSet;
use syntect::highlighting::{ThemeSet, Style};
use syntect::highlighting::Color as OtherColor;
use syntect::util::{LinesWithEndings};
use iced::widget::text::Text;
// external modules used in creating structures for the simulator
mod legv8;
mod registers;
use registers::registers as regs;
use crate::regs::registers;
use crate::legv8::Instruction;

pub fn main() -> iced::Result {
    Simulator::run(Settings::default())
}

// reads the contents of the file to be opened in the "editor view"
// fname : name of file
// returns : status of the opening 

fn readfile(fname: &str) -> std::io::Result<String>{
    let mut file = File::open(fname.to_string().trim())?;
    let mut code = String::new();
    file.read_to_string(&mut code)?;
    Ok(code)
}

// parses the code into legv8 code highlighting
// code: the code to be highlighted, theme : theme name for the syntax highlighting
// returns: tuple of parallel vectors of highlighting and particular strings

fn parse(code: &str, theme: String)-> (Vec<Style>, Vec<String>){
    let ss = SyntaxSet::load_from_folder("src/syntax/legv8.sublime-syntax").unwrap();
    let ts = ThemeSet::load_defaults();
    let syntax = ss.find_syntax_by_extension("s").unwrap_or_else(||ss.find_syntax_plain_text());
    let mut h = HighlightLines::new(syntax, &ts.themes[&theme]);
    let mut sty: Vec<Style> = Vec::new();
    let mut stat: Vec<&str> = Vec::new();
    for line in LinesWithEndings::from(code) {
        let ranges: Vec<(Style, &str)> = h.highlight_line(line, &ss).unwrap();
        let (mut sty1, mut stat1): (Vec<Style>, Vec<&str>) = ranges.into_iter().unzip();
        sty1.push(sty1.last().cloned().unwrap());
        stat1.push("\n");
        sty.append(&mut sty1);
        stat.append(&mut stat1);
    }
    let statstr: Vec<String> = stat.iter().map(|s| s.to_string()).collect();
    return (sty, statstr);
}


// represents the simulator structures for the application
// regs : representation of the 32 registers in legv8
// instructions : collection of instructions for the simulator
// main_mem: address and value pairings
// fname: file name for the legv8 assembly file
// darkmode: whether the application is in dark mode
// code: the code from file fname
// styles: collection of corresponding highlighting and text
// highlights: the actual styling of the text itself

struct Simulator<'a>{
   regs: Vec<registers::Reg>,
   instructions: Vec<Instruction>,
   main_mem: Vec<(u16, f32)>,
   fname: String,
   darkmode: bool,
   code: String,
   styles: (Vec<Style>, Vec<String>),
   highlights: Vec<Text<'a>>,
}

// Enumerating the statuses of the application to update the app accordingly.
// Input: When a file name is being typed in the input widget.
// FileOpen: When the button to open the file is clicked.
// Themechange: When the 'Toggle Theme' button is clicked.

#[derive(Debug, Clone)]
pub enum Message {
    Input(String),
    FileOpen,
    ThemeChange
}

// creating the application based on the simulator representation.
impl Sandbox for Simulator<'_>{
    type Message = Message;

    // initializes the simulator, starts out in darkmode and all registers are value 0.
    fn new() -> Self {
        let mut a = Vec::new();
        for i in 0..32 {
            a.push(registers::Reg{val: 0.0, name: format!("X{}", i)})
        }
        Self { regs: a, main_mem:Vec::new(), instructions:Vec::new(), darkmode:true,
        fname:"".to_string(), code:"".to_string(), styles:(Vec::new(), Vec::new()), highlights: Vec::new()}
        
    }
    // title of the app 
    fn title(&self) -> String {
        String::from("LEGV8 Simulator")
    }
    // updates the application based on an event from the message
    // message: the event that occured to cause the update to occur.

    fn update(&mut self, message: Message) {
        match message {
            Message::Input(s) => {
                self.fname = s;
            }
            Message::FileOpen => {
                let result = readfile(&self.fname);
                self.code = match result {
                    Ok(ref val) => val.to_string(),
                    Err(ref _err) => "Error reading your file.".to_string()
                };
                let v: Vec<&str> = self.fname.split('.').collect();
                if v.len() != 2 || v[1].ne("s"){
                    self.code = "Please use a .s assembly file to simulate.".to_string();
                }
                self.highlights.clear();
                if result.is_ok(){
                    let mut theme:String = "".to_string();
                    if self.darkmode {
                        theme = "base16-ocean.dark".to_string();
                    }
                    else {
                        theme = "Solarized (dark)".to_string();
                    }
                    self.styles = parse(&self.code, theme);
                    for x in 0..(self.styles.0).len()  {
                        let a: OtherColor = self.styles.0[x].foreground;
                        self.highlights.push(Text::new(self.styles.1[x].clone()).style(Color::from_rgb((a.r as f32)/255.0, (a.g as f32)/255.0, (a.b as f32)/255.0)).into());
                    }

                }
                else {
                    self.highlights.push(Text::new(self.code.clone()).into());
                }
            }
            Message::ThemeChange => {
                self.darkmode = !self.darkmode;
                self.update(Message::FileOpen);
            }

        }
    }
    // view the current state of the simulator
    // returns: the rendering for the application.

    fn view(&self) -> Element<Message> {
        const BOLD_FONT: Font = Font::External { 
            name: "bold font",
            bytes: include_bytes!("resources/Lato-Black.ttf")};
        // sets up the text highlighting from the content
        let mut a: Column<Message> = Column::new();
        let mut b: Row<Message> = Row::new();
        if self.styles.1.len() > 0 {
        for i in 0..self.highlights.len() {
            
            if self.styles.1[i].contains("\n") {
                a = a.push(b);
                b = Row::new();
            }
            else {
                b = b.push(self.highlights[i].to_owned());
            }
            
        }}
        let content: Element<_> = container(a.align_items(Alignment::Start).padding(30)).width(Length::Fill).into();
        // set up the whole appplication
        Element::from(column![column![
            row![text("File viewer").font(BOLD_FONT).size(30),button("Toggle Theme").on_press(Message::ThemeChange)].spacing(10).align_items(Alignment::Center), 
            row![text("Name of file to be simulated").size(20)].align_items(Alignment::Start),
            row![text_input(&String::new(), &self.fname, Message::Input), 
            button("Ok").on_press(Message::FileOpen)].align_items(Alignment::Center)].padding(30),container(scrollable(content)).height(Length::FillPortion(4)), 
            row![registers(self.regs.clone()), text("memory placeholder lol")]].height(Length::FillPortion(4)).width(Length::Fill).padding(20))
    }

    // Updates the theme based on if the darkmode indicator is selected or not from the input button.
    // returns: Theme [variable configuring the application colors]

    fn theme(&self) -> Theme {
        if self.darkmode {
            Theme::Dark 
        }
        else {
            Theme::Light
        }
    }
}