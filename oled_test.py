import time
import board, busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

#!/home/imran/rpi_projects/tree_demo/venv/bin/pythonimport time
import board, busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

# I2C setup
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# Function to display text
def show_message(text):
    oled.fill(0)         # clear the screen
    oled.show()
    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    draw.text((0, 10), text, font=font, fill=255)
    oled.image(image)
    oled.show()

# Show first message
show_message("Hello World")
time.sleep(3)  # wait 3 seconds

# Show second message
show_message("I am Good!")
time.sleep(3)  # wait 3 seconds
