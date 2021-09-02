#!/usr/bin/python3

from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor

from Nemesis.lib.Scan import NemesisScan
from Nemesis.lib.Functions import starter

def main():
    parser = ArgumentParser(description='\x1b[33mNemesis\x1b[0m', epilog='\x1b[33mEnjoy bug hunting\x1b[0m')
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument('---', '---', action="store_true", dest="stdin", help="Stdin")
    input_group.add_argument('-w', '--wordlist', type=str, help='Absolute path of wordlist')
    input_group.add_argument('-u', '--url', type=str, help="Url to scan")
    parser.add_argument('-b', '--banner', action="store_true", help="Print banner and exit")
    parser.add_argument('-d', '--domain', type=str, help="Base domain (optional)")
    parser.add_argument('-o', '--output', type=str, help="Output file")
    parser.add_argument('-e', '--enable-entropy', action="store_true", help="Enable entropy search")
    parser.add_argument('-t', '--threads', type=int, help="Number of threads")

    argv = parser.parse_args()
    input_wordlist = starter(argv)

    scanner_options = {
        'domain': argv.domain or "",
        'enable_entropy': argv.enable_entropy,
    }
    scanner = NemesisScan(scanner_options)

    for url in input_wordlist:
        scanner.scan_url(url)
"""     with ThreadPoolExecutor(max_workers=argv.threads) as submitter:
            future_objects = [submitter.submit(extract_url, input_word) for input_word in input_wordlist]
"""

if __name__ == "__main__":
    main()
