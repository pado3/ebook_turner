# ebook_turner.py 電子書籍めくり機 for Android with Seeeduino XIAO
# copyright (c) by @pado3
# ver.1.0 2021/10/16
# Note: ReaderはUPで戻りDOWNで送る。Kinoppyは逆。読書尚友・なろうリーダは選択可能。
import time
import board
import digitalio
import usb_hid

# consumer control code library
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

# mouse library
from adafruit_hid.mouse import Mouse

# Sleep for a bit to avoid a race condition on some systems
time.sleep(1)
control = ConsumerControl(usb_hid.devices)
mouse = Mouse(usb_hid.devices)

# define switch pins
sw_pin_array = []
sw_pins = [board.D7, board.D6, board.D5]
sw_pressed = [
    Mouse.RIGHT_BUTTON,
    ConsumerControlCode.VOLUME_INCREMENT,
    ConsumerControlCode.VOLUME_DECREMENT,
]

# Make all pin objects inputs with pullups
for pin in sw_pins:
    sw_pin = digitalio.DigitalInOut(pin)
    sw_pin.direction = digitalio.Direction.INPUT
    sw_pin.pull = digitalio.Pull.UP
    sw_pin_array.append(sw_pin)

# LED setting
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

while True:
    # Check each pin
    for sw_pin in sw_pin_array:
        if not sw_pin.value:  # LOW = Pressed
            led.value = False
            i = sw_pin_array.index(sw_pin)
            print("Pin #%d is grounded." % i)
            while not sw_pin.value:
                pass  # Wait for release the switch
            # output UP/DOWN/RIGHT function code
            func = sw_pressed[i]  # Get the corresponding function code
            if i:   # if i is not zero, send control code
                control.send(func)
            else:   # if i is zero, click mouse
                mouse.click(func)
            # Turn off the red LED
            led.value = True
    time.sleep(0.2)
