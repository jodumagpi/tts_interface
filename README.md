## Interface for training and evaluating the Text-to-Speech algorithm. :loud_sound:	

This repository contains the source code for a TTS algorithm based on deep learning models. The algorithm adapts two famous deep learning models, VocGAN and FastSpeech, as vocoder and synthesizer respectively. This code is mainly developed for Korean language only. The instructions for using the code will be described as follows.

- **Clone the repository and install requirements.**
  ```
  git clone https://github.com/jodumagpi/tts_interface.git
  cd tts_interface/
  pip install -r requirements.txt
  ```

- **Prepare the dataset.**\
The dataset must be contained in a folder named `data`. The dataset folder must contain wav files and the corresponding trancript (*.txt) file. The dataset folder must be placed inside the repository folder. The files must be aranged in the manner described below. A small sample data is included in this repository for reference.
  ```
  tts_interface  
        |_ data
            |_ 000.wav
            |_ 001.wav
            |_ transcript.txt
  ```

- **Train the vocoder.**\
When training from scratch, simply run the script for training the vocoder, which also includes data preprocessing steps.
  ```
  bash scripts/train_vocoder.sh
  ```
  When training from a checkpoint, edit the script (line 21) to point to the path of the checkpoint before running the script as described above.
    ```
    python vocoder/trainer.py -c vocoder/config/default.yaml -p /path/to/checkpoint.pt -n exp_name
    ```
  The model weights are saved at the `vocoder-chkpt` folder. Default configurations can be changed by modifying the `vocoder/config/default.yaml` file.

- **Train the synthesizer**\
Training the synthesizer involves 3 steps. 
  1. Generate phoneme dictionary.
      ```
      python dictionary/main.py
      ```
  2. Generate data alignments.
      ```
      bash scripts/align_data.sh
      ```
  3. Train the synthesizer.\
      This code already includes preprocessing. Before running the script, make sure that a trained VocGAN model is in the `synthesizer/vocoder/pretrained_models` folder. When training from scratch, directly run the code below.
      ```
      bash scripts/train_synthesizer.sh
      ```
      However, when training from a checkpoint, make sure that the checkpoint is in the `synthesizer-chkpt/data/` folder then edit the script (line 17) to indicate the latest iteration of the saved model before running the script as described above.
      ```
      python synthesizer/train.py --restore_step 1000 
      ```
      The model weights are saved at the `synthesizer-chkpt` folder. Default configurations can be changed by modifying the `synthesizer/hparams.py` file.
