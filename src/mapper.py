import argparse
import pickle
from math import dist
from statistics import mean

from tqdm import tqdm

parser = argparse.ArgumentParser(description='Generate character mapping')
parser.add_argument('target', help='target font file')
parser.add_argument('original', help='original font file')

args = parser.parse_args()

with open(args.target, 'rb') as tf, open(args.original, 'rb') as of:
    target = pickle.load(tf)
    original = pickle.load(of)


def compare(c1: set, c2: set):
    d1 = c1.difference(c2)
    d2 = c2.difference(c1)
    distance = []
    if d2:
        for xy in d1:
            distance.append(min([dist(xy, _xy) for _xy in d2]))
    if d1:
        for xy in d2:
            distance.append(min([dist(xy, _xy) for _xy in d1]))
    if distance:
        return mean(distance)
    else:
        return 0


min_vals = []
original_list = list(original.items())


def find(c):
    candidates = []
    for k, v in original_list:
        if v['coordinates'] == c[1]['coordinates']:
            return c[0], k, c[1]['unicode'], v['unicode']
        if (len(v['coordinates'].difference(c[1]['coordinates'])) +
            len(c[1]['coordinates'].difference(v['coordinates']))) / 2 < 5:
            candidates.append((k, v))
    if not candidates:
        return c[0], None, None, None
    dists = [compare(v['coordinates'], c[1]['coordinates']) for _, v in candidates]
    min_val = min(dists)
    min_id = dists.index(min_val)
    min_char = candidates[min_id]
    min_vals.append(min_val)
    return c[0], min_char[0], c[1]['unicode'], min_char[1]['unicode']


result = [find(c) for c in tqdm(target.items())]
cnt = 0
for item in result:
    if item[1] is None:
        cnt += 1
        # print(item)
    else:
        print(chr(item[-2]), chr(item[-1]))
print(cnt / len(result) * 100, '%')
print(result)
print(min_vals)
