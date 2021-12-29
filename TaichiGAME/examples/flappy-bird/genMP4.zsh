#!/bin/zsh

ffmpeg -framerate 60 -i ./results/frames/%06d.png -c:v libx264 ./results/out.mp4
