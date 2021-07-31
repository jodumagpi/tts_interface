# install sox tool
#sudo apt install -q -y sox

# convert to 16k audio clips
mkdir mfa-input
mkdir mfa-input/wav
echo "Normalize audio clips to sample rate of 16k"
find ./data -name "*.wav" -type f -execdir sox --norm=-3 {} -r 16k -c 1 `pwd`/mfa-input/wav/{} \;
echo "Number of clips" $(ls ./mfa-input/wav/ | wc -l)

python aligner/transcripts.py

# align data
source /tmp/mfa/miniconda3/bin/activate aligner
mfa train --clean mfa-input/ dict-results/phoneme_dictionary.txt ./mfa-results/ 