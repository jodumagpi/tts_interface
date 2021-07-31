#!/bin/bash

## a script to install Montreal Forced Aligner (MFA)

root_dir=${1:-/tmp/mfa}
mkdir -p $root_dir
cd $root_dir

# download miniconda3
wget -q --show-progress https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p $root_dir/miniconda3 -f

# create py38 env
$root_dir/miniconda3/bin/conda create -n aligner -c conda-forge openblas python=3.8 openfst pynini ngram baumwelch -y
source $root_dir/miniconda3/bin/activate aligner

mfa thirdparty download

# download and install mfa
source tmp/mfa/miniconda3/bin/activate aligner; mfa align --help

echo -e "\n======== DONE =========="
echo -e "\nMFA Activated!"
echo -e "\nFor more info, see: https://montreal-forced-aligner.readthedocs.io/en/latest/aligning.html to know how to use MFA"