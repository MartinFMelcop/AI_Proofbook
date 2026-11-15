#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
mkdir -p artifacts/video_parts
for part in 1 2 3 4; do
 case "$part" in
 1) file="assets/brand.webp";;
 2) file="assets/ensemble.webp";;
 3) file="assets/presentation.webp";;
 4) file="assets/title.webp";;
 esac
 ffmpeg -nostdin -loglevel error -y -loop 1 -framerate 24 -i "site/$file" \
  -vf "scale=1100:619,zoompan=z='min(1.08,1.0+on*0.0002)':d=1:s=960x540:fps=24,format=yuv420p" \
  -t 4.5 -an -c:v libx264 -preset veryfast -crf 22 \
  "artifacts/video_parts/shot${part}.mp4"
done
printf "" > artifacts/video_parts/list.txt
for part in 1 2 3 4; do printf "file '%s'\n" "shot${part}.mp4" >> artifacts/video_parts/list.txt; done
ffmpeg -nostdin -loglevel error -y -f concat -safe 0 -i artifacts/video_parts/list.txt \
 -i artifacts/opening_original_score.wav -c:v libx264 -preset veryfast -crf 20 \
 -c:a aac -b:a 160k -pix_fmt yuv420p -movflags +faststart \
 -shortest site/assets/opening_animatic.mp4
ffprobe -v error -show_entries format=duration,size -of default=noprint_wrappers=1 site/assets/opening_animatic.mp4
