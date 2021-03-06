# Contents:
# 1. Initialising the Pimoroni PicoDisplay
# 2. Defining variables etc
# 3. Defining functions
# 4. The main loop which executes the code

# Initialise the display

# Import the PICO Display
import picodisplay as display
import utime

# Initialise display with a bytearray display buffer, 2 bytes per pixel (RGB565)
display_buffer = bytearray(display.get_width() * display.get_height() * 2)
display.init(display_buffer)

# Set the backlight brightness
display.set_backlight(0.5)


# Define global variables


# Define the time for the renderloop
current_time = utime.ticks_ms()
frame_rate = 60

# Dictionary to store the data for the Runner
runner = {
    "Click": 0,
    "Credits": 5,
    "Tags": 0,
    "Brain Damage": 0
    }

# Dictionary to store the data for the Corp
corp = {
    "Click": 0,
    "Credits": 5,
    "Bad Publicity": 0
    }

# Selector remembers which menu item is selected (clicks/credits etc.)
# 0 is clicks, 1 is credits, 2 is tags/bad publicity, 3 is brain damage
selector = 0

# ident determines whether you're a corp or runner
# 0 means you're the runner, 1 means you're the corp, 2 means you have yet to select and are on the main menu screen
ident = 2

# submenu is used to trigger the ident select submenu (where you choose the specific identity you're playing as)
# 0 means the select ident submenu is not shown, 1 means it is
submenu = 0

# ident_pen determines the colour of your pen and the LED
# 0 is undefined, 1 is NBN, 2 is HB, 3 is jinteki, 4 is weyland, 5 is criminal, 6 is anarch, 7 is shaper
ident_pen = 0

# define pen colours including specific colours for each ident 
black = display.create_pen(0, 0, 0)
white = display.create_pen(255, 255, 255)
blue = display.create_pen(0, 0, 255)
red = display.create_pen(255, 0, 0)
HB = display.create_pen(127,116,168)
NBN = display.create_pen(242,202,80)
jinteki = display.create_pen(150,27,36)
weyland = display.create_pen(57,115,94)
criminal = display.create_pen(96,147,222)
anarch = display.create_pen(242,109,61)
shaper = display.create_pen(96,181,78)


# Define functions


# Defines the button class, checks for when the button is first pressed, just released, and continually pressed
class Button:
    
    button = display.BUTTON_X
    button_bounce_threshold = 0
    button_bounce_value = 0
    previous_button_value = False
    current_button_value = False
    
    def __init__(self, BUTTON, bounce_threshold):
        self.button = BUTTON
        self.button_bounce_threshold = bounce_threshold
    
    def button_just_pressed(self):
        return self.previous_button_value == False and self.current_button_value == True
        
    def button_pressed(self):
        return self.current_button_value == True
        
    def button_released(self):
        return self.current_button_value == False
        
    def button_just_released(self):
        return self.previous_button_value == True and self.current_button_value == False
    
    def update_button_state(self):
        if self.button_bounce_value < self.button_bounce_threshold:
            if display.is_pressed(self.button) != self.current_button_value:
                self.button_bounce_value += 1
            else:
                self.button_bounce_value = 0
        else:
            self.previous_button_value = self.current_button_value
            self.current_button_value = display.is_pressed(self.button)

# Define the buttons
# A button
button_a = Button(display.BUTTON_A, 2)

# B button
button_b = Button(display.BUTTON_B, 2)

# X button
button_x = Button(display.BUTTON_X, 2)

# Y button
button_y = Button(display.BUTTON_Y, 2)


# Clears the screen to black
def clear():
    display.set_pen(black)
    display.clear()
    display.update()

# Increases the click counter for the runner - counts up from 0 to 4 and loops from 4 to 0
def runner_increment_click():
    global runner
    if runner["Click"]<4:
        runner["Click"] += 1
    else:
        runner["Click"] = 0

# Decreases the click counter for the runner - counts down from current value to 0; does not loop from 0 to 4
def runner_decrement_click():
    global runner
    if runner["Click"] > 0:
        runner["Click"] -= 1
    else:
        runner["Click"] = 0

