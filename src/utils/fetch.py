import argparse
import re

import requests


def main():
    parser = argparse.ArgumentParser(description='Fetch font file from css')
    parser.add_argument('css', help='source css file')

    args = parser.parse_args()

    with open(args.css) as reader:
        url_re = re.compile(r"//([a-zA-Z0-9\-./_]+\.woff)")
        fname_re = re.compile(r"([a-zA-Z0-9]+\.woff)")
        urls = set(url_re.findall(reader.read()))

    fnames = [fname_re.findall(url)[0] for url in urls]
    for fname, url in zip(fnames, urls):
        resp = requests.get('https://{}'.format(url), allow_redirects=True)
        with open(fname, 'wb') as writer:
            writer.write(resp.content)


if __name__ == '__main__':
    main()
