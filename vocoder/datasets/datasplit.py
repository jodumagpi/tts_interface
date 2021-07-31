# split to train and val
import os
import random
from shutil import copyfile

def split():
    os.mkdir("data/vocoder")
    os.mkdir("data/vocoder/train")
    os.mkdir("data/vocoder/valid")

    wavs = sorted([x for x in os.listdir("./data") if x.endswith(".wav")])
    random.seed(55)
    random.shuffle(wavs)
    train, val = wavs[:int(len(wavs)*0.8)], wavs[int(len(wavs)*0.8):]
    for t in train:
        copyfile("data/"+t, "data/vocoder/train/"+t)
    for v in val:
        copyfile("data/"+v, "data/vocoder/valid/"+v)

if __name__ == "__main__":
    split()