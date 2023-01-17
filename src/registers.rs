// representation of one register in legv8 - val is the value stored in them and name is x0-x31 
// [will add support for aliasing later ? x31 = xzr]
#[derive(Clone)]
pub struct Reg{
    pub val: f32,
    pub name: String,
}

pub mod registers {
    use crate::registers::Reg;
    use iced_native::layout::{self, Layout};
    use iced_native::renderer;
    use iced_native::widget::{self, Widget};
    use iced_native::{Color, Element, Length, Point, Rectangle, Size};

    pub struct Registers {
        regs: Vec<Reg>,
        width: f32,
        height: f32,
    }
    impl Registers {
        pub fn new(reg: Vec<Reg>, w:f32, h:f32) -> Self {
            Self { regs:reg, width:w, height:h}
        }
    }

    pub fn registers(reg: Vec<Reg>, w:f32, h:f32) -> Registers {
        Registers::new(reg, w, h)
    }

    impl<Message, Renderer> Widget<Message, Renderer> for Registers
    where
        Renderer: renderer::Renderer,
    {
        fn width(&self) -> Length {
            Length::Shrink
        }

        fn height(&self) -> Length {
            Length::Shrink
        }

        fn layout(
            &self,
            _renderer: &Renderer,
            _limits: &layout::Limits,
        ) -> layout::Node {
            layout::Node::new(Size::new(self.width, self.height))
        }

        fn draw(
            &self,
            _state: &widget::Tree,
            renderer: &mut Renderer,
            _theme: &Renderer::Theme,
            _style: &renderer::Style,
            layout: Layout<'_>,
            _cursor_position: Point,
            _viewport: &Rectangle,
        ) {
            renderer.fill_quad(
                renderer::Quad {
                    bounds: layout.bounds(),
                    border_width: 0.0,
                    border_radius: 0.0.into(),
                    border_color: Color::TRANSPARENT,
                },
                Color::BLACK,
            );
        }
    }

    impl<'a, Message, Renderer> From<Registers> for Element<'a, Message, Renderer>
    where
        Renderer: renderer::Renderer,
    {
        fn from(registers: Registers) -> Self {
            Self::new(registers)
        }
    }
}