# stenography-experiments

This is a proprietary stenography encoder and decoder. To read an encoded image, each character is read from 3 consecutive pixels, with each red, green and blue value representing a 1 or 0, being if it is odd or if it is even, respectively. The blue of every third pixel is ignored. So every 8 of these bits represents one utf-8 character. Pixels can only be discolored by 1/256th, so it is fairly indistinguishable to the human eye.

Both the encoder and decoder have a worst case time complexity of O(n) where n is the amount of pixels in the file.

## Usage

To use the stenography encoder execute encoder.py with a python interpreter, and use commandline arguments `-it`, `-im` and `-o`. `-it` is followed by the path of your input text file, `-im` is followed by the path of the payload image, and `-o` is followed by the path of the new file. You can call it anything with a filename extension recognized by Python Imaging Library, but don't use lossy formats like jpeg! Lossy formats will lose the data you just encoded into the file. If the `-o` argument is not used, the program will default to "output.png". Here are examples of usage:

    python3.9 encoder.py -it inputtext.txt -im pikachu.png -o secret_pikachu.png

To use the decoder, run the decoder.py program with the `-i` and `-o` arguments. `-i` is followed by the path of the image to be decoded, and `-o` is followed by the name of the output text file. It is possible to run the program without `-o` flag at all, it will then send the output to `stdout`. I highly recommend not sending the output to the shell, because all image data is printed, not just the encrypted contents, the program will most likely print so many lines that you can't scroll up to see the encrypted text. It can however be useful to do this if you wish to pipe the output directly to a different program. It is also possible to directly send the output to a file with `>`, if you prefer to do it that way.

    python3.9 decoder.py -i FGzJ3RcakAIXefG.png -o secret_code.txt

identical to:

    python3.9 decoder.py -i FGzJ3RcakAIXefG.png > secret_code.txt
