# file: scroll_hashim.py
import time
import scan_driver as led  # uses your working SPI + flags

# 5x7 font columns (LSB = top row). Only letters we need.
FONT = {
    "H": [0b10001,0b10001,0b11111,0b10001,0b10001],
    "A": [0b01110,0b10001,0b11111,0b10001,0b10001],
    "S": [0b01111,0b10000,0b01110,0b00001,0b11110],
    "I": [0b11111,0b00100,0b00100,0b00100,0b11111],
    "M": [0b10001,0b11011,0b10101,0b10001,0b10001],
    " ": [0,0,0,0,0],
}

def build_columns(text):
    cols = []
    for ch in text:
        glyph = FONT.get(ch.upper(), FONT[" "])
        # Each glyph is 5 columns wide; add one blank column as spacing
        cols.extend(glyph + [0])
    return cols

def scroll(text="HAS", speed=0.10):
    cols = build_columns(text)
    width = len(cols)
    # pad 8 blanks at the end so it scrolls fully off
    cols.extend([0]*8)

    while True:
        for shift in range(len(cols) - 7):
            # Build the 8x8 frame from the current 8-column window
            for y in range(8):
                rowbits = 0
                for x in range(8):
                    # y 0..6 contain glyph; y==7 blank baseline
                    bit = 0
                    if y < 7:
                        bit = (cols[shift + x] >> y) & 1
                    rowbits |= (bit << x)
                led.frame[y] = rowbits

            # keep scanning fast for persistence; hold this frame ~speed seconds
            t0 = time.time()
            while time.time() - t0 < speed:
                led.scan_once()

if __name__ == "__main__":
    try:
        led.clear()
        for _ in range(8): led.scan_once()   # quick blank
        scroll(" HASHIM ")
    finally:
        led.clear()
        for _ in range(8): led.scan_once()
