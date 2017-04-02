#!/usr/bin/env python3

#
# Copyright (c) 2017 Erik Nordstrøm <erik@nordstroem.no>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#

# Hat tip to /u/trosh. https://www.reddit.com/r/place/comments/62mt06/is_someone_taking_a_timelapse_of_the_whole_screen/dfnt5mv/

def decodebin (binf):

    pix = []

    binf.read(4) # skip first 4 bytes which aren't pixels

    for y in range(1000):

        for x in range(500):

            byte = ord(binf.read(1))

            pix1 = byte >> 4
            pix2 = byte & 15

            #pix.append((x, y, pix1))
            pix.append(pix1)
            #pix.append((x, y, pix2))
            pix.append(pix2)

    return pix

if __name__ == '__main__':

    from PIL import Image
    import os, sys

    from palette import palette
    from decodebin import decodebin

    if len(sys.argv) != 3:

        sys.stderr.write('Usage: {} <in.bin> <out.png>\n'.format(sys.argv[0]))
        sys.exit(1)

    img = Image.new('RGB', (1000, 1000))
    pix = img.load()

    with open(sys.argv[1], 'rb') as binf:

        decoded = decodebin(binf)

        for y in range(1000):

            for x in range(1000):

                pix[x, y] = palette[decoded[y * 1000 + x]]

    img.save(sys.argv[2])
