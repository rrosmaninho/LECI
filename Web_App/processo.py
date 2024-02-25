from PIL import Image
from PIL import ExifTags
import os
import glob

def blackAndWhite(img2):
    im = Image.open(img2)
    width, height = im.size
    new_im = Image.new("L", im.size)
    for x in range(width):
        for y in range(height):
            p = im.getpixel( (x,y) )
            l = int(p[0]*0.299 + p[1]*0.587 + p[2]*0.144)
            new_im.putpixel( (x,y), (l) )
    new_im.save("tmp/blackandwhite.jpg")
    
def borders(image_path):
    border_size=50
    border_color=(255, 0, 255)
    image = Image.open(image_path).convert("RGB")
    width, height = image.size
    border_image = Image.new("RGB", (width + border_size*2, height + border_size*2), border_color)
    border_image.paste(image, (border_size, border_size))
    border_image.save("tmp/borders.jpg")

def sepia(im):
    img = Image.open(im).convert("RGB")
    width, height = img.size
    pixels = img.load()

    for py in range(height):
        for px in range(width):
            r, g, b = img.getpixel((px, py))

            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
            tb = int(0.272 * r + 0.534 * g + 0.131 * b)

            if tr > 255:
                tr = 255

            if tg > 255:
                tg = 255

            if tb > 255:
                tb = 255

            pixels[px, py] = (tr,tg,tb)

    img.save("tmp/sepia.jpg")