from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY
from pimoroni import RGBLED
import buttons
import utime
import jpegdec

# Define the time for the render and logic loops
render_time = utime.ticks_ms()
logic_time = utime.ticks_ms()
frame_rate = 60
logic_rate = 5

# Define the display
d = PicoGraphics(display=DISPLAY_PICO_DISPLAY, rotate=0)

# Create a new JPEG decoder for our PicoGraphics
j = jpegdec.JPEG(d)

# define pen colours including specific colours for each ident 
black = d.create_pen(0, 0, 0)
white = d.create_pen(255, 255, 255)
blue = d.create_pen(0, 0, 255)
red = d.create_pen(255, 0, 0)
HB = d.create_pen(127,116,168)
NBN = d.create_pen(242,202,80)
jinteki = d.create_pen(150,27,36)
weyland = d.create_pen(57,115,94)
criminal = d.create_pen(96,147,222)
anarch = d.create_pen(226,106,53)
shaper = d.create_pen(96,181,78)

d.set_font("bitmap8")

# Clear Screen
def clear():
    d.set_pen(black)
    d.clear()

# Define LED
led = RGBLED(6, 7, 8)
led.set_rgb(0,0,0)


# define LED colours including specific colours for each ident 
def led_black():
    led.set_rgb(0, 0, 0)
def led_white():
    led.set_rgb(255, 255, 255)
def led_blue():
    led.set_rgb(0, 0, 255)
def led_red():
    led.set_rgb(255, 0, 0)
def led_HB():
    led.set_rgb(127,116,168)
def led_NBN():
    led.set_rgb(242,202,80)
def led_jinteki():
    led.set_rgb(150,27,36)
def led_weyland():
    led.set_rgb(57,115,94)
def led_criminal():
    led.set_rgb(96,147,222)
def led_anarch():
    led.set_rgb(226,106,53)
def led_shaper():
    led.set_rgb(96,181,78)

# Define the list:
# Side - None, Corp, Runner
# Ident - None, HB, Jinteki, NBN, Weyland, Anarch, Criminal, Shaper
# Clicks
# Credits 
# Tags
# BD
# BP
player = [0, 0, 0, 5, 0, 0, 0]

def set_corp():
    player[0]=1
    led_blue()

def set_runner():
    player[0]=2
    led_red()

def set_HB():
    player[1]=1
    d.set_pen(HB)
    led_HB()
    j.open_file("HB.jpg")
    j.decode(0, 0, jpegdec.JPEG_SCALE_FULL, dither=True)

def set_jinteki():
    player[1]=2
    d.set_pen(jinteki)
    led_jinteki()

def set_NBN():
    player[1]=3
    d.set_pen(NBN)
    led_NBN()

def set_weyland():
    player[1]=4
    d.set_pen(weyland)
    led_weyland()

def set_anarch():
    player[1]=5
    d.set_pen(anarch)
    led_anarch()

def set_criminal():
    player[1]=6
    d.set_pen(criminal)
    led_criminal()
    
def set_shaper():
    player[1]=7
    d.set_pen(shaper)
    led_shaper()

def click_up():
    player[2]+=1

def click_down():
    player[2]-=1

def credit_up():
    player[3]+=1

def credit_down():
    player[3]-=1

def tag_up():
    player[4]+=1

def tag_down():
    player[4]-=1

def bd_up():
    player[5]+=1

def bd_down():
    player[5]-=1
    
def bp_up():
    player[6]+=1

def bp_down():
    player[6]-=1

def reset():
    global player
    player.clear()
    player = [0, 0, 0, 5, 0, 0, 0]
    d.set_backlight(1)

# Variable to remember the list item selected
selector = 0

# Render loop
def render_loop():
    global render_time
    new_render_time = utime.ticks_ms()

    if ((new_render_time - render_time) >= (1000/frame_rate)):
        render_time = new_render_time
        buttons.key_update()
        d.update()
        clear()

# Side selection
def main_menu():
    global player
    if player[0] == 0:
        led_black()
        d.set_pen(blue)
        d.text("CORP", 80, 10, scale=4)
        d.set_pen(white)
        d.text("OR", 101, 60, scale=4)
        d.set_pen(red)
        d.text("RUNNER", 60	, 100, scale=4)
        if buttons.button_a.key_just_released():
            set_corp()
        if buttons.button_x.key_just_released():
            set_corp()
        if buttons.button_b.key_just_released():
            set_runner()
        if buttons.button_y.key_just_released():
            set_runner()


