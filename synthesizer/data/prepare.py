## delete unaligned data
import random, os
from shutil import copyfile

def main():

    # prep data folder
    if not os.path.exists("data/synthesizer"):
        os.mkdir("data/synthesizer")
        os.mkdir("data/synthesizer/wavs")

    # read unaligned data
    unaligned = open("mfa-results/unaligned.txt").read().splitlines()
    unaligned_files = []
    for x in unaligned:
        unaligned_files.append("_".join(x.split("\t")[0].split("-")[1:]))
        
    print("Total of {} unaligned files.".format(len(unaligned_files)))

    # only copy aligned data
    for x in [y for y in os.listdir("data") if y.endswith("wav")]:
        if not x[:-4] in unaligned_files: # aligned
            copyfile(os.path.join("data", x), os.path.join("data/synthesizer/wavs", x))

    print("Total training data (aligned): {}".format(len([x for x in os.listdir("data/synthesizer/wavs") if x.endswith("wav")])))

    # replace transcript
    transcript = open("data/transcript.txt").read().splitlines() # read old transcript
    aligned_transcript = open("data/synthesizer/transcript.txt", "w") # write new transcript
    for t in transcript:
        if t.split("|")[0] not in unaligned_files:
            aligned_transcript.write(t+"\n")
    aligned_transcript.close()

    # rename TextGrids
    for t in [x for x in os.listdir("mfa-results/wav/") if x.endswith("TextGrid")]:
        t_rename = "_".join(t.split("-")[1:])
        os.rename("mfa-results/wav/"+t, "mfa-results/wav/"+t_rename)

    print("Total TextGrids: {}".format(len([x for x in os.listdir("mfa-results/wav") if x.endswith("TextGrid")])))

if __name__ == "__main__":
    main()