import torch
import torch.nn as nn
import numpy as np
import hparams as hp
import os

import argparse
import re
from string import punctuation

from fastspeech2 import FastSpeech2
from vocoder import vocgan_generator

from text import text_to_sequence, sequence_to_text
import utils
import audio as Audio

import codecs
from g2pk import G2p
from jamo import h2j

from scipy.io import wavfile

import noisereduce as nr

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def cut(signal):
    for i in range(len(signal)):
        if np.abs(signal[i]) > 500:
            return i

def split(sentence):

    remove = ["“", "”", "‘", "’", "\'", "\"", "}", ")", "]"]
    space = ["(", "{", "["]
    replace = ["·"]
    topic = ["는", "은"]
    obj = ["를", "을"]
    subject = ["이", "가"]
    location = ["에", "서"]
    thru = ["로"]
    conj = ["고", "과", "와"]
    extra = ["인", "면", "한", "해", "우", "최", "된", "대"]
    pause = topic + obj + subject + location + thru + conj + extra

    chars = [x for x in sentence]
    new_sentence = []

    for e, c in enumerate(chars):
        if c in remove:
            continue # ignore
        elif c in space: # replace brackets w spaces
            new_sentence.append(" ")
        elif c in replace: # some specific punctuation
            new_sentence.append(", ")
        #elif c in pause and chars[e+1] == " " and not e == 0: # if word ends like
        #    new_sentence.append(c+";")
        else:
            new_sentence.append(c)
    
    new_sentence = "".join(new_sentence)
    #print("Processed sentence:")
    #print(new_sentence)
    lst = new_sentence.split(" ")
    splits = [" ".join(lst[i:i + 3]) for i in range(0, len(lst), 3)]
    if len(splits[-1].split(" ")) == 1 and len(splits) > 1:
        splits[-2] += splits[-1]
        del splits[-1]
    return splits

def kor_preprocess(text):
    text = text.rstrip(punctuation)
    
    g2p=G2p()
    phone = g2p(text)
    phone = h2j(phone)
    phone = list(filter(lambda p: p != ' ', phone))
    phone = '{' + '}{'.join(phone) + '}'
    phone = re.sub(r'\{[^\w\s]?\}', '{sp}', phone)
    phone = phone.replace('}{', ' ')

    sequence = np.array(text_to_sequence(phone,hp.text_cleaners))
    sequence = np.stack([sequence])
    return torch.from_numpy(sequence).long().to(device)


def get_FastSpeech2():
    checkpoint_path = os.path.join(hp.checkpoint_path, "fastspeech.pth.tar")
    model = nn.DataParallel(FastSpeech2())
    model.load_state_dict(torch.load(checkpoint_path, map_location=device)['model'])
    model.requires_grad = False
    model.eval()
    return model

def synthesize(model, vocoder, text, sentence, prefix=''):

    mean_mel, std_mel = torch.tensor(np.load(os.path.join(hp.preprocessed_path, "mel_stat.npy")), dtype=torch.float).to(device)
    mean_f0, std_f0 = torch.tensor(np.load(os.path.join(hp.preprocessed_path, "f0_stat.npy")), dtype=torch.float).to(device)
    mean_energy, std_energy = torch.tensor(np.load(os.path.join(hp.preprocessed_path, "energy_stat.npy")), dtype=torch.float).to(device)

    mean_mel, std_mel = mean_mel.reshape(1, -1), std_mel.reshape(1, -1)
    mean_f0, std_f0 = mean_f0.reshape(1, -1), std_f0.reshape(1, -1)
    mean_energy, std_energy = mean_energy.reshape(1, -1), std_energy.reshape(1, -1)

    src_len = torch.from_numpy(np.array([text.shape[1]])).to(device)
        
    mel, mel_postnet, log_duration_output, f0_output, energy_output, _, _, mel_len = model(text, src_len)
    
    mel_torch = mel.transpose(1, 2).detach()
    mel_postnet_torch = mel_postnet.transpose(1, 2).detach()
    f0_output = f0_output[0]
    energy_output = energy_output[0]

    mel_torch = utils.de_norm(mel_torch.transpose(1, 2), mean_mel, std_mel)
    mel_postnet_torch = utils.de_norm(mel_postnet_torch.transpose(1, 2), mean_mel, std_mel).transpose(1, 2)
    f0_output = utils.de_norm(f0_output, mean_f0, std_f0).squeeze().detach().cpu().numpy()
    energy_output = utils.de_norm(energy_output, mean_energy, std_energy).squeeze().detach().cpu().numpy()

    return utils.vocgan_infer(mel_postnet_torch, vocoder, path=os.path.join(""))

if __name__ == "__main__":
    
	model = get_FastSpeech2().to(device)
	vocoder = utils.get_vocgan(ckpt_path=hp.vocoder_pretrained_model_path)
	
	g2p=G2p()
	
	print('input sentence')
	sentence = input()
	
	print('sentence that will be synthesized: ')
	print(sentence)
	
	sentence = split(sentence)
	splits = []
	for e, s in enumerate(sentence):   
		text = kor_preprocess(s)
		res = synthesize(model, vocoder, text, sentence)
		idx = cut(res)
		splits.append(res[idx:])
	audio = np.hstack(splits)
	audio = nr.reduce_noise(audio, hp.sampling_rate)
	wavfile.write("result.wav", hp.sampling_rate, audio)
