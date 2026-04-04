from PIL import Image, ImageDraw, ImageFont, ImageOps
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter

import glob
import math
import os

GRADIENT = ".:coPO?@"

# change and test with different values
SCALE_FACTOR = 0.3

char_width = 8
char_height = 18

gradient_array = list(GRADIENT)
gradient_length = len(gradient_array)
interval = gradient_length / 256


def getGradient(brightness):
    return gradient_array[math.floor(brightness * interval)]


txt_file = open("output.txt", "w")

# samples autocomplete on <Tab>
script_dir = os.path.dirname(__file__)
samples_dir = os.path.join(script_dir, '..', 'assets', 'samples')
samples_dir = os.path.normpath(samples_dir)
images = [os.path.basename(p) for p in sorted(
    glob.glob(os.path.join(samples_dir, '*')))]

images_completer = WordCompleter(images, ignore_case=True)

while True:
    session = PromptSession(completer=images_completer,
                            complete_while_typing=True)
    try:
        image_file = session.prompt(
            "Enter the filename from '/samples' with extension: ")
        im = Image.open(os.path.join(samples_dir, image_file))
        print(f"{image_file} loaded successfully.")
        break
    except FileNotFoundError:
        print("File not found. Please try again.")

# you can set your own font
font = ImageFont.truetype(
    "../assets/fonts/NotoSansMNerdFontMono-CondensedBlack.ttf", 13)

# normalize EXIF orientation
im = ImageOps.exif_transpose(im)

# set width, heigh values; apply resize
width, height = im.size
new_w = max(1, int(SCALE_FACTOR * width))
new_h = max(1, int(SCALE_FACTOR * height * (char_width / char_height)))
im = im.resize((new_w, new_h), resample=Image.NEAREST)
width, height = im.size

im = im.convert("RGB")
pixel = im.load()

# create a new image
output_image = Image.new(
    'RGB', (char_width * width, char_height * height), color=(0, 0, 0))
draw = ImageDraw.Draw(output_image)

for i in range(height):
    for j in range(width):
        r, g, b = pixel[j, i]
        # use luminance for better brightness
        brightness = int(0.2126*r + 0.7152*g + 0.0722*b)
        txt_file.write(getGradient(brightness))
        draw.text((j*char_width, i*char_height),
                  getGradient(brightness), font=font, fill=(r, g, b))

    txt_file.write('\n')

output_image.show()
output_image.save("output.png")
