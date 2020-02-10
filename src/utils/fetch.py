import argparse
import json
import re

import requests


def main():
    parser = argparse.ArgumentParser(description='Fetch font file from css')
    parser.add_argument('css', help='source css file')

    args = parser.parse_args()

    with open(args.css) as reader:
        # fname_re = re.compile(r"([a-zA-Z0-9]+\.woff)")
        buffer = reader.read().split("@font-face{")
        buffer = list(filter(None, buffer))
    font_name_re = re.compile(r"font-family:\s+\"([\w-]+)\"")
    url_re = re.compile(r"//([a-zA-Z0-9\-./_]+\.woff)")
    font_names = []
    urls = []
    for line in buffer:
        font_names.append(font_name_re.findall(line)[0])
        urls.append(url_re.findall(line)[0])

    print(font_names, urls)
    assert len(font_names) == len(urls)
    # fnames = [fname_re.findall(url)[0] for url in urls]
    for fname, url in zip(font_names, urls):
        resp = requests.get('https://{}'.format(url), allow_redirects=True)
        with open('{}.woff'.format(fname), 'wb') as writer:
            writer.write(resp.content)

    # create mapping
    mapping = {}
    mapping_re = re.compile(r".(\w+){font-family:\s+['\"]([\w-]+)['\"]")
    for line in buffer:
        clz, font = mapping_re.findall(line)[0]
        mapping[clz] = '{}.woff'.format(font)
    with open('mapping.json', 'w') as writer:
        json.dump(mapping, writer)


if __name__ == '__main__':
    main()
