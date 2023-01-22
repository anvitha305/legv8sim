// representation of one register in legv8 - val is the value stored in them and name is x0-x31 
// [will add support for aliasing later ? x31 = xzr]
#[derive(Clone)]
pub struct Reg{
    pub val: f32,
    pub name: String,
}

pub mod registers {
    use crate::registers::Reg;
    use crate::Message;
    use iced::widget::{Row, column, row, text};
    use iced::{Element};c
    pub fn registers<'a>(regs: Vec<Reg>) -> Element<'a, Message> {
        let mut r1 = Vec::<Element<Message>>::new();
        let mut r2 = Vec::<Element<Message>>::new();
        let mut r3 = Vec::<Element<Message>>::new();
        let mut r4 = Vec::<Element<Message>>::new();
        for reg in &regs[0..(regs.len()/4)] {
            r1.push(column![row![text(reg.name.clone()+ ": "), text(reg.val)]].spacing(30).padding(10).into());
        }
        for reg in &regs[(regs.len()/4)..(regs.len()/2)] {
            r2.push(column![row![text(reg.name.clone()+ ": "), text(reg.val)]].spacing(30).padding(10).into());
        }
        for reg in &regs[(regs.len()/2)..(3*regs.len()/4)] {
            r3.push(column![row![text(reg.name.clone()+ ": "), text(reg.val)]].spacing(30).padding(10).into());
        }
        for reg in &regs[(3*regs.len()/4)..(regs.len())] {
            r4.push(column![row![text(reg.name.clone()+ ": "), text(reg.val)]].spacing(30).padding(10).into());
        }
        column![Row::with_children(r1), Row::with_children(r2), 
        Row::with_children(r3), Row::with_children(r4)].into()
        
    }
}