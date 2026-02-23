#!/bin/bash

# Convert all MP3 files to WAV (44.1 kHz) recursively
find . -type f -iname "*.mp3" | while read -r file; do
    out="${file%.*}.wav"
    echo "Converting: $file → $out"
    ffmpeg -y -i "$file" -ar 44100 "$out"
done

read -p "Press Enter to continue..."

backup_dir="./gomi"
mkdir -p "$backup_dir"
find . -type f -iname "*.mp3" | while read -r file; do
    echo "Moving: $file → $backup_dir"
    mv "$file" "$backup_dir/"
done