# Increments the credits for the runner dictionary
def runner_increment_credit():
    global runner
    runner["Credits"] += 1

# Decrements the credits for the runner dictionary - does not go below 0
def runner_decrement_credit():
    global runner
    if runner["Credits"] > 0:
        runner["Credits"] -= 1
    else:
        runner["Credits"] = 0

# Increases the click counter for the corp - counts up from 0 to 3 and loops from 3 to 0
def corp_increment_click():
    global corp
    if corp["Click"]<3:
        corp["Click"] += 1
    else:
        corp["Click"] = 0

# Decreases the click counter for the corp - counts down from current value to 0; does not loop from 0 to 3
def corp_decrement_click():
    global corp
    if corp["Click"] > 0:
        corp["Click"] -= 1
    else:
        corp["Click"] = 0

# Increases the credits for the corp dictionary
def corp_increment_credit():
    global corp
    corp["Credits"] += 1    

# Decreases the credits for the corp dictionary - does not go below 0
def corp_decrement_credit():
    global corp
    if corp["Credits"] > 0:
        corp["Credits"] -= 1
    else:
        corp["Credits"] = 0

# Increases the tags for the runner dictionary
def increment_tag():
    global runner
    runner["Tags"] += 1

# Decreases the tags for the runner dictionary - does not go below 0
def decrement_tag():
    global runner
    if runner["Tags"] > 0:
        runner["Tags"] -= 1
    else:
        runner["Tags"] = 0
        
# Increases the brain damage for the runner dictionary
def increment_brain_damage():
    global runner
    runner["Brain Damage"] += 1

# Decreases the brain damage for the runner dictionary - does not go below 0
def decrement_brain_damage():
    global runner
    if runner["Brain Damage"] > 0:
        runner["Brain Damage"] -= 1
    else:
        runner["Brain Damage"] = 0

# Increases the bad publicity for the corp dictionary
def increment_bad_publicity():
    global corp
    corp["Bad Publicity"] += 1

# Decreases the bad publicity for the corp dictionary - does not go below 0
def decrement_bad_publicity():
    global corp
    if corp["Bad Publicity"] > 0:
        corp["Bad Publicity"] -= 1
    else:
        corp["Bad Publicity"] = 0

# Increases the selector value - used to navigate the menus
# Loops at 3 for runner and at 2 for corp
def cycle_up_selector():
    global selector
    global ident
    if ident == 0:
        if selector < 3:
            selector += 1
        else:
            selector = 0
    if ident == 1:
        if selector < 2:
            selector += 1
        else:
            selector = 0

# Decreases the selector value and loops to max at 0 as defined by your ident
def cycle_down_selector():
    global selector
    if selector > 0:
        selector -= 1
    elif ident == 0 and selector == 0:
        selector = 3
    elif ident == 1 and selector == 0:
        selector = 2

# Sets your ident to runner and resets the dictionary, also sets the state of the submenu
def set_runner():
    global submenu
    submenu = 1
    global ident
    ident = 0
    global runner
    runner = {
    "Click": 0,
    "Credits": 5,
    "Tags": 0,
    "Brain Damage": 0
    }
    display.set_led(255, 0, 0)
    clear()

# Sets your ident to corp and resets the dictionary, also sets the state of the submenu
def set_corp():
    global submenu
    submenu = 1
    global ident
    ident = 1
    global corp
    corp = {
    "Click": 0,
    "Credits": 5,
    "Bad Publicity": 0
    }
    display.set_led(0, 0, 255)
    clear()


# Sets your ident to NBN and your pen colour to match
def set_NBN():
    global submenu
    submenu = 0
    global ident_pen
    ident_pen = 1
    display.set_led(242,202,80)
    clear()


# Sets your ident to HB and your pen colour to match
def set_HB():
    global submenu
    submenu = 0
    global ident_pen
    ident_pen = 2
    display.set_led(127,116,168)
    clear()

# Sets your ident to jinteki and your pen colour to match
def set_jinteki():
    global submenu
    submenu = 0
    global ident_pen
    ident_pen = 3
    display.set_led(150,27,36)
    clear()

    
