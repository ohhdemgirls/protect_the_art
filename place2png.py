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

from PIL import Image
import os, sys

from palette import palette

if len(sys.argv) != 3:

    sys.stderr.write('Usage: {} <in.bin> <out.png>\n'.format(sys.argv[0]))
    sys.exit(1)

img = Image.new('RGB', (1000, 1000))
pix = img.load()

with open(sys.argv[1], 'rb') as fin:

    for y in range(1000):

        for x in range(500):

            byte = ord(fin.read(1))

            pix1 = byte >> 4
            pix2 = byte & 15

            pix[    x * 2, y] = palette[pix1]
            pix[x * 2 + 1, y] = palette[pix2]

img.save(sys.argv[2])
