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

import os, numpy
from datetime import datetime

os.chdir('tmp/png/')

frames = [ int(f[:-4]) for f in os.listdir()
    if f.endswith('.png') and f[0] == '1' ]

frames.sort()

time_between_frames = lambda fg: [ p[1] - p[0] for p in zip(fg[:-1], fg[1:]) ]

groups = []
curr_group = []

for time_to_next, frame in zip(time_between_frames(frames), frames[:-1]):

    curr_group.append(frame)

    if time_to_next > 99:

        groups.append(curr_group)
        curr_group = []

groups.append(curr_group)

if time_to_next > 99:

    groups.append([frames[-1]])

else:

    groups[-1].append(frames[-1])

def ut_to_human (ut):

    return datetime.utcfromtimestamp(ut).strftime('%Y-%m-%dT%H:%M:%SZ')

def framestats (fg):

    tbf = time_between_frames(fg)

    return ('  * First capture in group: {} ({})\n'
        + '  * Last capture in group: {} ({})\n'
        + '  * Number of captures in group: {} frames\n'
        + '  * Min time between frames: {} second{}\n'
        + '  * Max time between frames: {} second{}\n'
        + '  * Mean time between frames: {:4.2f} seconds\n'
        + '  * Standard deviation for time between frames: {:4.2f}') \
        .format(
            ut_to_human(fg[0]), fg[0], ut_to_human(fg[-1]), fg[-1], len(fg),
            min(tbf), '' if min(tbf) == 1 else 's',
            max(tbf), '' if max(tbf) == 1 else 's',
            numpy.mean(tbf), numpy.std(tbf))

print('Statistics about the captured frames.\n\nTotal\n')

print(framestats(frames))

print('\n---\n')

print('Grouped such that each group has 99 seconds between captures at most.\n')

for i, group in enumerate(groups):

    if len(group) > 1:

        print('Group #{}\n'.format(i + 1))
        print(framestats(group))

    else:

        print('Single frame at {} ({})'
            .format(ut_to_human(group[0]), group[0]))

    print()
