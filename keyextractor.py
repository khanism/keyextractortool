import os
import sys
from aeskeyexpansion import schedule_key, print_roundkeys

def print_usage():
    print("Usage: python", sys.argv[0],"\n-keylen <keylength,default=128>\n-file <path to input file>\n-offs <starting offset in file,default=0>\n-v If to output the current offset")


curr_offs = 0
input_file = ""
keylen = 128
verbose = False

if len(sys.argv) < 3:
    print_usage()
    exit()


for i in range(0, len(sys.argv)):
    if sys.argv[i] == "-offs":
        curr_offs = int(sys.argv[i+1])
    elif sys.argv[i] == "-file":
        input_file = sys.argv[i+1]
    elif sys.argv[i] == "-keylen":
        keylen = int(sys.argv[i+1])
    elif sys.argv[i] == "-v":
        verbose = True

#Number of rounds
Nk = keylen//32
Nr = 10 if Nk==4 else 14
#Length of whole key schedule in bytes
kslen = (4*(Nr+1))*4
#Read file
with open(input_file, "rb") as f:
    #Read bytes as hex
    while(True): #TODO: Fix This later on. Should quit, when max possible offset is reached
        try:
            if verbose:
                print("Reading from offset", curr_offs)
            f.seek(curr_offs)
            #Read potential key schedule from file
            ks_str = f.read(kslen).hex()
        except IOError as strerror:
            print("Failed to read bytes from Offset", curr_offs)
            print("I/O error: {0}".format(strerror))
            exit()
        
        
        key_schedule = schedule_key(ks_str[0 : keylen//8*2], keylen)
        key_schedule_calculated_str = ""
        for t in key_schedule:
            for e in t:
                key_schedule_calculated_str += bytes([e]).hex()
        
        #print("Calculated Key schedule str is \n{}\n".format(key_schedule_calculated_str))
        
        #Check if potential key schedule and calculated key schedule match
        if(ks_str == key_schedule_calculated_str):
            print("Found Key at offset", curr_offs)
            print("AES Key:\n" + ks_str[0 : keylen//8*2])
            print("Expaned key:\n" + key_schedule_calculated_str)
            print("\n")
            curr_offs += 1
            #exit()
        else:
            curr_offs += 1

