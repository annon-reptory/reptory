#!/usr/bin/python
# -*- coding: utf-8 -*-
# Python to read file by N lines each time
# https://coderwall.com/p/5vi8ca/use-python-to-read-file-by-n-lines-each-time

from __future__ import division
import sys
from itertools import islice

beam_width = 25


class Patch(object):
    line_number_in_correct_file = -1
    buggy = "N/A"
    inferred = "N/A"
    position = "-1"

    def __init__(self, line_number_in_correct_file, buggy, inferred, position):
        self.line_number_in_correct_file = line_number_in_correct_file
        self.buggy = buggy
        self.inferred = inferred
        self.position = position


if len(sys.argv) != 5:
    print('usage: lines.py actual_correct input_buggy model_output output_patch_file')
    sys.exit(1)

with open(sys.argv[1]) as f:
    file_1 = [line.rstrip() for line in f]

with open(sys.argv[2]) as f:
    file_2 = [line.rstrip() for line in f]

with open(sys.argv[3]) as f:
    file_3 = [line.rstrip() for line in f]

model_output_file_name = sys.argv[3]
if len(file_1) != len(file_2) \
        or len(file_2) != len(file_3) / beam_width \
        or len(file_1) != len(file_3) / beam_width:
    print('files are different length')
    sys.exit(1)

output_patch_file = sys.argv[4]


def next_n_lines(file_opened, N):
    return [x.strip() for x in islice(file_opened, N)]


def average(lst):
    if len(lst) == 0:
        return -1
    return sum(lst) / len(lst)


tp = 0
sample = open(model_output_file_name, 'r')

positions = []
patches = list()
for i in range(len(file_1)):
    fix_suggestions = next_n_lines(sample, beam_width)
    for (position, fix_suggestion) in enumerate(fix_suggestions):
        if file_1[i] == fix_suggestion:
            tp += 1
            positions.extend([position + 1])

            patch = Patch(line_number_in_correct_file=i,
                          buggy=file_2[i],
                          inferred=fix_suggestion,
                          position=position + 1)
            patches.append(patch)
            # print("corrected patch#: ", i,
            #       " buggy: ", file_2[i],
            #       " inferred: ", file_1[i],
            #       " in position: ", position + 1)

with open(output_patch_file, 'w') as f:
    for p in patches:
        str_patch = 'buggy={}, inferred={}, position={}, line_number_in_correct_file={}\n' \
            .format(p.buggy,
                    p.inferred,
                    p.position,
                    p.line_number_in_correct_file)
        f.write(str_patch)

print('  positions (average) :  {:10.4f} '.format(average(positions)))
print('  exact match         :  {} '.format(tp))
print('  saved patches to file: {} '.format(output_patch_file))
