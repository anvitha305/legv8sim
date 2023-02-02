// representation of one register in legv8 - val is the value stored in them and name is x0-x31 
// [will add support for aliasing later ? x31 = xzr]
#[derive(Clone)]
pub struct Reg{
    pub val: f32,
    pub name: String,
}

// module that renders the registers 
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
    pub fn registers<'a>(regs: Vec<Reg>) -> Element<'a, Message> {
        const BOLD_FONT: Font = Font::External { 
            name: "bold font",
            bytes: include_bytes!("resources/Lato-Black.ttf")};
        let mut r1 = Vec::<Element<Message>>::new();
        let mut r2 = Vec::<Element<Message>>::new();
        let mut r3 = Vec::<Element<Message>>::new();
        let mut r4 = Vec::<Element<Message>>::new();
        let mut rnum = 8;

        // i'm SORRY THIS IS UGGY </3 IT'S JUST . 2D PUSHING TO A COLUMN IS NOT FUN.
        for reg in &regs[0..(regs.len()/4)] {
            let mut s = reg.name.clone();
            s.insert(1,'0');
            r1.push(column![container(row![text(s+ " ").font(BOLD_FONT), text(reg.val)]).style(iced::theme::Container::Box).width(Length::Units(110)).max_width(110)].spacing(30).padding(10).into());
            
        }
        for reg in &regs[(regs.len()/4)..(regs.len()/2)] {
            if rnum<10{
                let mut s = reg.name.clone();
                s.insert(1,'0');
                r2.push(column![container(row![text(s+ " ").font(BOLD_FONT), text(reg.val)]).style(iced::theme::Container::Box).width(Length::Units(110)).max_width(110)].spacing(30).padding(10).into());
            }
            else {
                r2.push(column![container(row![text(reg.name.clone()+ " ").font(BOLD_FONT), text(reg.val)]).style(iced::theme::Container::Box).width(Length::Units(110)).max_width(110)].spacing(30).padding(10).into());
            }
            rnum+=1;
        }
        for reg in &regs[(regs.len()/2)..(3*regs.len()/4)] {
            r3.push(column![container(row![text(reg.name.clone()+ " ").font(BOLD_FONT), text(reg.val)]).style(iced::theme::Container::Box).width(Length::Units(110)).max_width(110)].spacing(30).padding(10).into());
        }
        for reg in &regs[(3*regs.len()/4)..(regs.len())] {
            r4.push(column![container(row![text(reg.name.clone()+ " ").font(BOLD_FONT), text(reg.val)]).style(iced::theme::Container::Box).width(Length::Units(110)).max_width(110)].spacing(30).padding(10).into());
        }
        column![Row::with_children(r1), Row::with_children(r2), 
        Row::with_children(r3), Row::with_children(r4)].spacing(20).padding(30).into()
        
    }
}