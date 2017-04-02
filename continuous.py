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

from time import time, sleep
import os, sys, requests, mmap, shutil, json

from config import *

from decodebin import decodebin

canvas = { 'file': None, 'expire': 0, 'subset': None }

start_x = 0
start_y = 0
end_x = 999
end_y = 999
artworkfn = None

prognam = sys.argv[0]

if len(sys.argv) == 2:

    artworkfn = sys.argv[1]

elif len(sys.argv) == 6:

    start_x = int(sys.argv[1])
    start_y = int(sys.argv[2])
    end_x = int(sys.argv[3])
    end_y = int(sys.argv[4])
    artworkfn = sys.argv[5]

else:

    sys.stderr.write('Usage: {} [<start_x> <start_y> <end_x> <end_y>] <artwork.bin>\n'.format(prognam))
    sys.exit(1)

if (0 > start_x) or (start_x > end_x):

    sys.stderr.write("{}: ERROR: Need to have 0 <= start_x <= end_x. "
        .format(prognam))

    sys.stderr.write("You provided `{}' for start_x".format(start_x))
    if start_x >= end_x:
        sys.stderr.write(" and `{}' for end_x".format(end_x))
    sys.stderr.write(".\n")

    sys.exit(1)

if (0 > start_y) or (start_y > end_y):

    sys.stderr.write("{}: ERROR: Need to have 0 <= start_y <= end_y. "
        .format(prognam))

    sys.stderr.write("You provided `{}' for start_y".format(start_y))
    if start_y >= end_y:
        sys.stderr.write(" and `{}' for end_y".format(end_y))
    sys.stderr.write(".\n")

    sys.exit(1)

subset_width = end_x + 1 - start_x
subset_height = end_y + 1 - start_y

scanband_nominal_height_px = min(subset_height, scanband_nominal_height_px)

accounts = []

now = lambda: int(time())

with open('tmp/cookies.txt', 'r') as cookiesf:

    for cookiel in cookiesf:

        cookie = cookiel.strip()

        s = requests.Session()

        account = { 'cookie': cookiel.strip(), 'can_use_after': now(), 's': s }

        accounts.append(account)

def get_data_subset (data):

    subset = [[None for i in range(subset_width)] for j in range(subset_height)]

    j = 0

    for y in range(start_y, end_y + 1):

        i = 0

        for x in range(start_x, end_x + 1):

            subset[j][i] = data[y * 1000 + x] #[2]

            i += 1

        j += 1

    return subset

def get_canvas ():

    called = now()
    expire = called + canvas_refresh_interval_seconds

    new_canvas = { 'file': None, 'expire': 0, 'subset': None }

    new_canvas['file'] = os.path.join('remote', str(called) + '.bin')
    new_canvas['expire'] = expire

    r = requests.get('https://www.reddit.com/api/place/board-bitmap',
        stream=True)

    if r.status_code == 200:

        partfn = new_canvas['file'] + '.part'

        try:

            with open(partfn, 'ab+') as dlf:

                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, dlf)

                dlf.seek(0)

                new_canvas['subset'] = get_data_subset(decodebin(dlf))

        except:

            if os.path.isfile(partfn):

                os.remove(partfn)

            raise

        os.rename(partfn, new_canvas['file'])

        return new_canvas

    return None

canvas = get_canvas()

artwork_subset = None

with open(artworkfn, 'rb') as artworkf:

    artwork_subset = get_data_subset(decodebin(artworkf))

def update_position_state (scanband):

    scanband['pos'] += 1

    if (scanband['pos'] == scanband['height']):

        scanband['pos'] = 0
        scanband['x'] += 1

    if (scanband['x'] == subset_width):

        scanband['x'] = 0
        scanband['y'] += scanband_nominal_height_px

    if (scanband['y'] >= subset_height):

        scanband['y'] = 0
        scanband['height'] = scanband_nominal_height_px

    if (scanband['y'] + scanband['height'] > subset_height):

        scanband['height'] = subset_height - scanband['y'] + 1

scanband = { 'x': 0, 'y': 0, 'height': scanband_nominal_height_px, 'pos': 0 }

while True:

    if canvas['expire'] <= now():

        sys.stderr.write('/')
        sys.stderr.flush()

        new_canvas = None

        try:

            new_canvas = get_canvas()

        except KeyboardInterrupt:

            raise

        except:

            pass

        if new_canvas is None:

            sys.stderr.write('Reusing cached canvas {}.\n'
                .format(canvas['file']))

            canvas['expire'] = canvas['expire'] + default_expiration_secs

        else:

            canvas = new_canvas

        sleep(2)

    account = accounts[0]
    accounts = accounts[1:]

    if account['can_use_after'] <= now():

        account['can_use_after'] = now() + default_expiration_secs

        sys.stderr.write(':')

        for k in range(subset_width * subset_height):

            x, y = scanband['x'], scanband['y'] + scanband['pos']

            if (canvas['subset'][y][x] == artwork_subset[y][x]):

                sys.stderr.write('-')
                sys.stderr.flush()

                update_position_state(scanband)

            else:

                sys.stderr.write('({}, {})'.format(x, y))
                sys.stderr.flush()

                break

        x, y = scanband['x'], scanband['y'] + scanband['pos']

        try:

            r = account['s'].get('https://www.reddit.com/r/place.json', headers={'User-Agent': ua, 'Cookie': 'reddit_session=' + account['cookie']})
            sleep(2)

            sys.stderr.write(' ' + str(r.status_code))

            modhash = json.loads(r.text)['data']['modhash']

            paint = { 'x': x + start_x , 'y': y + start_y , 'color': artwork_subset[y][x] }

            sys.stderr.write(' ' + str(paint))
            sys.stderr.flush()

            r = account['s'].post('https://www.reddit.com/api/place/draw.json', data=paint, headers={'User-Agent': ua, 'Cookie': 'reddit_session=' + account['cookie'], 'X-Modhash': modhash})
            sleep(2)

            sys.stderr.write(' ' + str(r.status_code))

            if r.status_code == 200:

                update_position_state(scanband)

            else:

                sys.stderr.write(' ' + r.text)

            sys.stderr.flush()

            wait = int(json.loads(r.text)['wait_seconds']) + 1
            account['can_use_after'] = wait + now()

            sys.stderr.write(',' + str(wait))
            sys.stderr.flush()

        except KeyboardInterrupt:

            raise

        except:

            sys.stderr.write('\n' + str(sys.exc_info()[1]) + '\n')

        sleep(2)

    accounts.append(account)

    sys.stderr.flush()
