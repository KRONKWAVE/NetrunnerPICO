from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY
from pimoroni import Button
import jpegdec


class Display(PicoGraphics):
    def __init__(self) -> None:
        super().__init__(DISPLAY_PICO_DISPLAY, rotate=0)
        self.set_backlight(0.5)
        self.red = self.create_pen(255, 0, 0)
        self.green = self.create_pen(0, 255, 0)
        self.blue = self.create_pen(0, 0, 255)
        self.black = self.create_pen(0, 0, 0)
        self.white = self.create_pen(255, 255, 255)
        self.hb = self.create_pen(127, 116, 168)
        self.nbn = self.create_pen(242, 202, 80)
        self.jinteki = self.create_pen(150, 27, 36)
        self.weyland = self.create_pen(57, 115, 94)
        self.criminal = self.create_pen(96, 147, 222)
        self.anarch = self.create_pen(242, 109, 61)
        self.shaper = self.create_pen(96, 181, 78)
        self.WIDTH, self.HEIGHT = self.get_bounds()
        self.button_a = Button(12, repeat_time=500)
        self.button_b = Button(13, repeat_time=500)
        self.button_x = Button(14, repeat_time=500)
        self.button_y = Button(15, repeat_time=500)

    def clear_screen(self):
        self.set_pen(self.black)
        self.clear()

    def display_image(self, path: str):
        j = jpegdec.JPEG(PicoGraphics(display=DISPLAY_PICO_DISPLAY))
        j.open_file(path)
        j.decode(0, 0, jpegdec.JPEG_SCALE_FULL, dither=True)


display = Display()
