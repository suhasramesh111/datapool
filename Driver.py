#Importing the KWIC module
import time
from KWIC import master
from IPython import get_ipython


#clear the old outputs
# def clear_console():
#     get_ipython().magic('clear')

#Creating the master object
KWIC = master()

#Reading lines
with open("Dataset_KWIC.txt", "r") as f:
    sentences = f.readlines()

#Processing one line at a time
for sentence in sentences:
    #clear_console()
    sentence = sentence.strip("\n").lower()
    KWIC.process_line(sentence)
    
    time.sleep(2)

    
