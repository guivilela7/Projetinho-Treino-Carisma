from screeninfo import get_monitors
from mss import mss
import mss.tools
import keyboard as direct_keyboard
from pytesseract import pytesseract
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import difflib
import cv2 as cv
import PySimpleGUI as psg
import time
import re
import threading
from pynput import keyboard as pykey


path_to_tesseract = "./_internal/Tesseract/tesseract.exe"

all_quotes = ["Some weather we're having, huh?", "Hey hivekin, can I bug you for a moment?",
              "Sometimes I have really deep thoughts about life and stuff.", "So, how's work?",
              "Me-wow, is that the latest Felinor fashion?", "Wow, this breeze is great, right?",
              "You ever been to a Canor restaurant? The food's pretty howlright.",
              "So, what's keeping you busy these days?"]

# Providing the tesseract executable
# location to pytesseract library
pytesseract.tesseract_cmd = path_to_tesseract


def get_area_primary_monitor():
    for m in get_monitors():
        if m.is_primary:
            height = m.height * 0.405
            width = m.width * 0.40
            return height, width


def take_screenshot(top, left):
    with mss.mss() as sct:
        # The screen part to capture
        monitor = {"top": top, "left": left, "width": 400, "height": 50}
        output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)

        # Grab the data
        sct_img = sct.grab(monitor)

        # Save to the picture file
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
        return output


def grayscale(imgPath):
    image = cv.imread(imgPath)
    grayIMG = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    return grayIMG


def checkKey(key):
    global on
    global window
    if key == pykey.Key.f8:
        on = not on
        if on:
            window["Press F8 to Start/Stop"].update(button_color="green")
        else:
            window["Press F8 to Start/Stop"].update(button_color="#283b5b")


def running():
    global on
    global threadEvent
    area = get_area_primary_monitor()
    while not threadEvent.is_set():
        if on:
            image_path = take_screenshot(int(area[0]), int(area[1]))
            img = grayscale(image_path)
            ret, img = cv.threshold(img, 204, 255, cv.THRESH_BINARY_INV)

            text = pytesseract.image_to_string(img, config="-c tessedit_char_whitelist=' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ?-,'")

            if re.search("Try some", text):
                text = re.sub("^.*?\n", "", text)

            fuzz.SequenceMatcher = difflib.SequenceMatcher
            result = process.extractOne(text, all_quotes)

            if result[1] > 80:
                direct_keyboard.write(result[0])
                time.sleep(0.2)
                direct_keyboard.press("enter")


def gui():
    global threadEvent
    global layout
    global window

    while True:
        event, values = window.read(timeout=100)
        if event == psg.WIN_CLOSED or event == "Close":
            threadEvent.set()
            window.close()
            break


threadEvent = threading.Event()

on = False

layout = [[psg.Button(button_text="Press F8 to Start/Stop", size=(30, 2))], [psg.Button("Close", size=(30, 2))]]

window = psg.Window("Auto Charisma", layout, resizable=True)

listener = pykey.Listener(on_press=checkKey)
run = threading.Thread(target=running, daemon=True)
guiRun = threading.Thread(target=gui, daemon=True)
guiRun.start()
time.sleep(1)
listener.start()
run.start()

guiRun.join()