# Sets your ident to weyland and your pen colour to match
def set_weyland():
    global submenu
    submenu = 0
    global ident_pen
    ident_pen = 4
    display.set_led(57,115,94)
    clear()


# Sets your ident to criminal and your pen colour to match
def set_criminal():
    global submenu
    submenu = 0
    global ident_pen
    ident_pen = 5
    display.set_led(96,147,222)
    clear()

    
# Sets your ident to anarch and your pen colour to match
def set_anarch():
    global submenu
    submenu = 0
    global ident_pen
    ident_pen = 6
    display.set_led(242,109,61)
    clear()

    
# Sets your ident to shaper and your pen colour to match
def set_shaper():
    global submenu
    submenu = 0
    global ident_pen
    ident_pen = 7
    display.set_led(96,181,78)
    clear()


# Sets the pen colour based on the identity
def set_ident_pen():
    if ident_pen == 1:
        display.set_pen(NBN)
    elif ident_pen == 2:
        display.set_pen(HB)
    elif ident_pen == 3:
        display.set_pen(jinteki)
    elif ident_pen == 4:
        display.set_pen(weyland)
    elif ident_pen == 5:
        display.set_pen(criminal)
    elif ident_pen == 6:
        display.set_pen(anarch)
    elif ident_pen == 7:
        display.set_pen(shaper)

# Draws the credit shape for the runner screen
def runner_credit():
    display.rectangle(8, 43, 2, 14)
    display.rectangle(14, 48, 7, 9)
    display.rectangle(17, 45, 4, 3)
    display.rectangle(14, 57, 4, 3)
    display.pixel_span(9, 42, 2)
    display.pixel_span(10, 41, 2)
    display.pixel_span(11, 40, 2)
    display.pixel_span(12, 39, 5)
    display.pixel_span(13, 38, 3)
    display.pixel_span(16, 40, 2)
    display.pixel_span(17, 41, 2)
    display.pixel_span(18, 42, 2)
    display.pixel_span(19, 43, 2)
    display.pixel_span(18, 44, 3)
    display.pixel_span(15, 47, 2)
    display.pixel_span(18, 57, 2)
    display.pixel_span(9, 57, 2)
    display.pixel_span(10, 58, 2)
    display.pixel_span(11, 59, 2)
    display.pixel_span(12, 60, 5)
    display.pixel_span(13, 61, 3)
    display.pixel(14, 37)
    display.pixel(16, 46)
    display.pixel(18, 58)
    display.pixel(14, 62)

# Draws the credit shape for the corp screen
def corp_credit():
    display.rectangle(8, 61, 2, 14)
    display.rectangle(14, 66, 7, 9)
    display.rectangle(17, 63, 4, 3)
    display.rectangle(14, 75, 4, 3)
    display.pixel_span(9, 60, 2)
    display.pixel_span(10, 59, 2)
    display.pixel_span(11, 58, 2)
    display.pixel_span(12, 57, 5)
    display.pixel_span(13, 56, 3)
    display.pixel_span(16, 58, 2)
    display.pixel_span(17, 59, 2)
    display.pixel_span(18, 60, 2)
    display.pixel_span(19, 61, 2)
    display.pixel_span(18, 62, 3)
    display.pixel_span(15, 65, 2)
    display.pixel_span(18, 75, 2)
    display.pixel_span(9, 75, 2)
    display.pixel_span(10, 76, 2)
    display.pixel_span(11, 77, 2)
    display.pixel_span(12, 78, 5)
    display.pixel_span(13, 79, 3)
    display.pixel(14, 55)
    display.pixel(16, 64)
    display.pixel(18, 76)
    display.pixel(14, 80)   

