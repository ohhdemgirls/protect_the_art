#!/usr/bin/env bash

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

set -eu

latestpng="$( ls tmp/*.png | grep '^tmp/[0-9]\+\.png' | tail -n2 | head -n1 )"
feh -x $latestpng &
prev_pid=$!

while true ; do
  prevpng=$latestpng
  latestpng="$( ls tmp/*.png | grep '^tmp/[0-9]\+\.png' | tail -n2 | head -n1 )"
  if [ "$prevpng" != "$latestpng" ] ; then
    feh -x $latestpng &
    sleep 1
    kill $prev_pid
    prev_pid=$!
  fi
done
