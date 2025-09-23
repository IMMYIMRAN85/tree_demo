import time, spidev

BUS, DEV = 0, 0
SPEEDS = [500000, 1000000, 2000000]       # try a few
MODES  = [0, 1]                            # CPOL/CPHA combos that 74HC595 tolerates

def write_pair(spi, b1, b2):
    # Send two bytes; CE0 acts as latch (goes high at end of transfer)
    spi.xfer2([b1 & 0xFF, b2 & 0xFF])

def show_banner(spi, label, on_bytes):
    print(label, "->", [hex(x) for x in on_bytes])
    # ON
    for _ in range(50):
        write_pair(spi, *on_bytes)
        time.sleep(0.01)
    # OFF
    for _ in range(50):
        write_pair(spi, 0x00, 0x00)
        time.sleep(0.01)

def main():
    for hz in SPEEDS:
        for mode in MODES:
            spi = spidev.SpiDev()
            spi.open(BUS, DEV)
            spi.max_speed_hz = hz
            spi.mode = mode
            print(f"\n=== speed={hz} mode={mode} ===")
            # Four plausible mappings:
            # A) rows first, rows active-LOW; cols active-HIGH (common)
            show_banner(spi, "A rows-first, rows LOW, cols HIGH", (0xFE, 0xFF))
            # B) rows first, rows HIGH, cols LOW
            show_banner(spi, "B rows-first, rows HIGH, cols LOW", (0x01, 0x00))
            # C) cols first, rows LOW, cols HIGH
            show_banner(spi, "C cols-first, rows LOW, cols HIGH", (0xFF, 0xFE))
            # D) cols first, rows HIGH, cols LOW
            show_banner(spi, "D cols-first, rows HIGH, cols LOW", (0x00, 0x01))
            spi.close()

if __name__ == "__main__":
    main()

