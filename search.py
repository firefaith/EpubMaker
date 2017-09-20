#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys,os
import re
reload(sys)
sys.setdefaultencoding("utf-8")
W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[34m' # blue
P  = '\033[35m' # purple
SEP = "\.|。|，"

def find(fpath,key):
  f = open(fpath,'r')
  formatKey = "{}{}{}".format(G,key,W)
  formatPath = "{}{}{}".format(P,fpath,W)
  line_num = 0
  key_count = 0
  while 1:
    lines = f.readlines(1000)
    if not lines:
      break
    for line in lines:
      line_num = line_num + 1
      partline = re.split(SEP,line)
      #print len(partline)
      for l in partline:
      	#print l
        if key in l:
          formatLine = l.replace(key,formatKey)
          n = l.count(key)
          key_count = key_count + n
          print line_num,formatPath,formatLine

  print "Doc stat:",formatPath,key_count
  return key_count   
def gci(filepath,key):
#遍历filepath下所有文件，包括子目录
  files = os.listdir(filepath)
  key_count = 0
  for fi in files:
    if os.path.isdir(fi):
      gci(fi)                  
    else:
      fpath =  os.path.join(filepath,fi)
      key_count = key_count + find(fpath,key)
      #print fpath
  print "All stat:{} in {} appear {} ".format(key,filepath,key_count)

if(len(sys.argv)!=3):
  print("Error:less args.1 input dir,2 search key")
  sys.exit()

inputdir = sys.argv[1]
key = sys.argv[2]

print(R+"hello how are you"+W)
print("{}Hello{}World{}!!!!".format(R,G,W))

gci(inputdir,key)