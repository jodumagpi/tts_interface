#!/bin/bash

## a script to train the vocoder

python vocoder/datasets/datasplit.py

sudo apt install -q -y sox
mkdir ./temp
echo "normalize audio training clips to sample rate of 22050"
find ./data/vocoder/train -name "*.wav" -type f -execdir sox --norm=-3 {} -r 22050 -c 1 `pwd`/temp/{} \;
echo "Number of clips" $(ls ./temp/ | wc -l)
mv ./temp/* ./data/vocoder/train
echo "normalize audio validation clips to sample rate of 22050"
find ./data/vocoder/valid -name "*.wav" -type f -execdir sox --norm=-3 {} -r 22050 -c 1 `pwd`/temp/{} \;
echo "Number of clips" $(ls ./temp/ | wc -l)
mv ./temp/* ./data/vocoder/valid
rm -rf ./temp

python vocoder/preprocess.py -c vocoder/config/default.yaml -d data/vocoder

python vocoder/trainer.py -c vocoder/config/default.yaml -n exp