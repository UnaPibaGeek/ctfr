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
```bash
$ git clone https://github.com/UnaPibaGeek/ctfr.git
$ cd ctfr
$ pip3 install -r requirements.txt
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


## Screenshots
<p align="center">
  <img src="http://www.semecayounexploit.com/CTFR/CTFR-ST.png" />
</p>

<p align="center">
  <img src="http://www.semecayounexploit.com/CTFR/CTFR-FB.png" />
</p>


## Running with Docker

Running `ctfr` in docker enables for easy cloud deployment.

##### [Demo](https://asciinema.org/a/P1xuBzRPoFNnT5rVxQD0uqbLm)
To run `ctfr` in a docker container, simply build and run as follows:  
```bash
git clone https://github.com/UnaPibaGeek/ctfr
cd ctfr
docker build -t ctfr .
docker run -it ctfr -d example.com


```

## Author
* *Sheila A. Berta - [(@UnaPibaGeek)](https://www.twitter.com/UnaPibaGeek).*
