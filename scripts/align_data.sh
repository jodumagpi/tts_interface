#!/bin/bash

## a script to install Montreal Forced Aligner (MFA) and align data


mkdir -p /tmp/mfa
cd /tmp/mfa

# download miniconda3
wget -q --show-progress https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p /tmp/mfa/miniconda3 -f

# create py38 env
/tmp/mfa/miniconda3/bin/conda create -n aligner -c conda-forge openblas python=3.8 openfst pynini ngram baumwelch -y
# activate env
source /tmp/mfa/miniconda3/bin/activate aligner

# install mfa, download kaldi
pip install montreal-forced-aligner # install requirements
pip install git+https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner.git # install latest updates

mfa thirdparty download

# return to previous directory
cd -

# install sox tool
sudo apt install -q -y sox

# convert to 16k audio clips
mkdir mfa-input
mkdir mfa-input/wav
echo "Normalize audio clips to sample rate of 16k"
find ./data -name "*.wav" -type f -execdir sox --norm=-3 {} -r 16k -c 1 `pwd`/mfa-input/wav/{} \;
echo "Number of clips" $(ls ./mfa-input/wav/ | wc -l)

python aligner/transcripts.py

# align data
mfa train --clean mfa-input/ dict-results/phoneme_dictionary.txt ./mfa-results/ 