# Draws the tag shape for the runner screen
def tag():
    display.rectangle(10, 85, 5, 5)
    display.rectangle(21, 77, 24, 2)
    display.pixel_span(7, 81, 9)
    display.pixel_span(8, 93, 10)
    display.rectangle(5, 83, 5, 2)
    display.pixel_span(6, 82, 4)
    display.pixel_span(15, 90, 6)
    display.pixel_span(15, 91, 5)
    display.pixel_span(15, 92, 4)
    display.pixel_span(15, 94, 2)
    display.pixel_span(8, 80, 2)
    display.rectangle(18, 84, 1, 6)
    display.rectangle(18, 84, 1, 6)
    display.rectangle(6, 85, 1, 7)
    display.pixel_span(14, 84, 3)
    display.pixel_span(15, 83, 3)
    display.pixel_span(16, 82, 3)
    display.pixel_span(17, 81, 3)
    display.pixel_span(18, 80, 3)
    display.pixel_span(19, 79, 3)
    display.rectangle(23, 72, 6, 2)
    display.rectangle(25, 74, 2, 3)
    display.rectangle(30, 73, 2, 4)
    display.rectangle(34, 73, 2, 4)
    display.rectangle(37, 73, 2, 3)
    display.rectangle(41, 74, 2, 3)
    display.pixel_span(31, 72, 4)
    display.pixel_span(38, 72, 5)
    display.pixel_span(32, 75, 2)
    display.pixel_span(38, 76, 3)
    display.pixel(40, 74)
    display.pixel(20, 78)
    display.pixel(9, 79)
    display.pixel(15, 85)
    display.pixel(7, 92)
    display.pixel(15, 95)
    display.pixel(4, 84)

# Draws the bad publicity shape for the corp screen
def bad_publicity():
    display.rectangle(14, 96, 2, 11)
    display.rectangle(5, 105, 9, 2)
    display.rectangle(16, 96, 4, 2)
    display.pixel(20, 96)
    display.pixel(22, 97)
    display.rectangle(23, 96, 3, 2)
    display.rectangle(24, 98, 2, 3)
    display.pixel(24, 101)
    display.pixel(26, 102)
    display.rectangle(25, 103, 2, 11)
    display.pixel(26, 114)
    display.pixel(24, 115)
    display.rectangle(24, 116, 2, 12)
    display.pixel_span(21, 126, 3)
    display.pixel_span(22, 127, 2)
    display.pixel_span(13, 126, 6)
    display.pixel_span(12, 127, 8)
    display.pixel_span(8, 125, 3)
    display.pixel_span(8, 126, 2)
    display.rectangle(6, 120, 2, 7)
    display.pixel(7, 119)
    display.pixel(5, 117)
    display.rectangle(5, 107, 2, 10)
    display.pixel_span(5, 104, 3)
    display.pixel_span(6, 103, 3)
    display.pixel_span(7, 102, 3)
    display.pixel_span(8, 101, 3)
    display.pixel_span(9, 100, 3)
    display.pixel_span(10, 99, 3)
    display.pixel_span(11, 98, 3)
    display.pixel_span(12, 97, 2)
    display.pixel(13, 96)

# Draws the brain damage shape for the runner screen
def brain_damage():
    display.pixel(22, 103)
    display.pixel_span(21, 104, 2)
    display.pixel_span(20, 105, 2)
    display.pixel_span(19, 106, 2)
    display.pixel_span(18, 107, 6)
    display.pixel_span(21, 108, 2)
    display.pixel_span(20, 109, 2)
    display.pixel_span(20, 105, 2)
    display.pixel_span(11, 110, 2)
    display.pixel_span(14, 110, 2)
    display.pixel_span(19, 110, 2)
    display.pixel_span(10, 111, 3)
    display.pixel_span(14, 111, 3)
    display.pixel_span(18, 111, 2)
    display.pixel_span(10, 112, 3)
    display.pixel_span(14, 112, 3)
    display.pixel(18, 112)
    display.pixel_span(9, 113, 2)
    display.pixel_span(14, 113, 4)
    display.pixel_span(8, 114, 5)
    display.pixel(14, 114)
    display.pixel_span(16, 114, 3)
    display.pixel_span(7, 115, 4)
    display.pixel(12, 115)
    display.pixel_span(16, 115, 4)
    display.rectangle(7, 119, 4, 2)
    display.rectangle(7, 118, 2, 6)
    display.rectangle(11, 122, 2, 2)
    display.rectangle(18, 117, 2, 2)
    display.rectangle(17, 120, 3, 2)
    display.rectangle(18, 122, 2, 2)
    display.rectangle(15, 122, 2, 2)
    display.rectangle(14, 125, 3, 2)
    display.rectangle(11, 126, 2, 2)
    display.pixel_span(7, 116, 2)
    display.pixel_span(10, 117, 3)
    display.pixel_span(14, 117, 3)
    display.pixel_span(16, 118, 2)
    display.pixel_span(11, 120, 2)
    display.pixel_span(14, 120, 3)
    display.pixel_span(9, 123, 2)
    display.pixel_span(8, 124, 2)
    display.pixel_span(17, 124, 2)
    display.pixel_span(9, 125, 2)
    display.pixel_span(14, 127, 2)
    display.pixel(12, 116)
    display.pixel(14, 116)
    display.pixel(16, 116)
    display.pixel(19, 116)
    display.pixel(7, 117)
    display.pixel(12, 116)
    display.pixel(10, 118)
    display.pixel(12, 118)
    display.pixel(14, 118)
    display.pixel(14, 119)
    display.pixel(19, 119)
    display.pixel(9, 121)
    display.pixel(12, 121)
    display.pixel(14, 121)
    display.pixel(14, 123)
    display.pixel(14, 124)
    display.pixel(12, 125)
    display.pixel(17, 125)
    display.pixel(10, 126)

