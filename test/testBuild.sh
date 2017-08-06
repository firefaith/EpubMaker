#!/usr/bin/env bash

target_dir="test_docs"
subname="test"
cate_name="cate.txt"

if [ -d $target_dir ]; then
  set -x
  rm -rf $target_dir
  set +x
fi

mkdir $target_dir
echo "testTitle" >> $target_dir/$cate_name
echo "testAurthor" >> $target_dir/$cate_name
for i in {1..5};
do
  output_title=$subname${i}
  echo $i > $target_dir/${output_title}.txt
  echo $output_title >> $target_dir/$cate_name
done
ls $target_dir
cat $target_dir/$cate_name

python2 buildEpub.py $target_dir/$cate_name $target_dir 
