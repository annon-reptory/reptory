rm -rf empty_dir
mkdir empty_dir

rsync -a --delete empty_dir/ *Buggy/
rm -rf *Buggy

rsync -a --delete empty_dir/ *Correct/
rm -rf *Correct

rsync -a --delete empty_dir/ *Data/
rm -rf *Data

rmdir empty_dir
