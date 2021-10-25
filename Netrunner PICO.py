import picodisplay as display
import utime

# Initialise display with a bytearray display buffer
buf = bytearray(display.get_width() * display.get_height() * 2)
display.init(buf)
display.set_backlight(0.5)

# define global variables

runner = {
    "Click": 0,
    "Credits": 5,
    "Tags": 0,
    "Brain Damage": 0
    }

corp = {
    "Click": 0,
    "Credits": 5,
    "Bad Publicity": 0
    }

selector = 0

ident = 2
# ident 0 is runner, 1 is corp, 2 is side select

submenu = 0
# when 1 this opens the select ident screen

identPen = 0
#0 is neutral, in order: HB, NBN, JNTK, WLND, CRIM, ANAR, SHPR


rclicks = "Click: {}".format(runner["Click"])
rcredits = "Credits: {}".format(runner["Credits"])
tags = "Tags: {}".format(runner["Tags"])
bd = "Brain Damage: {}".format(runner["Brain Damage"])

cclicks = "Click: {}".format(corp["Click"])
ccredits = "Credits: {}".format(corp["Credits"])
bp = "Bad Publicity: {}".format(corp["Bad Publicity"])

white = display.create_pen(255, 255, 255)
blue = display.create_pen(0, 0, 255)
red = display.create_pen(255, 0, 0)
HB = display.create_pen(127,116,168)
NBN = display.create_pen(242,202,80)
JNTK = display.create_pen(150,27,36)
WLND = display.create_pen(57,115,94)
CRIM = display.create_pen(96,147,222)
ANAR = display.create_pen(242,109,61)
SHPR = display.create_pen(96,181,78)


#define functions

def clear():
    display.set_pen(0, 0, 0)
    display.clear()
    display.update()

def run_increment_click():
    global runner
    if runner["Click"]<4:
        runner["Click"] += 1
    else:
        runner["Click"] = 0
        
def run_decrement_click():
    global runner
    if runner["Click"] > 0:
        runner["Click"] -= 1
    else:
        runner["Click"] = 0


def run_increment_credit():
    global runner
    runner["Credits"] += 1
     
def run_decrement_credit():
    global runner
    if runner["Credits"] > 0:
        runner["Credits"] -= 1
    else:
        runner["Credits"] = 0


def corp_increment_click():
    global corp
    if corp["Click"]<3:
        corp["Click"] += 1
    else:
        corp["Click"] = 0
        
def corp_decrement_click():
    global corp
    if corp["Click"] > 0:
        corp["Click"] -= 1
    else:
        corp["Click"] = 0


def corp_increment_credit():
    global corp
    corp["Credits"] += 1
     
def corp_decrement_credit():
    global corp
    if corp["Credits"] > 0:
        corp["Credits"] -= 1
    else:
        corp["Credits"] = 0

def increment_tag():
    global runner
    runner["Tags"] += 1
        
def decrement_tag():
    global runner
    if runner["Tags"] > 0:
        runner["Tags"] -= 1
    else:
        runner["Tags"] = 0
        

def increment_bd():
    global runner
    runner["Brain Damage"] += 1

def decrement_bd():
    global runner
    if runner["Brain Damage"] > 0:
        runner["Brain Damage"] -= 1
    else:
        runner["Brain Damage"] = 0

def increment_bp():
    global corp
    corp["Bad Publicity"] += 1

def decrement_bp():
    global corp
    if corp["Bad Publicity"] > 0:
        corp["Bad Publicity"] -= 1
    else:
        corp["Bad Publicity"] = 0

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

def cycle_down_selector():
    global selector
    if selector > 0:
        selector -= 1
    else:
        selector = 3

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
    clear()
    utime.sleep(1)

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
    clear()
    utime.sleep(1)

def set_NBN():
    global submenu
    submenu = 0
    global identPen
    identPen = 1
    clear()
    utime.sleep(1)

def set_HB():
    global submenu
    submenu = 0
    global identPen
    identPen = 2
    clear()
    utime.sleep(1)

def set_JNTK():
    global submenu
    submenu = 0
    global identPen
    identPen = 3
    clear()
    utime.sleep(1)
    
def set_WLND():
    global submenu
    submenu = 0
    global identPen
    identPen = 4
    clear()
    utime.sleep(1)

def set_CRIM():
    global submenu
    submenu = 0
    global identPen
    identPen = 5
    clear()
    utime.sleep(1)
    
def set_ANAR():
    global submenu
    submenu = 0
    global identPen
    identPen = 6
    clear()
    utime.sleep(1)
    
def set_SHPR():
    global submenu
    submenu = 0
    global identPen
    identPen = 7
    clear()
    utime.sleep(1)


#the code!!

clear()

while ident == 2:
    display.set_pen(blue)
    display.text("CORP", 75, 10,240, 4)
    display.set_pen(white)
    display.text("OR", 95, 60,240, 4)
    display.set_pen(red)
    display.text("RUNNER", 60, 110,240, 4)
    display.update()
    if display.is_pressed(display.BUTTON_A):
        set_corp()
    if display.is_pressed(display.BUTTON_X):
        set_corp()
    if display.is_pressed(display.BUTTON_B):
        set_runner()
    if display.is_pressed(display.BUTTON_Y):
        set_runner()