# Draws the click shape for the runner screen
def runner_click():
    display.rectangle(10, 8, 14, 2)
    display.rectangle(10, 25, 14, 2)
    display.rectangle(9, 9, 2, 2)
    display.rectangle(7, 12, 2, 2)
    display.rectangle(5, 15, 2, 2)
    display.rectangle(5, 18, 2, 2)
    display.rectangle(7, 21, 2, 2)
    display.rectangle(9, 24, 2, 2)
    display.rectangle(23, 24, 2, 2)
    display.rectangle(25, 21, 2, 2)
    display.rectangle(27, 18, 2, 2)
    display.rectangle(27, 15, 2, 2)
    display.rectangle(25, 12, 2, 2)
    display.rectangle(23, 9, 2, 2)
    display.rectangle(17, 13, 1, 5)
    display.rectangle(9, 15, 1, 5)
    display.rectangle(23, 14, 1, 2)
    display.rectangle(24, 16, 1, 4)
    display.pixel_span(8, 11, 2)
    display.pixel_span(14, 11, 6)
    display.pixel_span(24, 11, 2)
    display.pixel_span(12, 12, 2)
    display.pixel_span(20, 12, 2)
    display.pixel_span(6, 14, 2)
    display.pixel_span(26, 14, 2)
    display.pixel_span(4, 17, 2)
    display.pixel_span(28, 17, 2)
    display.pixel_span(15, 18, 2)
    display.pixel_span(14, 19, 2)
    display.pixel_span(6, 20, 2)
    display.pixel_span(13, 20, 2)
    display.pixel_span(26, 20, 2)
    display.pixel_span(12, 22, 2)
    display.pixel_span(20, 22, 2)
    display.pixel_span(8, 23, 2)
    display.pixel_span(14, 23, 6)
    display.pixel_span(24, 23, 2)
    display.pixel(11, 13)
    display.pixel(22, 13)
    display.pixel(10, 14)
    display.pixel(10, 20)
    display.pixel(23, 20)
    display.pixel(11, 21)
    display.pixel(22,21)

