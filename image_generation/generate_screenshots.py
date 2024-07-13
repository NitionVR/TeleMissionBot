from mss import mss
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import time

def capture_screenshot_with_text(output_filename, text):
    with mss() as sct:
        
        screenshot_filename = 'screenshot.png'
        time.sleep(10)
        screenshot = sct.shot(output=screenshot_filename)

        
        img = Image.open(screenshot_filename)

        
        draw = ImageDraw.Draw(img)

        
        font = ImageFont.load_default()
        text_position = (500, 500)  

        
        draw.text(text_position, text, font=font, fill=(255, 0, 0))

        
        img.save(output_filename)


output_filename = 'screenshot_with_text.png'
text_to_overlay = 'M8'
capture_screenshot_with_text(output_filename, text_to_overlay)



