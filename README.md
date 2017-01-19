# pyDirBusted
pyDirBusted is a python utility used to brute-force and enumerate web directories within a site. 

## Setup
run 'python3 -m pip install -r requirements.txt' to install dependencies



## Usage
After cloning the repo to your system, go into the pyDirBusted directory and run 'python3 -m pip install -r requirements.txt'. After dependencies are installed, you can run './pyDirBusted -h' to view options. This utility requires a wordlist of possible web directories and a URL to start with. 

Syntax is as follows:
'./pyDirBusted -u https://yoursite.com -w wordlists/wordlist.wordlist -o outfile.txt -v'

## Acknowledgements
Thanks to [coldfusion39](https://github.com/coldfusion39) and [zeroSteiner](https://github.com/zerosteiner) for some help and advice with this project. I pulled the wordlists from [here](http://blog.thireus.com/web-common-directories-and-filenames-word-lists-collection/) so they're not all mine. 

