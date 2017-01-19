# pyDirBusted
pyDirBusted is a multi-session python utility used to brute-force and enumerate web directories and filenames on web and application servers. This utlitiy attempts to find both visible and hidden files located on a server, and outputs the results both to the screen with the verbose option on and active directories/files may be stored in a file of your choosing. 

## Setup
run `python3 -m pip install -r requirements.txt` to install dependencies

## Usage
After cloning the repo to your system, go into the pyDirBusted directory and run `python3 -m pip install -r requirements.txt`. After dependencies are installed, you can run `./pyDirBusted -h` to view options. This utility requires a wordlist of possible web directories and a URL to start with. 

Syntax is as follows:
`./pyDirBusted -u https://yoursite.com -w wordlists/wordlist.wordlist -o outfile.txt -v`

## Acknowledgements
Thanks to [coldfusion39](https://github.com/coldfusion39) and [zeroSteiner](https://github.com/zerosteiner) for some help and advice with this project. I pulled the wordlists from [here](http://blog.thireus.com/web-common-directories-and-filenames-word-lists-collection/) so they're not all mine. 

## License
pyDirBusted is released under the GNU General Public License. Check it out [here](https://github.com/y4utj4/pyDirBusted/blob/master/LICENSE).