# Ident selection
def ident():
    global player
    if player[0]==1 and player[1]==0:
        d.set_pen(HB)
        d.text("HB", 10, 10, 240, 3)
        d.set_pen(jinteki)
        d.text("Jinteki", 130, 10, 240, 3)
        d.set_pen(NBN)
        d.text("NBN", 10, 110, 240, 3)
        d.set_pen(weyland)
        d.text("Weyland", 124, 110, 240, 3)
        if buttons.button_a.key_just_released():
            set_HB()
        if buttons.button_b.key_just_released():
            set_NBN()
        if buttons.button_x.key_just_released():
            set_jinteki()
        if buttons.button_y.key_just_released():
            set_weyland()       
    elif player[0]==2 and player[1]==0:
        d.set_pen(shaper)
        d.text("Shaper", 10, 10, 240, 3)
        d.set_pen(anarch)
        d.text("Anarch", 140, 10, 240, 3)
        d.set_pen(criminal)
        d.text("Criminal", 10, 110, 240, 3)
        if buttons.button_a.key_just_released():
            set_shaper()
        if buttons.button_x.key_just_released():
            set_anarch()
        if buttons.button_b.key_just_released():
            set_criminal()

# Runner logic
def runner():
    global player
    if player[0]==2 and player[1]!=0:  
        # Initialising the correct backgrounds
        if player[1]==5:
            j.open_file("Anarch.jpg")
            j.decode(0, 0, jpegdec.JPEG_SCALE_FULL, dither=True)
            d.set_pen(anarch)
            d.text("Click - " + "{}".format(player[2]), 0, 0, scale=2)
            d.text("Credits - " + "{}".format(player[3]), 0, 25, scale=2)
            d.text("Tags - " + "{}".format(player[4]), 0, 50, scale=2)
            d.text("BD - " + "{}".format(player[5]), 0, 75, scale=2)
        if player[1]==6:
            j.open_file("Criminal.jpg")
            j.decode(0, 0, jpegdec.JPEG_SCALE_FULL, dither=True)
            d.set_pen(criminal)
            d.text("Click - " + "{}".format(player[2]), 0, 0, scale=2)
            d.text("Credits - " + "{}".format(player[3]), 0, 25, scale=2)
            d.text("Tags - " + "{}".format(player[4]), 0, 50, scale=2)
            d.text("BD - " + "{}".format(player[5]), 0, 75, scale=2)
        if player[1]==7:
            j.open_file("Shaper.jpg")
            j.decode(0, 0, jpegdec.JPEG_SCALE_FULL, dither=True)
            d.set_pen(shaper)
            d.text("Click - " + "{}".format(player[2]), 0, 0, scale=2)
            d.text("Credits - " + "{}".format(player[3]), 0, 25, scale=2)
            d.text("Tags - " + "{}".format(player[4]), 0, 50, scale=2)
            d.text("BD - " + "{}".format(player[5]), 0, 75, scale=2)
            
        # Runner item selection functionality
        global selector
        r = selector
        if r == 0:
            d.set_pen(white)
            d.text("Click - " + "{}".format(player[2]), 0, 0, scale=2)
            if buttons.button_a.key_just_released():
                selector = 3
            if buttons.button_b.key_just_released():
                selector = 1
            if buttons.button_x.key_just_released() and player[2]<=3:
                click_up()
            elif buttons.button_x.key_just_released() and player[2]>=3:
                player[2] = 0
            elif buttons.button_y.key_just_released() and player[2]>0:
                click_down()
        elif r == 1:
            d.set_pen(white)
            d.text("Credits - " + "{}".format(player[3]), 0, 25, scale=2)
            if buttons.button_a.key_just_released():
                selector = 0
            if buttons.button_b.key_just_released():
                selector = 2
            if buttons.button_x.key_just_released():
                credit_up()
            elif buttons.button_y.key_just_released() and player[3]>0:
                credit_down()
        elif r == 2:
            d.set_pen(white)
            d.text("Tags - " + "{}".format(player[4]), 0, 50, scale=2)
            if buttons.button_a.key_just_released():
                selector = 1
            if buttons.button_b.key_just_released():
                selector = 3
            if buttons.button_x.key_just_released():
                tag_up()
            elif buttons.button_y.key_just_released() and player[4]>0:
                tag_down()
        elif r == 3:
            d.set_pen(white)
            d.text("BD - " + "{}".format(player[5]), 0, 75, scale=2)
            if buttons.button_a.key_just_released():
                selector = 2
            if buttons.button_b.key_just_released():
                selector = 0
            if buttons.button_x.key_just_released():
                bd_up()
            elif buttons.button_y.key_just_released() and player[5]>0:
                bd_down()

