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

import sys, requests, json, time

with open('created.txt', 'r') as usrpass:

    with open('tmp/cookies.txt', 'w') as cookies:

        for uline in usrpass:

            usr, pwd = [v for v in uline.strip().split('\t') if v]

            status = 0
            attempts = 0

            while status != 200 and attempts < 30:

                attempts += 1

                r = requests.post('https://www.reddit.com/api/login', data={ 'user': usr, 'passwd': pwd, 'api_type': 'json' })
                status = r.status_code

                sys.stderr.write('.')
                sys.stderr.flush()

                time.sleep(2)

            sys.stderr.write('{}\n'.format(status))

            if status == 200:

                cookie = json.loads(r.text)['json']['data']['cookie']
                #print(cookie)

                cookies.write('{}\n'.format(cookie))
