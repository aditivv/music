import time
import requests
from RPLCD.gpio import CharLCD
import RPi.GPIO as GPIO

# Setup LCD
lcd = CharLCD(
    cols=16, rows=2,
    pin_rs=15, pin_e=21,
    pins_data=[20, 19, 13, 6],
    numbering_mode=GPIO.BCM
)

def get_song_title():
    try:
        response = requests.get("http://localhost/api/v1/getstate", timeout=2)
        data = response.json()
        title = data.get("title", "")
        artist = data.get("artist", "")
        return title, artist
    except:
        return "No track", ""

def scroll_text(text, row, delay=0.3):
    if len(text) <= 16:
        lcd.cursor_pos = (row, 0)
        lcd.write_string(text.ljust(16))
    else:
        padded = text + "    "
        for i in range(len(padded)):
            lcd.cursor_pos = (row, 0)
            lcd.write_string((padded[i:] + padded)[:16])
            time.sleep(delay)

last_title = ""

try:
    lcd.clear()
    lcd.write_string("Volumio Player")
    time.sleep(2)

    while True:
        title, artist = get_song_title()
        if title != last_title:
            lcd.clear()
            last_title = title
        scroll_text(title or "No track", 0)
        scroll_text(artist or "", 1)
        time.sleep(0.3)

except KeyboardInterrupt:
    lcd.clear()
    GPIO.cleanup()