# Changelog

All notable changes to CTFR are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## 1.3.0 - 2026-09-25

### Added

- Support for complete URLs, paths, ports, uppercase names, trailing dots, and internationalized domain names as input.
- Validation that rejects empty, malformed, or non-fully-qualified targets before contacting crt.sh.
- `--timeout SECONDS` to configure the HTTP timeout. The default is 30 seconds.
- `--append` to preserve an existing output file and add only new names.
- `--version` and a version number in the banner.
- A final summary showing the number of unique names found and written.
- `pyproject.toml` with package metadata, Python requirements, dependencies, and the `ctfr` console command.
- `.gitignore` entries for Python, test, build, coverage, and virtual-environment artifacts.
- Seven unit tests covering input normalization, invalid targets, JSON extraction, HTTP request construction, deduplication, overwrite mode, and append mode.
- A GitHub Actions workflow that runs the test suite on Python 3.9 and 3.13.
- Virtual-environment, package installation, testing, and responsible-use instructions in the README.

### Changed

- Raised the documented minimum Python version from 3.0 to 3.9.
- Changed the version from `1.2` to `1.3.0` and represented it as a string.
- Reorganized the script into small, independently testable functions.
- Added an `if __name__ == "__main__"` guard, so importing `ctfr` no longer runs the command-line program.
- Moved `argparse` to the module imports and added a CLI description.
- Replaced manual URL cleanup with `urllib.parse.urlsplit` and IDNA normalization.
- A leading `www.` is removed to retain CTFR's previous target behavior.
- Requests to crt.sh now use encoded query parameters, a CTFR user-agent, status validation, and an explicit timeout.
- crt.sh `name_value` fields are split into individual lines before processing.
- Results are normalized to lowercase ASCII, sorted, and deduplicated.
- Wildcard entries such as `*.example.com` are represented as `example.com`.
- Results outside the requested domain are discarded.
- Output files are opened once instead of once per result and are always written as UTF-8.
- Updated the `requests` dependency to the supported range `>=2.32.0,<3.0.0`.
- Replaced outdated README installation and usage instructions.

### Fixed

- Fixed `https://example.com` being incorrectly interpreted as the target `https:`.
- Fixed complete URLs without `www.` producing invalid crt.sh queries.
- Fixed multiple certificate names being stored as one multiline result.
- Fixed duplicate names appearing when the same name is present in multiple certificates.
- Fixed repeated file opens and explicit closes inside a context manager.
- Fixed network, HTTP, malformed JSON, invalid target, and output file errors terminating with unhandled tracebacks.
- Fixed the declared version not appearing in the banner.
- Removed unused enumeration variables and commented-out legacy code.

### Behavior changes

- `--output` now **replaces** an existing file by default. Previous versions always appended. Use `--append` for the old behavior.
- Append mode does not write names already present in the destination file.
- Invalid targets now exit with status code `1` and print a concise error to standard error.
- HTTP errors and unavailable or malformed crt.sh responses now exit cleanly with status code `1`.
- Wildcard markers are omitted from output because they are certificate patterns, not literal hostnames.

### Validation performed

- `python3 -m unittest discover -s tests -v`: all seven tests pass.
- `python3 -m py_compile ctfr.py tests/test_ctfr.py`: compilation succeeds.
- A Python wheel for version 1.3.0 builds successfully.
- `python3 ctfr.py --help` and `python3 ctfr.py --version` execute successfully.
- A live query using `https://example.com/path` is normalized to `example.com` and returns scoped, unique results.
- `git diff --check` reports no whitespace errors.

### Known limitations

- CTFR depends on the availability and response format of the third-party crt.sh service.
- Certificate Transparency records are historical and do not prove that a hostname currently resolves or is reachable.
- CTFR only reports names found in certificates; it is not a complete inventory of a domain.
