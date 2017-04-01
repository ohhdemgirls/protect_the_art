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

from PIL import Image
import os, sys

from palette import palette

if len(sys.argv) != 3:

    sys.stderr.write('Usage: {} <in.png> <out.bin>\n'.format(sys.argv[0]))
    sys.exit(1)

vals = []

with Image.open(sys.argv[1]) as fin:

    if fin.mode != 'RGB':

        fin = fin.convert('RGB')

    pix = fin.load()

    with open(sys.argv[2], 'wb') as fout:

        for y in range(1000):

            for x in range(500):

                pix1 = palette.index(pix[    x * 2, y])
                pix2 = palette.index(pix[x * 2 + 1, y])

                pack = (pix1 << 4) + pix2
                fout.write(pack.to_bytes(1, byteorder='big'))
