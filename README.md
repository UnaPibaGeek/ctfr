# CTFR

CTFR discovers subdomains from public [Certificate Transparency](https://certificate.transparency.dev/) logs through [crt.sh](https://crt.sh/). It does not use dictionaries or brute force.

## Requirements

- Python 3.9 or later
- Internet access to `crt.sh`

## Installation

```bash
git clone https://github.com/UnaPibaGeek/ctfr.git
cd ctfr
python3 -m venv .venv
source .venv/bin/activate
python -m pip install .
```

This installs the `ctfr` command. For development, use `python -m pip install -e .` instead.

## Usage

```text
ctfr -d DOMAIN_OR_URL [-o FILE] [--append] [--timeout SECONDS]
```

The target can be a domain or a complete URL:

```bash
ctfr -d example.com
ctfr -d https://example.com/path
ctfr -d example.com -o subdomains.txt
ctfr -d example.com -o subdomains.txt --append
```

By default, `--output` replaces the destination file with sorted, unique results. Use `--append` to preserve its contents and add only names that are not already present.

You can also run the source file directly after installing the requirements:

```bash
python -m pip install -r requirements.txt
python3 ctfr.py -d example.com
```

## Tests

The test suite does not make external network requests:

```bash
python -m unittest discover -s tests -v
```

## Changes

See [CHANGELOG.md](CHANGELOG.md) for the complete list of fixes, new features, behavior changes, validation performed, and known limitations.

## Responsible use

Certificate Transparency data is public, but you should only investigate systems when you have authorization to do so.

## License

CTFR is distributed under the GNU General Public License v3.0. See [LICENSE](LICENSE).

## Author

Sheila A. Berta ([@UnaPibaGeek](https://www.twitter.com/UnaPibaGeek))
