# (DOES NOT) WORK IN PROGRESS
from PIL import Image
import argparse
from random import randrange

# Parse arguments.
argparser = argparse.ArgumentParser(
    description="text + image to image steganography encoder")
argparser.add_argument("-it", "--text", type=str, default=None,
                       help="input text file")
argparser.add_argument("-im", "--image", type=str, default=None,
                       help="input image file")
argparser.add_argument("-o", "--output", type=str, default="output.png",
                       help="output image file")

args = argparser.parse_args()

if not args.text:
    print("No input text file")
    exit()
if not args.image:
    print("No input image file")
    exit()

f = open(args.text, "r")
flength = len(f.read())
f.seek(0, 0)


with Image.open(args.image).convert('RGB') as im:

    im2 = Image.new(im.mode, im.size)
    olddata = list(im.getdata())      # Contains the original image data
    newdata = []                    # Contains the new data to put in the image

    for p_index in range(0, len(olddata), 3):

        # Convert character to binary string
        bstring = bin(int.from_bytes(f.read(1).encode(), 'big'))[2:]

        # Loop through 3 rgb tuples in idata
        for i in range(0,3):

            # Will be converted to a tuple with the RGB values of one pixel
            new_rgb = []

            try:
                # Loop through the three color bands of this pixel
                for j, band in enumerate(olddata[p_index + i]):
                    if j + i * 3 >= len(bstring):
                        new_rgb.append(olddata[p_index + i][j])
                        continue
                    if band != int(bstring[j + i * 3]):
                        if band == 255:
                            new_rgb.append(olddata[p_index + i][j] - 1)
                        if band == 0:
                            new_rgb.append(olddata[p_index + i][j] + 1)
                        else:
                            new_rgb.append(olddata[p_index + i][j]
                            + randrange(-1, 2, 2))
            except IndexError:
                break

            # Append a tuple with this pixel's rgb values to the list
            newdata.append(tuple(new_rgb))

    # Save file
    im2.putdata(newdata)
    im2.save(args.output)

