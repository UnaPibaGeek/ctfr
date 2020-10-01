# CTFR
Do you miss AXFR technique? This tool allows to get the subdomains from a HTTP**S** website in a few seconds.  
How it works? CTFR does not use neither dictionary attack nor brute-force, it just abuses of Certificate Transparency logs.  
For more information about CT logs, check www.certificate-transparency.org and [crt.sh](https://crt.sh/).

## GETTING STARTED
Please, follow the instructions below for installing and run CTFR.

### PRE-REQUISITIES
Make sure you have installed the following tools:
```
Python 3.0 or later.
pip3 (sudo apt-get install python3-pip).
```

### INSTALLING
```bash
$ git clone https://github.com/UnaPibaGeek/ctfr.git
$ cd ctfr
$ pip3 install -r requirements.txt
```

### RUNNING
```bash
$ python3 ctfr.py --help
```


## USAGE
Parameters and examples of use.

### PARAMETERS
```
-d --domain [target_domain] (required)
-o --output [output_file] (optional)
```

### EXAMPLES
```bash
$ python3 ctfr.py -d starbucks.com
```
```bash
$ python3 ctfr.py -d facebook.com -o /home/shei/subdomains_fb.txt
```

### WITH DOCKERS
I think it's a little bit crazy to use Docker for running such a little python script, but if you want to do it anyway, you can use [this Docker image](https://hub.docker.com/r/unapibageek/ctfr).

The instructions are there.

## SCREENSHOTS
<p align="center">
  <img src="https://www.semecayounexploit.com/CTFR/CTFR-ST.png" />
</p>

<p align="center">
  <img src="https://www.semecayounexploit.com/CTFR/CTFR-FB.png" />
</p>


## AUTHOR
* *Sheila A. Berta - [(@UnaPibaGeek)](https://www.twitter.com/UnaPibaGeek).*
