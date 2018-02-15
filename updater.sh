#!/bin/bash
rm -rf websites
rm -rf wget-log
wget --reject '*.js,*.css,*.ico,*.txt,*.gif,*.jpg,*.jpeg,*.png,*.mp3,*.pdf,*.tgz,*.flv,*.avi,*.mpeg,*.iso' --ignore-tags=img,link,script --header="Accept: text/html" -i links.txt -P websites &&
python3 NovelFinderV2.0.py
