from PIL import Image
import argparse
from random import randrange

# Parse arguments
argparser = argparse.ArgumentParser(
    description="text + image to image steganography encoder")
argparser.add_argument("-it", "--text", type=str, default=None,
                       help="input text file")
argparser.add_argument("-im", "--image", type=str, default=None,
                       help="input image file")
argparser.add_argument("-o", "--output", type=str, default="output.png",
                       help="output image file")

args = argparser.parse_args()

# Check for sufficient user input
if not args.text:
    print("No input text file")
    exit()
if not args.image:
    print("No input image file")
    exit()

# Open text file
f = open(args.text, "r")
flength = len(f.read())
f.seek(0, 0)


with Image.open(args.image).convert('RGBA') as im:

    # Convert the image data to a list so it can be edited
    imglist = [list(i) for i in im.getdata()]

    for p_index in range(0, min(flength * 3, len(imglist)), 3):

        # Convert character to binary string
        bstring = bin(int.from_bytes(f.read(1).encode(), 'big'))[2:]
        bstring = (8 - len(bstring)) * '0' + bstring

        # Loop through 3 rgb tuples in idata
        for i in range(0,3):
            try:
                # Loop through the three color bands of
                # this pixel and adjust if necessary
                for j, band in enumerate(imglist[p_index + i]):

                    if j + i * 3 >= len(bstring):
                        continue

                    if band % 2 != int(bstring[j + i * 3]):
                        if band == 255:
                            imglist[p_index + i][j] -= 1
                        elif band == 0:
                            imglist[p_index + i][j] += 1
                        else:
                            imglist[p_index + i][j] += randrange(-1, 2, 2)
            except IndexError:
                break

    # Save file
    im2 = Image.new(im.mode, im.size)
    im2.putdata([tuple(i) for i in imglist])
    im2.save(args.output)

