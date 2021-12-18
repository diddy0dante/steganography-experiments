from PIL import Image
import argparse

# Parse arguments.
argparser = argparse.ArgumentParser(
    description="image to text steganography converter")
argparser.add_argument("-i", "--input", type=str, default=None,
                       help="input image file")
argparser.add_argument("-o", "--output", type=str, default=None,
                       help="output text file")

args = argparser.parse_args()

if not args.input:
    print("No input image")
    exit()

# Output string
asciistring = ""

# Process image data and write to asciistring.
with Image.open(args.input).convert('RGB') as im:
    rgblist = list(im.getdata())

    for p_index in range(0, len(rgblist), 3):
        bitstring = "0b"
        for val in rgblist[p_index % len(rgblist)]:
            bitstring += str(val % 2)
        for val in rgblist[((p_index + 1) % len(rgblist))]:
            bitstring += str(val % 2)
        for val in rgblist[((p_index + 2) % len(rgblist))][:-1]:
            bitstring += str(val % 2)
        n = int(bitstring, 2)
        try:
            asciistring += n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()
        except UnicodeDecodeError:
            pass

# Print output to stdout or to the specified file.
if not args.output:
    print(asciistring)
else:
    with open(args.output, "w") as f:
        f.write(asciistring)
