# Python to read file by N lines each time
# https://coderwall.com/p/5vi8ca/use-python-to-read-file-by-n-lines-each-time

from __future__ import division
import sys

beam_width = 50

if len(sys.argv) != 4:
    print("usage: lines.py actual_correct input_buggy model_output")
    sys.exit(1)

with open(sys.argv[1]) as f:
    file_1 = [line.rstrip() for line in f]

with open(sys.argv[2]) as f:
    file_2 = [line.rstrip() for line in f]

with open(sys.argv[3]) as f:
    file_3 = [line.rstrip() for line in f]

model_output_file_name = sys.argv[3]
if len(file_1) != len(file_2) or len(file_2) != len(file_3) / beam_width or len(file_1) != len(file_3) / beam_width:
    print("files are different length")
    sys.exit(1)

from itertools import islice


def next_n_lines(file_opened, N):
    return [x.strip() for x in islice(file_opened, N)]


def average(lst):
    return sum(lst) / len(lst)


fp, fn, tp, tn = 0, 0, 0, 0
fn_maybe = 0
fp_maybe = 0

sample = open(model_output_file_name, 'r')

positions = []
for i in range(len(file_1)):
    fix_suggestions = next_n_lines(sample, beam_width)

    for position, fix_suggestion in enumerate(fix_suggestions):
        # if file_1[i] == fix_suggesstion and file_1[i] != file_2[i]:
        if file_1[i] == fix_suggestion:
            # true positive: model corrected an error correctly
            # print('line {} is a true positive'.format(i))
            tp += 1
            positions.extend([position + 1])
            print("sample line#: ",i, " buggy: ", file_2[i] , " inferred: ", file_1[i], " in position: ", position+1)

#for pos in positions:
#    print(pos)

print('  sure: average: {:10.4f} '.format(average(positions)))
print('  sure: true positive: {} '.format(tp))

