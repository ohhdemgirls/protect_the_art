#!/usr/bin/env bash

ffmpeg -f concat -r 60 -i tmp/animation_frames.txt \
  -vcodec libx264 -crf 25 -pix_fmt yuv420p tmp/animation.mp4
