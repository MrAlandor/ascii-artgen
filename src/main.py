from PIL import Image, ImageDraw, ImageFont, ImageOps

import math

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
# path to the image
im = Image.open("../assets/samples/Beluga.jpg")

# you can set your own font
font = ImageFont.truetype(
    "../assets/fonts/NotoMonoNerdFontMono-Regular.ttf", 13)

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
