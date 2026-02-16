from display import Display, display
from stats import CorpStats, RunnerStats


class MenuItem:
    def __init__(self, name, value) -> None:
        self.name: str = name
        self.value: int = value


class Menu:
    def __init__(self, display: Display, menu_items: list[MenuItem], menu_colour, align_centre=False) -> None:
        self.display: Display = display
        self.index: int = 0
        self.menu_items: list[MenuItem] = menu_items
        self.menu_colour = menu_colour
        self.active = False
        self.align_centre = align_centre
        self._set_menu_spacing()

    def _set_menu_spacing(self):
        max_value = 0
        for menu_item in self.menu_items:
            px_width = self.display.measure_text(menu_item.name, 2)
            if px_width > max_value:
                max_value = px_width

        self.menu_width = max_value

    def _get_next_index(self):
        return self.index + 1 if self.index != len(self.menu_items) - 1 else 0

    def _get_prev_index(self):
        return self.index - 1 if self.index != 0 else len(self.menu_items) - 1

    def _get_x_coord(self, option_name: str):
        px_width = self.display.measure_text(option_name, 2, fixed_width=True)
        align_px = int(self.display.WIDTH /
                       2) if self.align_centre else int(self.display.WIDTH/3)

        x_coord = align_px - int(px_width/2)
        return x_coord

    def draw_options(self):
        current_option = self.menu_items[self.index]
        prev_option = self.menu_items[self._get_prev_index()]
        next_option = self.menu_items[self._get_next_index()]

        current_x = self._get_x_coord(current_option.name)
        prev_x = self._get_x_coord(prev_option.name)
        next_x = self._get_x_coord(next_option.name)
        value_x = int(3*(self.display.WIDTH/4))

        current_y = int(self.display.HEIGHT/2)
        prev_y = int(self.display.HEIGHT/4)
        next_y = int(3*(self.display.HEIGHT/4))

        self.display.clear_screen()
        self.display.set_pen(self.display.white)

        self.display.text(prev_option.name, prev_x,
                          prev_y, scale=2, fixed_width=True)
        if prev_option.value != None:
            self.display.text(str(prev_option.value), value_x,
                              prev_y, scale=2, fixed_width=True)

        self.display.set_pen(self.menu_colour)

        self.display.text(current_option.name, current_x,
                          current_y, scale=2, fixed_width=True)
        if current_option.value != None:
            self.display.text(str(current_option.value), value_x,
                              current_y, scale=2, fixed_width=True)

        self.display.set_pen(self.display.white)

        self.display.text(next_option.name, next_x,
                          next_y, scale=2, fixed_width=True)
        if next_option.value != None:
            self.display.text(str(next_option.value), value_x,
                              next_y, scale=2, fixed_width=True)

        self.display.update()


class SetItem(Menu):
    def __init__(self, display: Display, menu_items: list[MenuItem], display_colour) -> None:
        super().__init__(
            display, menu_items, display_colour, True)

    def run_menu(self):
        if self.display.button_a.read():
            self.index = self._get_prev_index()
        if self.display.button_b.read():
            self.index = self._get_next_index()
        if self.display.button_y.read():
            self.active = False
            return self.menu_items[self.index].name
        if self.display.button_x.read():
            self.active = False
            return 'Main'
        self.draw_options()
        return None


class StatMenu(Menu):
    def __init__(self, display: Display, menu_colour, corp: bool) -> None:
        self.is_corp = corp
        self.stats = CorpStats() if corp else RunnerStats()
        if corp:
            menu_items = [MenuItem('Click', self.stats.current_click), MenuItem(
                'Credits', self.stats.current_credits), MenuItem('Bad Pub', self.stats.bad_publicity)]
        else:
            menu_items = [MenuItem('Click', self.stats.current_click), MenuItem(
                'Credits', self.stats.current_credits), MenuItem('Tags', self.stats.tags), MenuItem('Brain Dmg', self.stats.brain_damage)]
        super().__init__(display, menu_items, menu_colour)

    def run_menu(self):
        if self.display.button_a.read():
            self.index = self._get_prev_index()
        if self.display.button_b.read():
            self.index = self._get_next_index()
        if self.display.button_x.read():
            if self.menu_items[self.index].name == 'Click':
                self.stats.increment_click()
                self.menu_items[self.index].value = self.stats.current_click
            else:
                self.menu_items[self.index].value += 1
        if self.display.button_y.read():
            if self.menu_items[self.index].name == 'Click':
                self.stats.decrement_click()
                self.menu_items[self.index].value = self.stats.current_click
            else:
                self.menu_items[self.index].value -= 1

        if self.display.button_y.raw() and self.display.button_x.raw():
            self.active = False
            return 'Corp' if self.is_corp else 'Runner'
        self.draw_options()
        return None


ident_menu = SetItem(
    display, [MenuItem('Corp', None), MenuItem('Runner', None)], display.green)

corp_menu = SetItem(display, [MenuItem('Jinteki', None), MenuItem(
    'NBN', None), MenuItem('Haas Bioroid', None), MenuItem('Weyland', None)], display.blue)

runner_menu = SetItem(display, [MenuItem('Anarch', None), MenuItem(
    'Criminal', None), MenuItem('Shaper', None)], display.red)

jinteki_menu = StatMenu(display, display.jinteki, True)
nbn_menu = StatMenu(display, display.nbn, True)
hb_menu = StatMenu(display, display.hb, True)
weyland_menu = StatMenu(display, display.weyland, True)

anarch_menu = StatMenu(display, display.anarch, False)
criminal_menu = StatMenu(display, display.criminal, False)
shaper_menu = StatMenu(display, display.shaper, False)
