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

ua = 'Mr. Fourchan'

import os, sys, requests, json

with open('tmp/cookies.txt', 'r') as cookies:

    with open(sys.argv[1], 'r') as worklist:

        for cookiel in cookies:

            cookie = cookiel.strip()

            x, y, color = worklist.readline().strip().split(' ')


            paint = {
                'x': x,
                'y': y,
                'color': color
            }

            r = requests.get('https://www.reddit.com/r/place.json', headers={'User-Agent': ua, 'Cookie': 'reddit_session=' + cookie})
            sys.stderr.write('{}\n'.format(r.status_code))
            modhash = json.loads(r.text)['data']['modhash']

            #print(modhash)

            #sys.exit(0)

            r = requests.post('https://www.reddit.com/api/place/draw.json', data=paint, headers={'User-Agent': ua, 'Cookie': 'reddit_session=' + cookie, 'X-Modhash': modhash})

            sys.stderr.write('{}\n'.format(r.status_code))
            print(r.text)
