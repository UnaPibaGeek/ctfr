# CTFR
Do you miss AXFR technique? This tool allows to get the subdomains from a HTTP**S** website in a few seconds.  
How it works? CTFR does not use neither dictionary attack nor brute-force, it just abuses of Certificate Transparency logs. 
Additional domains are grabbed from the `Names` field of the record stored at [censys.io](https://censys.io).
For more information about CT logs, check www.certificate-transparency.org and [crt.sh](https://crt.sh/).

## Getting Started
Please, follow the instructions below for installing and run CTFR.

### Pre-requisites
Make sure you have installed the following tools:
```
Python 3.0 or later.
pip3 (sudo apt-get install python3-pip).
```

### Installing
```bash
$ git clone https://github.com/UnaPibaGeek/ctfr.git
$ cd ctfr
$ pip3 install -r requirements.txt
```
If you want to also search for additional domains from censys.io, you also need to install BeautifulSoup4:
```bash
$ pip3 install beautifulsoup4
```
This was left out of the requirements.txt file so you weren't forced to install it.

### Running
```bash
$ python3 ctfr.py --help
```


## Usage
Parameters and examples of use.

### Parameters
```
-d --domain [target_domain] (required)
-o --output [output_file] (optional)
-a --alt (optional, single switch)
```

### Examples
```bash
$ python3 ctfr.py -d starbucks.com
```
```bash
$ python3 ctfr.py -d facebook.com -o /home/shei/subdomains_fb.txt
```
```bash
$ python3 ctfr.py -d facebook.com -a -o /home/shei/subdomains_fb.txt
```

### With Docker
I think it's a little bit crazy to use Docker for running such a little python script, but if you want to do it anyway, you can download [this lightweight (97.8MB) Docker image](https://hub.docker.com/r/johnpaulada/ctfr/) made by John Paulada.

The instructions are there.

## Screenshots
<p align="center">
  <img src="https://www.semecayounexploit.com/CTFR/CTFR-ST.png" />
</p>

<p align="center">
  <img src="https://www.semecayounexploit.com/CTFR/CTFR-FB.png" />
</p>


## Author
* *Sheila A. Berta - [(@UnaPibaGeek)](https://www.twitter.com/UnaPibaGeek).*
