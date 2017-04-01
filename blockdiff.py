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

import os, sys, math

from palette import palette

if len(sys.argv) != 4:

    sys.stderr.write("Usage: {} <basis_in.bin> <desired_in.bin> <worklist_out.txt>\n".format(sys.argv[0]))
    sys.exit(1)

basis = []
desired = []

#workviz = Image.new('RGB', (1000, 1000), "white")
#wpix = workviz.load()

def blockid_next (blockid):

    incr = 16

    if blockid[2] < 255:

        return (blockid[0], blockid[1], blockid[2] + incr)

    elif blockid[1] < 255:

        return (blockid[0], blockid[1] + incr, 0)

    elif blockid[0] < 255:

        return (blockid[0] + incr, 0, 0)

    else: # (255, 255, 255)

        return (0, 0, 0)

def diffblock (c, r, blockid):

    blockwork = []

    for j in range(r * 13, (r + 1) * 13):

        for i in range(c * 13, (c + 1) * 13):

            if (i == 1000) or (j == 1000):

                break

            k = i + 1000 * j

            if desired[k] == 3: # For now we skip bg pixels to save time

                continue

            if desired[k] != basis[k]:

                blockwork.append((i, j, desired[k]))
                #wpix[i, j] = blockid

    return blockwork

def readbin (binf):

    pix = []

    binf.read(4) # skip first 4 bytes which aren't pixels

    for y in range(1000):

        for x in range(500):

            byte = ord(binf.read(1))

            pix1 = byte >> 4
            pix2 = byte & 15

            pix.append(pix1)
            pix.append(pix2)

    return pix

with open(sys.argv[1], 'rb') as basisf:

    basis = readbin(basisf)

with open(sys.argv[2], 'rb') as desiredf:

    desired = readbin(desiredf)

worklist = []

blockid = (0, 0, 0)

for r in range(math.ceil(1000 / 13)):

    for c in range(math.ceil(1000 / 13)):

        worklist.append(diffblock(c, r, blockid))

        blockid = blockid_next(blockid)

sys.stderr.write("Number of pixels that need to be changed: {}\n".format(sum(map(len, worklist))))

with open(sys.argv[3], 'w') as worklistf:

    for block in worklist:

        for x, y, color in block:

            worklistf.write("{} {} {}\n".format(x, y, color))

#workviz.save(sys.argv[4])
