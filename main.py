from screeninfo import get_monitors
from mss import mss
import mss.tools
from pytesseract import pytesseract
from PIL import Image
from fuzzywuzzy import process

path_to_tesseract = r"F:\Projetinho Treino Carisma\Tesseract\tesseract.exe"

all_quotes = ["Some weather we're having, huh?", "Hey hivekin, can I bug you for a moment?", "Sometimes I have really deep thoughts about life and stuff.", "So, how's work?", "Me-wow, is that the latest Felinor fashion?", "Wow, this breeze is great, right?", "You ever been to a Canor restaurant? The food's pretty howlright.", "So, what's keeping you busy these days?"]

# for m in get_monitors():
#     print(m)

# with mss.mss() as sct:
#     # The screen part to capture
#     monitor = {"top": 456, "left": 798, "width": 325, "height": 17}
#     output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)
#
#     # Grab the data
#     sct_img = sct.grab(monitor)
#
#     # Save to the picture file
#     mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
#     print(output)

image_path = r"sct-456x798_325x17.png"

img = Image.open(image_path)

# Providing the tesseract executable
# location to pytesseract library
pytesseract.tesseract_cmd = path_to_tesseract

# Passing the image object to image_to_string() function
# This function will extract the text from the image
text = pytesseract.image_to_string(img)

# Displaying the extracted text
print(text)

result = process.extractOne(text, all_quotes)
print(result)
