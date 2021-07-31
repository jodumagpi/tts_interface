#!/bin/bash

## a script to install Montreal Forced Aligner (MFA)

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

echo -e "\n======== DONE =========="
echo -e "\nMFA Activated!"
echo -e "\nFor more info, see: https://montreal-forced-aligner.readthedocs.io/en/latest/aligning.html to know how to use MFA"