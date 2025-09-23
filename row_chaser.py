# file: row_chaser.py
import time
import scan_driver as led   # uses your working driver

def row_chaser(delay=1.0, loops=5):
    for _ in range(loops):
        for r in range(8):      # row 0 ? row 7
            led.clear()
            for c in range(8):  # light whole row
                led.set_pixel(c, r, True)
            t0 = time.time()
            while time.time() - t0 < delay:
                led.scan_once()

if __name__ == "__main__":
    try:
        led.clear()
        for _ in range(8): led.scan_once()   # blank quickly
        row_chaser(delay=1.0, loops=20)
    finally:
        led.clear()
        for _ in range(8): led.scan_once()
