import time, spidev

# ==== TUNE THESE IF NEEDED ====
SPI_BUS, SPI_DEV = 0, 0
SPI_HZ = 1_000_000            # lower to 500_000 if you see artifacts
SPI_MODE = 0                  # 0 or 1; most boards are fine with 0

INVERT_ROWS = True            # many 8x8 boards have active-LOW rows
INVERT_COLS = False           # and active-HIGH columns
FIRST_BYTE_IS_ROWS = True     # first shifted byte -> rows; second -> columns
# ==============================

spi = spidev.SpiDev()
spi.open(SPI_BUS, SPI_DEV)
spi.max_speed_hz = SPI_HZ
spi.mode = SPI_MODE

frame = [0]*8  # 8 rows, each a bitmask of 8 columns

def _rows_mask(row):
    m = 1 << row
    return (m ^ 0xFF) & 0xFF if INVERT_ROWS else m & 0xFF

def _cols_mask(bits):
    b = bits & 0xFF
    return b ^ 0xFF if INVERT_COLS else b

def _write16(rows_byte, cols_byte):
    if FIRST_BYTE_IS_ROWS:
        spi.xfer2([rows_byte & 0xFF, cols_byte & 0xFF])
    else:
        spi.xfer2([cols_byte & 0xFF, rows_byte & 0xFF])

def clear():
    for i in range(8): frame[i] = 0

def set_pixel(x, y, on=True):
    if 0 <= x < 8 and 0 <= y < 8:
        if on:  frame[y] |=  (1 << x)
        else:   frame[y] &= ~(1 << x)

def scan_once():
    for r in range(8):
        _write16(_rows_mask(r), _cols_mask(frame[r]))

def blank_immediately():
    # no row selected -> blank
    _write16(0x00 if not INVERT_ROWS else 0xFF, 0x00 if not INVERT_COLS else 0xFF)

def demo_bounce(t_secs=6):
    clear()
    x,y,dx,dy = 0,0,1,1
    t0 = time.time()
    logic_dt = 0
    while time.time()-t0 < t_secs:
        scan_once()
        logic_dt += 1
        if logic_dt >= 50:     # ~50 scans per logic step
            clear(); set_pixel(x,y,True)
            x += dx; y += dy
            if x<=0 or x>=7: dx*=-1
            if y<=0 or y>=7: dy*=-1
            logic_dt = 0

def demo_row_col_sweep():
    clear()
    # light each row with a walking column to confirm orientation
    for r in range(8):
        for c in range(8):
            clear(); set_pixel(c, r, True)
            t = time.time()+0.12
            while time.time() < t:
                scan_once()

if __name__ == "__main__":
    try:
        blank_immediately()
        # small pause so you can see it blank
        t = time.time()+0.5
        while time.time() < t: scan_once()

        demo_row_col_sweep()
        demo_bounce(6)

    finally:
        clear()
        for _ in range(8): scan_once()
        spi.close()
