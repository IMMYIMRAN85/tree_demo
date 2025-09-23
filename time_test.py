import time
import board, busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

# I2C setup
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# Load default font
font = ImageFont.load_default()

while True:
    # Get current time
    current_time = time.strftime("%H:%M:%S")  # 24-hour format
    current_date = time.strftime("%Y-%m-%d")  # YYYY-MM-DD

    # Clear display
    oled.fill(0)
    oled.show()

    # Create image for drawing
    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)

    # Draw time and date
    draw.text((0, 0), "Time: " + current_time, font=font, fill=255)
    draw.text((0, 16), "Date: " + current_date, font=font, fill=255)

    # Show on OLED
    oled.image(image)
    oled.show()

    time.sleep(1)  # update every second
