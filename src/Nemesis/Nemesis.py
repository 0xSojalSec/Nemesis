#!/usr/bin/python3

from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor

from Nemesis.lib.Extract import extract_url
from Nemesis.lib.Functions import starter

def main():
    parser = ArgumentParser(description='\x1b[33mNemesis\x1b[0m', epilog='\x1b[33mEnjoy bug hunting\x1b[0m')
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument('---', '---', action="store_true", dest="stdin", help="Stdin")
    input_group.add_argument('-w', '--wordlist', type=str, help='Absolute path of wordlist')
    input_group.add_argument('-u', '--url', type=str, help="url to scan")
    #parser.add_argument('-d', '--domain', type=str, help="Domain")
    parser.add_argument('-o', '--output', type=str, help="Output file")
    parser.add_argument('-e', '--enable-entropy', action="store_true", help="Enable entropy search")
    parser.add_argument('-t', '--threads', type=int, help="Number of threads")
    parser.add_argument('-b', '--banner', action="store_true", help="Print banner and exit")
    argv = parser.parse_args()
    input_wordlist = starter(argv)

    for input_url in input_wordlist:
        extract_url(input_url)
#     with ThreadPoolExecutor(max_workers=argv.threads) as submitter:
        # future_objects = [submitter.submit(extract_url, input_word) for input_word in input_wordlist]
        # if argv.output_directory:
            # pass
            # #output_writer(argv.domain, future_objects, filepath=argv.output_directory)
        # elif argv.output:
            # pass
            # #output_writer(argv.output, future_objects, filepath=None)

if __name__ == "__main__":
    main()
