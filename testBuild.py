#!/usr/bin/env python2
#coding:utf-8
import ConfigParser

cf = ConfigParser.ConfigParser()
conf_file = 'book.conf'
cf.read(conf_file)
cf.set('book','contents_path','testbook')

with open(conf_file,"w+") as f:
  cf.write(f)
  
