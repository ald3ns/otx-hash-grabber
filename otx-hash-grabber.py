import requests
import argparse
import json
from rich.progress import track

def setup_parser():
    '''
    Setup argparse stuff
    '''
    parser = argparse.ArgumentParser(description="Grab malware family hashes from OTX")
    parser.add_argument("family", type=str, help="Specify the malware family you want in the format [name]:[platform]/[sample]. Ex: TrojanDownloader:Win32/Cutwail")
    parser.add_argument("-f", "--format", help="Hash output from md5, sha1, sha256, or all")
    parser.add_argument("-k", "--key", type=str, help="You OTX API key")
    parser.add_argument("-o", "--output", type=str, help="Name of your output file")
    return parser

def main():

    # Some important variables
    url = "https://otx.alienvault.com/otxapi/malware/samples?"
    key = ""

    # Setup the argument parser
    parser = setup_parser()
    args = parser.parse_args()

    # Check if the API key was supplied, if no then use the supplied key
    if key == "" and args.key != None:
        headers = {
            "X-OTX-API-KEY":args.key
        }
    elif key != "":
        headers = {
            "X-OTX-API-KEY":key
        }
    else:
        print("Missing API key...")
        exit()

    # These are the URL parameters, change them as you see fit
    payload = {
        "family":args.family,
        "limit":1000,
        "page":1
    }

    # Make first request to get the number of samples
    number = json.loads(requests.get(url, headers=headers, params=payload).text)
    num_samples = number["count"]
    print(f"Expecting {num_samples} hashes")

    # Create the output array for writing or printing
    to_write = []

    # Loop over all of the page numbers
    for page in track(range(1, (num_samples//1000)+2), description="[green]Downloading..."):

        # Update the page
        payload["page"] = page

        # Make the updated request and parse to JSON
        hashes = json.loads(requests.get(url, headers=headers, params=payload).text)

        # Loop over the results
        for result in hashes["results"]:
            if args.format == "md5":
                to_write.append(result['md5'])
            elif args.format == "sha1":
                to_write.append(result['sha1'])
            elif args.format == "sha256":
                to_write.append(result['sha256'])
            else:
                to_write.append(f"{result['md5']} {result['sha1']} {result['sha256']}")

    # Check if we should write to a file if so do that
    if args.output != None:
        file = open(args.output, "w")
        for i in to_write:
            file.write(i)
            file.write("\n")
        file.close()
    else:
        for i in to_write:
            print(i)

    print(f"Successfully wrote hashes to {args.output}")


if __name__ == "__main__":
    main()
