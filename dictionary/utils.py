from multiprocessing import Pool
from tqdm import tqdm

from g2pk import G2p
from jamo import h2j

from glob import glob
import os

g2p = G2p()

def do_multiprocessing(job, tasklist, num_jobs=8):
	p = Pool(num_jobs)
	with tqdm(total=len(tasklist)) as pbar:
		for _ in tqdm(p.imap_unordered(job, tasklist)):
			pbar.update()	

def get_path(*args):
	return os.path.join('', *args)

def create_dir(*args):
        path = get_path(*args)
        if not os.path.exists(path):
                os.mkdir(path)
        return path

def copy_file(source_file, dest_file):
	os.system("cp {} {}".format(source_file, dest_file))

def read_file(source_path):
	with open(source_path, mode="r", encoding="utf-8-sig") as f:
		content = f.readline().rstrip()
	return content

def create_phoneme_dictionary(source_path):
	grapheme_dict, phoneme_dict = {}, {}
	for lab_file in tqdm([x for x in os.listdir(get_path(source_path)) if x.endswith("lab")]):
		sentence = read_file(get_path(source_path, lab_file))
		word_list = sentence.split(" ")
		grapheme_list = h2j(sentence).split(" ")
		phoneme_list = h2j(g2p(sentence)).split(" ")

		for idx, word in enumerate(word_list):
			if not word in grapheme_dict.keys():
				grapheme_dict[word] = " ".join(grapheme_list[idx])

			if not word in phoneme_dict.keys():
				phoneme_dict[word] = " ".join(phoneme_list[idx])

	return grapheme_dict, phoneme_dict

def read_meta(path):
	with open(path, 'r', encoding='utf-8') as f:
		lines = f.readlines()
	return lines

def write_file(savepath, transcript):
	with open(savepath, 'w') as f:
		f.write(transcript)


def write_dictionary(savepath, dictionary):
	"""
		input-dict format
			key: word of transcript delimited by <space> (e.g. 국물이)	
			value: phoneme of hangul-word decomposed into syllables  (e.g. ㄱㅜㅇㅁㅜㄹㅣ)
				=> i.e., input dictionary must define word-phoneme mapping
	"""

	with open(savepath, "w", encoding="utf-8") as f:
		for key in dictionary.keys():
			content = "{}\t{}\n".format(key, dictionary[key])
			f.write(content)


