# CTFR
Do you miss AXFR technique? This tool allows to get the subdomains from a HTTP**S** website in a few seconds.  
How it works? CTFR does not use neither dictionary attack nor brute-force, it just abuses of Certificate Transparency logs.  
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

### Installing with OTinstaller
On Linux, [OTinstaller](https://github.com/OSINTVerseHQ/OTinstaller) is a third-party tool manager that clones this repository and installs CTFR into its own virtualenv. It isn't maintained by the CTFR author, so please report problems with it [on the OTinstaller tracker](https://github.com/OSINTVerseHQ/OTinstaller/issues).

```bash
$ pipx install otinstaller
$ otinstaller init
$ otinstaller install ctfr
$ otinstaller run ctfr -- -d starbucks.com   # same as python3 ctfr.py -d starbucks.com
```

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
```

### Examples
```bash
$ python3 ctfr.py -d starbucks.com
```
```bash
$ python3 ctfr.py -d facebook.com -o /home/shei/subdomains_fb.txt
```

### With Docker
I think it's a little bit crazy to use Docker for running such a little python script, but if you want to do it anyway, you can use [this Docker image](https://hub.docker.com/r/unapibageek/ctfr).

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
