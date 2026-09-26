#!/usr/bin/env python3
"""Discover subdomains through Certificate Transparency logs."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any, Iterable, Optional, Sequence
from urllib.parse import urlsplit

import requests


VERSION = "1.3.0"
CRT_SH_URL = "https://crt.sh/"
DEFAULT_TIMEOUT = 30.0
DOMAIN_LABEL = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$")


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Discover subdomains using Certificate Transparency logs."
    )
    parser.add_argument("-d", "--domain", required=True, help="Target domain or URL.")
    parser.add_argument("-o", "--output", type=Path, help="Output file.")
    parser.add_argument(
        "--append",
        action="store_true",
        help="Append only new results instead of replacing the output file.",
    )
    parser.add_argument(
        "--timeout",
        type=positive_number,
        default=DEFAULT_TIMEOUT,
        metavar="SECONDS",
        help=f"HTTP timeout in seconds (default: {DEFAULT_TIMEOUT:g}).",
    )
    parser.add_argument("--version", action="version", version=f"CTFR {VERSION}")
    return parser.parse_args(argv)


def positive_number(value: str) -> float:
    try:
        number = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be a number") from exc
    if number <= 0:
        raise argparse.ArgumentTypeError("must be greater than zero")
    return number


def banner() -> None:
    print(
        rf"""
          ____ _____ _____ ____
         / ___|_   _|  ___|  _ \
        | |     | | | |_  | |_) |
        | |___  | | |  _| |  _ <
         \____| |_| |_|   |_| \_\\

                       v{VERSION}
"""
    )


def normalize_domain(value: str) -> str:
    """Return a validated ASCII domain from a domain name or URL."""
    value = value.strip()
    if not value:
        raise ValueError("the target domain cannot be empty")

    parsed = urlsplit(value if "://" in value else f"//{value}")
    try:
        hostname = parsed.hostname
        parsed.port  # Validate a port if one was supplied.
    except ValueError as exc:
        raise ValueError(f"invalid target: {exc}") from exc

    if not hostname:
        raise ValueError("the target does not contain a valid domain")

    hostname = hostname.rstrip(".").lower()
    if hostname.startswith("www."):
        hostname = hostname[4:]
    try:
        domain = hostname.encode("idna").decode("ascii")
    except UnicodeError as exc:
        raise ValueError("the target contains an invalid internationalized domain") from exc

    if len(domain) > 253 or "." not in domain:
        raise ValueError("enter a fully qualified domain, such as example.com")
    if not all(DOMAIN_LABEL.fullmatch(label) for label in domain.split(".")):
        raise ValueError(f"invalid domain: {hostname}")
    return domain


def extract_subdomains(records: Any, target: str) -> list[str]:
    """Extract, normalize, and scope names returned by crt.sh."""
    if not isinstance(records, list):
        raise ValueError("crt.sh returned an unexpected JSON response")

    subdomains: set[str] = set()
    for record in records:
        if not isinstance(record, dict):
            continue
        name_value = record.get("name_value")
        if not isinstance(name_value, str):
            continue

        for name in name_value.splitlines():
            name = name.strip().lower().rstrip(".")
            if name.startswith("*."):
                name = name[2:]
            try:
                name = name.encode("idna").decode("ascii")
            except UnicodeError:
                continue
            if name == target or name.endswith(f".{target}"):
                if len(name) <= 253 and all(
                    DOMAIN_LABEL.fullmatch(label) for label in name.split(".")
                ):
                    subdomains.add(name)

    return sorted(subdomains)


def fetch_subdomains(
    target: str,
    timeout: float = DEFAULT_TIMEOUT,
    client: Any = requests,
) -> list[str]:
    response = client.get(
        CRT_SH_URL,
        params={"q": f"%.{target}", "output": "json"},
        headers={"User-Agent": f"CTFR/{VERSION}"},
        timeout=timeout,
    )
    response.raise_for_status()
    return extract_subdomains(response.json(), target)


def save_subdomains(
    subdomains: Iterable[str], output_file: Path, append: bool = False
) -> int:
    """Write results once and return the number of names written."""
    names = sorted(set(subdomains))

    if not append:
        output_file.write_text(
            "".join(f"{name}\n" for name in names), encoding="utf-8"
        )
        return len(names)

    previous = output_file.read_text(encoding="utf-8") if output_file.exists() else ""
    existing = set(previous.splitlines())
    new_names = [name for name in names if name not in existing]
    if not new_names:
        return 0

    separator = "\n" if previous and not previous.endswith("\n") else ""
    with output_file.open("a", encoding="utf-8") as file:
        file.write(separator + "".join(f"{name}\n" for name in new_names))
    return len(new_names)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    banner()

    try:
        target = normalize_domain(args.domain)
        subdomains = fetch_subdomains(target, args.timeout)
        saved = (
            save_subdomains(subdomains, args.output, args.append)
            if args.output is not None
            else 0
        )
    except (OSError, ValueError, requests.RequestException) as exc:
        print(f"[X] {exc}", file=sys.stderr)
        return 1

    print(f"[!] ---- TARGET: {target} ---- [!]\n")
    for subdomain in subdomains:
        print(f"[-]  {subdomain}")

    print(f"\n[!] Found {len(subdomains)} unique name(s).")
    if args.output is not None:
        action = "appended" if args.append else "written"
        print(f"[!] {saved} name(s) {action} to {args.output}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
