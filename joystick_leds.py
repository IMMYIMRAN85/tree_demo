#!/usr/bin/env python3
#Raspberry Pi 4 + PCF8591 + Joystick + 5 LEDs
#--------------------------------------------
#- Joystick X/Y via PCF8591 analog inputs
#- Joystick SW button via GPIO18
#- LEDs show UP, DOWN, LEFT, RIGHT movement, and CENTER when pressed

import time
import sys
import signal
from smbus import SMBus
from gpiozero import LED, Button


PIN_UP = 17      # GPIO17 -> UP LED
PIN_DOWN = 27    # GPIO27 -> DOWN LED
PIN_LEFT = 22    # GPIO22 -> LEFT LED
PIN_RIGHT = 23   # GPIO23 -> RIGHT LED
PIN_CENTER = 24  # GPIO24 -> CENTER press LED
PIN_SW = 18      # GPIO18 -> Joystick button (SW)

I2C_BUS = 1
PCF8591_ADDR = 0x48  # A0,A1,A2 tied to GND
CHAN_X = 0           # AIN0
CHAN_Y = 1           # AIN1
DEADZONE = 30        # ignore jitter near center (0-255 scale)


led_up = LED(PIN_UP)
led_down = LED(PIN_DOWN)
led_left = LED(PIN_LEFT)
led_right = LED(PIN_RIGHT)
led_center = LED(PIN_CENTER)

button = Button(PIN_SW, pull_up=True, bounce_time=0.02)  # Press = LOW

bus = SMBus(I2C_BUS)


def pcf8591_read(channel: int) -> int:
    """Read one channel (0-3) from PCF8591, return value 0-255"""
    if not 0 <= channel <= 3:
        raise ValueError("Channel must be 0-3")
    ctrl = 0x40 | channel
    bus.write_byte(PCF8591_ADDR, ctrl)
    _ = bus.read_byte(PCF8591_ADDR)   # dummy read
    return bus.read_byte(PCF8591_ADDR)

def calibrate_center(samples=30):
    """Read several samples to estimate joystick center"""
    sum_x, sum_y = 0, 0
    for _ in range(samples):
        sum_x += pcf8591_read(CHAN_X)
        sum_y += pcf8591_read(CHAN_Y)
        time.sleep(0.01)
    return sum_x / samples, sum_y / samples


def set_leds(up=False, down=False, left=False, right=False, center=False):
    led_up.value = 1 if up else 0
    led_down.value = 1 if down else 0
    led_left.value = 1 if left else 0
    led_right.value = 1 if right else 0
    led_center.value = 1 if center else 0

def cleanup(sig=None, frame=None):
    set_leds(False, False, False, False, False)
    bus.close()
    sys.exit(0)
    
signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

def main():
    print("Calibrating joystick center... Keep it still.")
    cx, cy = calibrate_center()
    print(f"Center X {cx:.1f}, Y {cy:.1f}")

while True:
        x = pcf8591_read(CHAN_X)
        y = pcf8591_read(CHAN_Y)

        dx = x - cx
        dy = y - cy
        
        up = dy < -DEADZONE
        down = dy > DEADZONE
        left = dx < -DEADZONE
        right = dx > DEADZONE
        center = not button.is_pressed  # button pressed = LOW

        set_leds(up, down, left, right, center)

        time.sleep(0.05)

if __name__ == "__main__":
    main()
