#!/usr/bin/env python3
import argparse
import sys

def create_parser():
    """
    Creates and returns the argparse parser with all the required options
    for the osintmaster tool.
    """
    # We use add_help=False so we can define --help manually under OPTIONS group
    # to better match the exact requirements of the subject.
    parser = argparse.ArgumentParser(
        description="Welcome to osintmaster multi-function Tool",
        add_help=False,
        formatter_class=argparse.RawTextHelpFormatter
    )

    options = parser.add_argument_group("OPTIONS")
    options.add_argument(
        "-i", metavar='"IP Address"', dest="ip", help="Search information by IP address"
    )
    options.add_argument(
        "-u", metavar='"Username"', dest="username", help="Search information by username"
    )
    options.add_argument(
        "-d", metavar='"Domain"', dest="domain", help="Enumerate subdomains and check for takeover risks"
    )
    options.add_argument(
        "-o", metavar='"FileName"', dest="output", help="File name to save output"
    )
    options.add_argument(
        "--help", action="help", help="Display this help message"
    )

    return parser

def main():
    parser = create_parser()

    if len(sys.argv) == 1:
        print("Welcome to osintmaster multi-function Tool\n")
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    # Display the banner
    print("Welcome to osintmaster multi-function Tool\n")

    # Routing logic based on arguments
    if args.ip:
        print(f"[*] Starting IP Lookup for: {args.ip}")
    if args.username:
        print(f"[*] Starting Username Lookup for: {args.username}")
    if args.domain:
        print(f"[*] Starting Domain Enumeration for: {args.domain}")
    if args.output:
        print(f"[*] Results will be saved to: {args.output}")

if __name__ == "__main__":
    main()
