#!/bin/bash

## a script to train the synthesizer

sudo apt install -q -y ffmpeg
sudo apt-get install -q -y zip unzip

python synthesizer/data/prepare.py
cd mfa-results/wav
zip -qr TextGrid.zip *
cd -
mv mfa-results/wav/TextGrid.zip synthesizer

mkdir synthesizer/vocoder/pretrained_models/
mkdir synthesizer-chkpt
mkdir synthesizer-chkpt/data

python synthesizer/preprocess.py
python synthesizer/train.py
##python synthesizer/train.py --restore_step 980000 # continue from checkpoint