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

# Resamples captures to 1 frame per n seconds.

n = 60

import sys
from statistics import *

anim_frames = []

for duration, frame in zip(time_between_frames(frames), frames[:-1]):

    anim_frames += [frame] * duration

anim_frames = anim_frames[0::(n - 1)]

repeats = []
curr_repeat = []

with open('../animation_frames.txt', 'w') as af:

    for anim_frame in anim_frames:

        if len(curr_repeat) and anim_frame != curr_repeat[-1]:

            repeats.append(curr_repeat)

            curr_repeat = []

        curr_repeat.append(anim_frame)

        af.write("file 'png/" + str(anim_frame) + ".png'\n")

repeats.append(curr_repeat)

repeat_counts = [ len(g) for g in repeats ]

#sys.stderr.write(str(repeat_counts) + '\n')

sys.stderr.write('Longest repeat: {}\n'.format(max(repeat_counts)))

sys.stderr.write('Unique frames: {}\n'.format(len(repeat_counts)))

sys.stderr.write('Total number of frames: {}\n'.format(len(anim_frames)))

import matplotlib.pyplot as plt

plt.bar([r[0] for r in repeats], repeat_counts)

plt.title('Repeat counts for individual captures')
plt.xlabel('capture id')
plt.ylabel('number of repeats')

plt.savefig('../repeat_frames.png')
