
def main():
    lines = open('./data/transcript.txt', 'r').read().splitlines()

    for line in lines:
        fn, transcript = line.split("|")
        f = open("./mfa-input/wav/{}.txt".format(fn), "w")
        f.write(transcript)
        f.close()

if __name__ == "__main__":
    main()