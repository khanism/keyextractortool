# keyextractortool


This is a POC tool to find AES 128/256 Bit Keys in a memory image (but can be abitrary binary file)

Currently works with 128 and 256 Bit keys

Developed with Python 3.7.3


## Usage:
```console
python keyextractor.py -keylen <keylength,default=128> -file <filepath> -offs <starting offset in file,default=0> -v If to output the current offset
```
##