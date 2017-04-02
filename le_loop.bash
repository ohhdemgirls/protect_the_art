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

./auth.py

while true ; do

  false

  while [ $? -ne 0 ] ; do
    ./blockdiff.bash
  done

  # For now we just take the greatest amount of seconds to wait
  now_sleep="$( ./paint.bash | jq .wait_seconds | sort | tail -n1 | cut -d'.' -f1 )"
  echo "Now sleep $now_sleep seconds" 1>&2

  if ! [[ $now_sleep =~ ^[0-9]+$ ]] ; then
    echo default sleep 1>&2
    now_sleep=300
  fi

  sleep $now_sleep
done
