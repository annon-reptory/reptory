import sys

if len(sys.argv) != 4:
    print("usage: lines.py actual_correct input_buggy model_output")
    sys.exit(1)

with open(sys.argv[1]) as f:
    file_1 = [line.rstrip() for line in f]

with open(sys.argv[2]) as f:
    file_2 = [line.rstrip() for line in f]

with open(sys.argv[3]) as f:
    file_3 = [line.rstrip() for line in f]

if len(file_1) != len(file_2) or len(file_2) != len(file_3) or len(file_1) != len(file_3) :
    print("files are different length")
    sys.exit(1)

fp, fn, tp, tn = 0, 0, 0, 0
fn_maybe = 0
fp_maybe = 0

for i in range(len(file_1)):
    if file_1[i] != file_2[i] and file_2[i] != file_3[i] and file_1[i] != file_3[i] :
        print('line {} has a difference in all files, might be a false negative?'.format(i))
        print('\t\033[1m{}\033[0m\t: {}'.format(sys.argv[1], file_1[i]))
        print('\t\033[1m{}\033[0m\t: {}'.format(sys.argv[2], file_2[i]))
        print('\t\033[1m{}\033[0m\t: {}'.format(sys.argv[3], file_3[i]))
        fn_maybe += 1
    elif file_1[i] == file_2[i] and file_2[i] == file_3[i]:
        # true negative: nothing was wrong with the code
        # print('line {} is a true negative'.format(i))
        tn += 1
    elif file_1[i] == file_3[i] and file_1[i] != file_2[i]:
        # true positive: model corrected an error correctly
        # print('line {} is a true positive'.format(i))
        tp += 1
    elif file_1[i] == file_2[i] and file_2[i] != file_3[i]:
        print('line {} might be a false positive'.format(i))
        print('\t\033[1m{}\033[0m\t: {}'.format(sys.argv[1], file_1[i]))
        print('\t\033[1m{}\033[0m\t: {}'.format(sys.argv[3], file_3[i]))
        fp_maybe += 1
    elif file_1[i] != file_3[i] and file_2[i] == file_3[i]:
        # false negative: model didn't do anything
        # print('line {} is a false negative'.format(i))
        fn += 1

print('  sure: true positive: {} \t true negative: {} \t false negative: {}'.format(tp, tn, fn))
print('unsure: false positive: {} \t false negative: {}'.format(fp_maybe, fn_maybe))
print('sanity check: total of above {}, line count {}'.format(tp+tn+fp+fn+fp_maybe+fn_maybe, len(file_1)))

