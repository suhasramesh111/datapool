import time
from KWIC import master

KWIC = master()

with open("Dataset_KWIC.txt", "r") as f:
    sentences = f.readlines()


for sentence in sentences:
    sentence = sentence.strip("\n").lower()
    KWIC.process_line(sentence)
    KWIC.output.print_all_KWIC()
    time.sleep(2)
    print("\n"*5)