# Corp logic
def corp():
    global player
    if player[0]==1 and player[1]!=0:
        if player[1]==1:
            j.open_file("HB.jpg")
            j.decode(0, 0, jpegdec.JPEG_SCALE_FULL, dither=True)
            d.set_pen(HB)
            d.text("Click - " + "{}".format(player[2]), 0, 0, scale=2)
            d.text("Credits - " + "{}".format(player[3]), 0, 25, scale=2)
            d.text("BP - " + "{}".format(player[6]), 0, 50, scale=2)
        if player[1]==2:
            j.open_file("Jinteki.jpg")
            j.decode(0, 0, jpegdec.JPEG_SCALE_FULL, dither=True)
            d.set_pen(jinteki)
            d.text("Click - " + "{}".format(player[2]), 0, 0, scale=2)
            d.text("Credits - " + "{}".format(player[3]), 0, 25, scale=2)
            d.text("BP - " + "{}".format(player[6]), 0, 50, scale=2)
        if player[1]==3:
            j.open_file("NBN.jpg")
            j.decode(0, 0, jpegdec.JPEG_SCALE_FULL, dither=True)
            d.set_pen(NBN)
            d.text("Click - " + "{}".format(player[2]), 0, 0, scale=2)
            d.text("Credits - " + "{}".format(player[3]), 0, 25, scale=2)
            d.text("BP - " + "{}".format(player[6]), 0, 50, scale=2)
        if player[1]==4:
            j.open_file("Weyland.jpg")
            j.decode(0, 0, jpegdec.JPEG_SCALE_FULL, dither=True)
            d.set_pen(weyland)
            d.text("Click - " + "{}".format(player[2]), 0, 0, scale=2)
            d.text("Credits - " + "{}".format(player[3]), 0, 25, scale=2)
            d.text("BP - " + "{}".format(player[6]), 0, 50, scale=2)
       
   # Corp item selection functionality
        global selector
        r = selector
        if r == 0:
            d.set_pen(white)
            d.text("Click - " + "{}".format(player[2]), 0, 0, scale=2)
            if buttons.button_a.key_just_released():
                selector = 2
            if buttons.button_b.key_just_released():
                selector = 1
            if buttons.button_x.key_just_released() and player[2]<=2:
                click_up()
            elif buttons.button_x.key_just_released() and player[2]>=2:
                player[2] = 0
            elif buttons.button_y.key_just_released() and player[2]>0:
                click_down()
        elif r == 1:
            d.set_pen(white)
            d.text("Credits - " + "{}".format(player[3]), 0, 25, scale=2)
            if buttons.button_a.key_just_released():
                selector = 0
            if buttons.button_b.key_just_released():
                selector = 2
            if buttons.button_x.key_just_released():
                credit_up()
            elif buttons.button_y.key_just_released() and player[3]>0:
                credit_down()
        elif r == 2:
            d.set_pen(white)
            d.text("BP - " + "{}".format(player[6]), 0, 50, scale=2)
            if buttons.button_a.key_just_released():
                selector = 1
            if buttons.button_b.key_just_released():
                selector = 0
            if buttons.button_x.key_just_released():
                bp_up()
            elif buttons.button_y.key_just_released() and player[6]>0:
                bp_down()

while True:
    render_loop()
    corp()
    runner()
    ident()
    main_menu()
    if buttons.button_x.key_pressed() and buttons.button_y.key_pressed():
        clear()
        d.set_backlight(0)
        led.set_rgb(0,0,0)
        utime.sleep(5)
        render_loop()
        reset()
        continue
        