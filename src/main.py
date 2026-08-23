#!/usr/bin/env python3
import argparse
import sys
from ip_lookup import lookup_ip
from username_lookup import lookup_username
from domain_enum import enumerate_domain

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

    # Routing logic based on arguments
    output_lines = []
    
    if args.ip:
        output_lines.append("IP Address:\n")
        output_lines.append(lookup_ip(args.ip))
        output_lines.append("")
        
    if args.username:
        output_lines.append("Username:\n")
        output_lines.append(lookup_username(args.username))
        output_lines.append("")
        
    if args.domain:
        output_lines.append("Domain and Subdomain Enumeration:\n")
        output_lines.append(enumerate_domain(args.domain))
        output_lines.append("")

    final_output = "\n".join(output_lines).strip()
    
    if final_output:
        print(final_output)
        
    if args.output:
        try:
            with open(args.output, "w") as f:
                f.write(final_output + "\n")
            print(f"\nData saved in {args.output}")
        except Exception as e:
            print(f"\nError saving data to {args.output}: {e}")

if __name__ == "__main__":
    main()
