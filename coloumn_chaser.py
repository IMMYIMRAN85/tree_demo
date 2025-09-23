# file: row_col_pixel_skipper.py
import time
import scan_driver as led  # your working driver

def row_pixel_runner(delay=0.2, loops=3, direction="LR", skip=True):
    """
    Runs across rows, lighting one pixel at a time.
    skip=True -> only use rows 0,2,4,6 (skips 1,3,5,7)
    direction: "LR" = left?right, "RL" = right?left
    """
    for _ in range(loops):
        row_range = range(0, 8, 2) if skip else range(8)
        for r in row_range:
            cols = range(8) if direction == "LR" else range(7, -1, -1)
            for c in cols:
                led.clear()
                led.set_pixel(c, r, True)
                t0 = time.time()
                while time.time() - t0 < delay:
                    led.scan_once()

def col_pixel_runner(delay=0.2, loops=3, direction="TB", skip=True):
    """
    Runs across columns, lighting one pixel at a time.
    skip=True -> only use cols 0,2,4,6 (skips 1,3,5,7)
    direction: "TB" = top?bottom, "BT" = bottom?top
    """
    for _ in range(loops):
        col_range = range(0, 8, 2) if skip else range(8)
        for c in col_range:
            rows = range(8) if direction == "TB" else range(7, -1, -1)
            for r in rows:
                led.clear()
                led.set_pixel(c, r, True)
                t0 = time.time()
                while time.time() - t0 < delay:
                    led.scan_once()

if __name__ == "__main__":
    try:
        led.clear()
        # run rows left?right, skipping every other row
        row_pixel_runner(delay=0.25, loops=1, direction="LR", skip=True)
        # run cols top?bottom, skipping every other column
        col_pixel_runner(delay=0.25, loops=1, direction="TB", skip=True)
    finally:
        led.clear()
        for _ in range(8): 
            led.scan_once()

