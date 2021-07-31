from dataset import Dataset
from utils import create_dir, get_path

import configs as cfg


def main():

	_ 			  = create_dir(cfg.savedir)
	savedir			  = create_dir(cfg.savedir, cfg.dataset_name)
	savepath		  = create_dir(savedir, "wavs_with_lab")
	savepath_wavs		  = create_dir(savedir, "wavs")
	metadata_savepath	  = get_path(savedir, cfg.metadata_name)
	grapheme_dict_savepath	  = get_path(savedir, cfg.grapheme_dictionary_name)
	phoneme_dict_savepath	  = get_path(savedir, cfg.phoneme_dictionary_name)

	instance = Dataset(
					source_dataset_path = cfg.source_dataset_path,
					savepath = savepath,
					savepath_wavs = savepath_wavs,
					metadata_savepath = metadata_savepath,
					grapheme_dictionary_savepath = grapheme_dict_savepath,
					phoneme_dictionary_savepath = phoneme_dict_savepath,
					num_threads=cfg.NUM_THREADS)

	instance.prepare_mfa_training()


if __name__ == "__main__":
	main()
