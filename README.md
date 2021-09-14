# Nemesis
![Nemesis](pics/Nemesis.png)
[![Code Grade](https://www.code-inspector.com/project/15087/status/svg)](https://frontend.code-inspector.com/public/project/15087/Nemesis/dashboard)
[![Code Quality](https://www.code-inspector.com/project/15087/score/svg)](https://frontend.code-inspector.com/public/project/15087/Nemesis/dashboard)

## Description
A simple tool for scanning urls for vulnerabilites and sensitive information. It has lot of pre defined regexes for dom xss possibility detection, secrets leakage, hidden parameters, extra links and much more. 

## Features
1. Supports scanning of both html and javascript urls
2. Pre defined regexes for dom xss (sinks & sources), web services, hidden parameters, endpoints and a lot more are already present. 
3. Shannon entropy helps to find additional suspicious data that can be missed by regexes but may generate false positive so disabled by default.

## Usage
```
usage: Nemesis.py [-h] [--- | -w WORDLIST | -u URL] [-o OUTPUT] [-e] [-t THREADS] [-b]

Nemesis

optional arguments:
  -h, --help            show this help message and exit
  ---, ---              Stdin
  -w WORDLIST, --wordlist WORDLIST
                        Absolute path of wordlist
  -u URL, --url URL     url to scan
  -o OUTPUT, --output OUTPUT
                        Output file
  -e, --enable-entropy  Enable entropy search
  -t THREADS, --threads THREADS
                        Number of threads
  -b, --banner          Print banner and exit

Enjoy bug hunting
```

## Example
1. Scan a single url
 - ```Nemesis -u google.com``` or ```Nemesis -u https://google.com/closurelibrary.js```
2. Scan from URLs
 - ```Nemesis -w hakrawler.txt```

## Limitations
* Output maybe repeated such as same links again and again
* Output to file saving is in work
* Additional logical errors and false positivies from faulty regex

## Support
If you wanted to support me freely for the tools I create, chekout [this out](https://github.com/machinexa2/machinexa2/blob/master/SUPPORT.md).

