# CTFR
Do you miss AXFR technique? This tool allows to get the subdomains from a HTTP**S** website in a few seconds.  
How it works? CTFR does not use neither dictionary attack nor brute-force, it just abuses of Certificate Transparency logs.  
For more information about CT logs, check www.certificate-transparency.org.

## Getting Started
Please, follow the instructions below for installing and run CTFR.

### Pre-requisites
Make sure you have installed the following tools:
```
Python 3.0 or later.
pip3 (sudo apt-get install python3-pip).
```

### Installing
```
git clone https://github.com/UnaPibaGeek/ctfr.git
cd ctfr
pip3 install -r requirements.txt
```

### Running
```
python3 ctfr.py --help
```


## Usage
Parameters and examples of use.

### Parameters
```
-d --domain [target_domain] (required)
-o --output [output_file] (optional)
```

### Examples
```
python3 ctfr.py -d starbucks.com
```
```
python3 ctfr.py -d facebook.com -o /home/shei/subdomains_fb.txt
```


## Screenshots
<p align="center">
  <img src="http://www.semecayounexploit.com/CTFR/CTFR-ST.png" />
</p>

<p align="center">
  <img src="http://www.semecayounexploit.com/CTFR/CTFR-FB.png" />
</p>


### Running with Docker

For those of you that can't run python natively, you may use the unwavering whale. Build your image:

```
docker build -t ctfr .
```

And just run it!

```
docker run --rm ctfr -d starbucks.com
```

For keeping output files, just mount a volume. E.g.:

```
docker run --rm -v ${PWD}:/usr/ ctfr -d starbucks.com -o subdomains_sb.txt
```

## Author
* *Sheila A. Berta - [(@UnaPibaGeek)](https://www.twitter.com/UnaPibaGeek).*
