# OTX Family Hash Grabber

A simple little script to download all of the sample hashes from the OTX malware
family page.

## Installation
Install with `pip` or whatever your favorite package manager is. There are only
two dependencies: `argparse` and `rich`.

```bash
python3 -m pip install -r requirements.txt
```

## Usage 

```
usage: otx-hash-grabber.py [-h] [-f FORMAT] [-k KEY] [-o OUTPUT] family

Grab malware family hashes from OTX

positional arguments:
  family                Specify the malware family you want in the format
                        [name]:[platform]/[sample]

optional arguments:
  -h, --help            show this help message and exit
  -f FORMAT, --format FORMAT
                        Hash output from md5, sha1, sha256, or all
  -k KEY, --key KEY     You OTX API key
  -o OUTPUT, --output OUTPUT
                        Name of your output file
```
