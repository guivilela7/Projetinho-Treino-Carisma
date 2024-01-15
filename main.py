from screeninfo import get_monitors
from mss import mss
import mss.tools
import keyboard
from pytesseract import pytesseract
from PIL import Image
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import difflib
import cv2 as cv


path_to_tesseract = "./Tesseract/tesseract.exe"

all_quotes = ["Some weather we're having, huh?", "Hey hivekin, can I bug you for a moment?",
              "Sometimes I have really deep thoughts about life and stuff.", "So, how's work?",
              "Me-wow, is that the latest Felinor fashion?", "Wow, this breeze is great, right?",
              "You ever been to a Canor restaurant? The food's pretty howlright.",
              "So, what's keeping you busy these days?"]


def get_area_primary_monitor():
    for m in get_monitors():
        if m.is_primary:
            height = m.height * 0.41
            width = m.width * 0.40
            return height, width


def take_screenshot(top, left):
    with mss.mss() as sct:
        # The screen part to capture
        monitor = {"top": top, "left": left, "width": 400, "height": 35}
        output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)

        # Grab the data
        sct_img = sct.grab(monitor)

        # Save to the picture file
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
        print(output)
        return output

def grayscale(imgPath):
    image = cv.imread(imgPath)
    grayIMG = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    return grayIMG



area = get_area_primary_monitor()
print(area)
image_path = take_screenshot(int(area[0]), int(area[1]))
# image_path = "sct-442x768_400x35.png"

print(image_path)



img = grayscale(image_path)

ret, img = cv.threshold(img, 204, 255, cv.THRESH_BINARY_INV)

# cv.imshow('THRESHOLH IMAGE', img)
# cv.waitKey(0)
# cv.destroyAllWindows()

# Providing the tesseract executable
# location to pytesseract library
pytesseract.tesseract_cmd = path_to_tesseract

# Passing the image object to image_to_string() function
# This function will extract the text from the image
text = pytesseract.image_to_string(img, config="-c tessedit_char_whitelist=' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ?-,'")

# Displaying the extracted text
print(text)

fuzz.SequenceMatcher = difflib.SequenceMatcher
result = process.extractOne(text, all_quotes)
print(result)
if result[1] > 80:
    keyboard.write(result[0])
    keyboard.press("enter")