# Draws the click shape for the corp screen
def corp_click():
    display.rectangle(10, 14, 14, 2)
    display.rectangle(10, 31, 14, 2)
    display.rectangle(9, 15, 2, 2)
    display.rectangle(7, 18, 2, 2)
    display.rectangle(5, 21, 2, 2)
    display.rectangle(5, 24, 2, 2)
    display.rectangle(7, 27, 2, 2)
    display.rectangle(9, 30, 2, 2)
    display.rectangle(23, 30, 2, 2)
    display.rectangle(25, 27, 2, 2)
    display.rectangle(27, 24, 2, 2)
    display.rectangle(27, 21, 2, 2)
    display.rectangle(25, 18, 2, 2)
    display.rectangle(23, 15, 2, 2)
    display.rectangle(17, 19, 1, 5)
    display.rectangle(9, 21, 1, 5)
    display.rectangle(23, 20, 1, 2)
    display.rectangle(24, 22, 1, 4)
    display.pixel_span(8, 17, 2)
    display.pixel_span(14, 17, 6)
    display.pixel_span(24, 17, 2)
    display.pixel_span(12, 18, 2)
    display.pixel_span(20, 18, 2)
    display.pixel_span(6, 20, 2)
    display.pixel_span(26, 20, 2)
    display.pixel_span(4, 23, 2)
    display.pixel_span(28, 23, 2)
    display.pixel_span(15, 24, 2)
    display.pixel_span(14, 25, 2)
    display.pixel_span(6, 26, 2)
    display.pixel_span(13, 26, 2)
    display.pixel_span(26, 26, 2)
    display.pixel_span(12, 28, 2)
    display.pixel_span(20, 28, 2)
    display.pixel_span(8, 29, 2)
    display.pixel_span(14, 29, 6)
    display.pixel_span(24, 29, 2)
    display.pixel(11, 19)
    display.pixel(22, 19)
    display.pixel(10, 20)
    display.pixel(10, 26)
    display.pixel(23, 26)
    display.pixel(11, 27)
    display.pixel(22,27)

# Opening menu screen, here you choose whether you want to track stats for corp or runner
def main_menu():
    if ident == 2:
        display.set_pen(blue)
        display.text("CORP", 80, 10, 240, 4)
        display.set_pen(white)
        display.text("OR", 101, 60, 240, 4)
        display.set_pen(red)
        display.text("RUNNER", 53, 100, 240, 4)
        if button_a.button_just_released():
            set_corp()
        if button_x.button_just_released():
            set_corp()
        if button_b.button_just_released():
            set_runner()
        if button_y.button_just_released():
            set_runner()

# After the menu screen you are asked which ident you are using, this will inform the pen and LED colour
def ident_select():
    if submenu == 1:
        if ident == 0:
            display.set_pen(shaper)
            display.text("Shaper", 10, 10, 240, 3)
            display.set_pen(anarch)
            display.text("Anarch", 140, 10, 240, 3)
            display.set_pen(criminal)
            display.text("Criminal", 10, 110, 240, 3)
            if button_a.button_just_released():
                set_shaper()
            if button_b.button_just_released():
                set_criminal()
            if button_x.button_just_released():
                set_anarch()
        elif ident == 1:
            display.set_pen(HB)
            display.text("HB", 10, 10, 240, 3)
            display.set_pen(jinteki)
            display.text("Jinteki", 130, 10, 240, 3)
            display.set_pen(NBN)
            display.text("NBN", 10, 110, 240, 3)
            display.set_pen(weyland)
            display.text("Weyland", 124, 110, 240, 3)
            if button_a.button_just_released():
                set_HB()
            if button_b.button_just_released():
                set_NBN()
            if button_x.button_just_released():
                set_jinteki()
            if button_y.button_just_released():
                set_weyland()

