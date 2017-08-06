#!/usr/bin/env python2
# coding:utf-8
import sys
sys.path.append(r"../")
from lib.util import zip_dir

usage = '1 : output filename like xxx.zip,2: input_dir'
if len(sys.argv) != 3:
    print usage
    sys.exit(1)

filename = sys.argv[1]
input_dir = sys.argv[2]
zip_dir(input_dir,filename)