while submenu == 1:
    if ident == 0:
        display.set_pen(SHPR)
        display.text("Shaper", 10, 10, 240, 3)
        display.set_pen(ANAR)
        display.text("Anarch", 140, 10, 240, 3)
        display.set_pen(CRIM)
        display.text("Criminal", 10, 110, 240, 3)
        display.update()
        if display.is_pressed(display.BUTTON_A):
            set_SHPR()
        if display.is_pressed(display.BUTTON_B):
            set_CRIM()
        if display.is_pressed(display.BUTTON_X):
            set_ANAR()
    elif ident == 1:
        display.set_pen(HB)
        display.text("HB", 10, 10, 240, 3)
        display.set_pen(JNTK)
        display.text("Jinteki", 130, 10, 240, 3)
        display.set_pen(NBN)
        display.text("NBN", 10, 110, 240, 3)
        display.set_pen(WLND)
        display.text("Weyland", 124, 110, 240, 3)
        display.update()
        if display.is_pressed(display.BUTTON_A):
            set_HB()
        if display.is_pressed(display.BUTTON_B):
            set_NBN()
        if display.is_pressed(display.BUTTON_X):
            set_JNTK()
        if display.is_pressed(display.BUTTON_X):
            set_WLND()

while ident == 0 and submenu == 0:
    if display.is_pressed(display.BUTTON_A):
        cycle_down_selector()
    if display.is_pressed(display.BUTTON_B):
        cycle_up_selector()
    if display.is_pressed(display.BUTTON_X):
        clear()
        if selector == 0:
            run_increment_click()
            corp_increment_click()
        if selector == 1:
            run_increment_credit()
            corp_increment_credit()
        if selector == 2:
            increment_tag()
            increment_bp()
        if selector == 3:
            increment_bd()
    if display.is_pressed(display.BUTTON_Y):
        clear()
        if selector == 0:
            run_decrement_click()
            corp_decrement_click()
        if selector == 1:
            run_decrement_credit()
            corp_decrement_credit()
        if selector == 2:
            decrement_tag()
            decrement_bp()
        if selector == 3:
            decrement_bd()
    if selector == 0:            
            display.set_pen(red)
            display.text("Click: {}".format(runner["Click"]), 10, 10, 240)
            display.set_pen(white)
            display.text("Credits: {}".format(runner["Credits"]), 10, 40, 240)
            display.text("Tags: {}".format(runner["Tags"]), 10, 70, 240)
            display.text("Brain Damage: {}".format(runner["Brain Damage"]), 10, 100, 240)
            display.update()
    elif selector == 1:            
            display.set_pen(white)
            display.text("Click: {}".format(runner["Click"]), 10, 10, 240)
            display.set_pen(red)
            display.text("Credits: {}".format(runner["Credits"]), 10, 40, 240)
            display.set_pen(white)
            display.text("Tags: {}".format(runner["Tags"]), 10, 70, 240)
            display.text("Brain Damage: {}".format(runner["Brain Damage"]), 10, 100, 240)
            display.update()
    elif selector == 2:            
            display.set_pen(white)
            display.text("Click: {}".format(runner["Click"]), 10, 10, 240)
            display.text("Credits: {}".format(runner["Credits"]), 10, 40, 240)
            display.set_pen(red)
            display.text("Tags: {}".format(runner["Tags"]), 10, 70, 240)
            display.set_pen(white)
            display.text("Brain Damage: {}".format(runner["Brain Damage"]), 10, 100, 240)
            display.update()
    elif selector == 3:            
            display.set_pen(white)
            display.text("Click: {}".format(runner["Click"]), 10, 10, 240)
            display.text("Credits: {}".format(runner["Credits"]), 10, 40, 240)
            display.text("Tags: {}".format(runner["Tags"]), 10, 70, 240)
            display.set_pen(red)
            display.text("Brain Damage: {}".format(runner["Brain Damage"]), 10, 100, 240)
            display.update()
    utime.sleep(0.1)

while ident == 1 and submenu == 0:
    if display.is_pressed(display.BUTTON_A):
        cycle_down_selector()
    if display.is_pressed(display.BUTTON_B):
        cycle_up_selector()
    if display.is_pressed(display.BUTTON_X):
        clear()
        if selector == 0:
            run_increment_click()
            corp_increment_click()
        if selector == 1:
            run_increment_credit()
            corp_increment_credit()
        if selector == 2:
            increment_tag()
            increment_bp()
        if selector == 3:
            increment_bd()
    if display.is_pressed(display.BUTTON_Y):
        clear()
        if selector == 0:
            run_decrement_click()
            corp_decrement_click()
        if selector == 1:
            run_decrement_credit()
            corp_decrement_credit()
        if selector == 2:
            decrement_tag()
            decrement_bp()
        if selector == 3:
            decrement_bd()
    if selector == 0:       
        display.set_pen(blue)
        display.text("Click: {}".format(corp["Click"]), 10, 10, 240)
        display.set_pen(white)
        display.text("Credits: {}".format(corp["Credits"]), 10, 60, 240)
        display.text("Bad Publicity: {}".format(corp["Bad Publicity"]), 10, 110, 240)
        display.update()
    elif selector == 1:      
        display.set_pen(white)
        display.text("Click: {}".format(corp["Click"]), 10, 10, 240)
        display.set_pen(blue)
        display.text("Credits: {}".format(corp["Credits"]), 10, 60, 240)
        display.set_pen(white)
        display.text("Bad Publicity: {}".format(corp["Bad Publicity"]), 10, 110, 240)
        display.update()
    elif selector == 2:        
        display.set_pen(white)
        display.text("Click: {}".format(corp["Click"]), 10, 10, 240)
        display.text("Credits: {}".format(corp["Credits"]), 10, 60, 240)
        display.set_pen(blue)
        display.text("Bad Publicity: {}".format(corp["Bad Publicity"]), 10, 110, 240)
        display.update()
    utime.sleep(0.1)