# The screen a runner sees
def runner_menu():
    if ident == 0 and submenu == 0:
        if button_a.button_just_released():
            cycle_down_selector()
        if button_b.button_just_released():
            cycle_up_selector()
        if button_x.button_just_released():
            clear()
            if selector == 0:
                runner_increment_click()
                corp_increment_click()
            if selector == 1:
                runner_increment_credit()
                corp_increment_credit()
            if selector == 2:
                increment_tag()
                increment_bad_publicity()
            if selector == 3:
                increment_brain_damage()
        if button_y.button_just_released():
            clear()
            if selector == 0:
                runner_decrement_click()
                corp_decrement_click()
            if selector == 1:
                runner_decrement_credit()
                corp_decrement_credit()
            if selector == 2:
                decrement_tag()
                decrement_bad_publicity()
            if selector == 3:
                decrement_brain_damage()
        if selector == 0:            
                set_ident_pen()
                runner_click()
                display.text("{}".format(runner["Click"]), 50, 6, 240, 3)
                display.set_pen(white)
                runner_credit()
                display.text("{}".format(runner["Credits"]), 50, 40, 240, 3)
                tag()
                display.text("{}".format(runner["Tags"]), 50, 73, 240, 3)
                brain_damage()
                display.text("{}".format(runner["Brain Damage"]), 50, 106, 240,3)
        elif selector == 1:            
                display.set_pen(white)
                runner_click()
                display.text("{}".format(runner["Click"]), 50, 6, 240, 3)
                set_ident_pen()
                runner_credit()
                display.text("{}".format(runner["Credits"]), 50, 40, 240, 3)
                display.set_pen(white)
                tag()
                display.text("{}".format(runner["Tags"]), 50, 73, 240, 3)
                brain_damage()
                display.text("{}".format(runner["Brain Damage"]), 50, 106, 240,3)
        elif selector == 2:            
                display.set_pen(white)
                runner_click()
                display.text("{}".format(runner["Click"]), 50, 6, 240, 3)
                runner_credit()
                display.text("{}".format(runner["Credits"]), 50, 40, 240, 3)
                set_ident_pen()
                tag()
                display.text("{}".format(runner["Tags"]), 50, 73, 240, 3)
                display.set_pen(white)
                brain_damage()
                display.text("{}".format(runner["Brain Damage"]), 50, 106, 240,3)
        elif selector == 3:            
                display.set_pen(white)
                runner_click()
                display.text("{}".format(runner["Click"]), 50, 6, 240, 3)
                runner_credit()
                display.text("{}".format(runner["Credits"]), 50, 40, 240, 3)
                tag()
                display.text("{}".format(runner["Tags"]), 50, 73, 240, 3)
                set_ident_pen()
                brain_damage()
                display.text("{}".format(runner["Brain Damage"]), 50, 106, 240,3)

# The screen a corp sees
def corp_menu():
    if ident == 1 and submenu == 0:
        if button_a.button_just_released():
            cycle_down_selector()
        if button_b.button_just_released():
            cycle_up_selector()
        if button_x.button_just_released():
            clear()
            if selector == 0:
                runner_increment_click()
                corp_increment_click()
            if selector == 1:
                runner_increment_credit()
                corp_increment_credit()
            if selector == 2:
                increment_tag()
                increment_bad_publicity()
            if selector == 3:
                increment_brain_damage()
        if button_y.button_just_released():
            clear()
            if selector == 0:
                runner_decrement_click()
                corp_decrement_click()
            if selector == 1:
                runner_decrement_credit()
                corp_decrement_credit()
            if selector == 2:
                decrement_tag()
                decrement_bad_publicity()
            if selector == 3:
                decrement_brain_damage()
        if selector == 0:       
            set_ident_pen()
            corp_click()
            display.text("{}".format(corp["Click"]), 60, 14, 240, 3)
            display.set_pen(white)
            corp_credit()
            display.text("{}".format(corp["Credits"]), 60, 58, 240, 3)
            bad_publicity()
            display.text("{}".format(corp["Bad Publicity"]), 60, 103, 240, 3)
        elif selector == 1:      
            display.set_pen(white)
            corp_click()
            display.text("{}".format(corp["Click"]), 60, 14, 240, 3)
            set_ident_pen()
            corp_credit()
            display.text("{}".format(corp["Credits"]), 60, 58, 240, 3)
            display.set_pen(white)
            bad_publicity()
            display.text("{}".format(corp["Bad Publicity"]), 60, 103, 240, 3)
        elif selector == 2:        
            display.set_pen(white)
            corp_click()
            display.text("{}".format(corp["Click"]), 60, 14, 240, 3)
            corp_credit()
            display.text("{}".format(corp["Credits"]), 60, 58, 240, 3)
            set_ident_pen()
            bad_publicity()
            display.text("{}".format(corp["Bad Publicity"]), 60, 103, 240, 3)

# Render loop
def renderloop():
    global current_time
    new_time = utime.ticks_ms()
    
    button_a.update_button_state()
    button_b.update_button_state()
    button_x.update_button_state()
    button_y.update_button_state()

    if ((new_time - current_time) >= (1000/frame_rate)):
        current_time = new_time

# Updates the display
def update():
    display.update()


# The main code!!

# Clear the screen to start with a blank slate
clear()

# Main loop
while True:
    renderloop()
    corp_menu()
    runner_menu()
    ident_select()
    main_menu()
    update()
