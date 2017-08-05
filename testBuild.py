#!/usr/bin/env python2
#coding:utf-8
import ConfigParser
from lib import const

cf = ConfigParser.ConfigParser()
conf_file = 'book.conf'
cate_file = 'testbooke_cate.txt'
cf.read(conf_file)
cf.set(const.CONF_NAME,const.BOOK_NAME,'TestBook')
cf.set(const.CONF_NAME,const.CONTENT_PATH,'testbook')
cf.set(const.CONF_NAME,const.CATE_PATH,cate_file)
cf.set(const.CONF_NAME,const.AUTHOR,'firefaith')
cf.set(const.CONF_NAME,const.DESC,'default book for testing')
cf.set(const.CONF_NAME,const.PUB,'Red over China')
cf.set(const.CONF_NAME,const.LANG,'zh.cn')

with open(conf_file,"w+") as f:
   cf.write(f)
  

print const.BOOK_NAME

with open(cate_file,"w") as f:
	for i in range(3):
		f.write("title_"+ str(i+1)+'\n')
		for j in range(2):
			f.write("\tsubtitle_"+str(i+1)+"."+str(j+1)+'\n')
			if(j==1):
				f.write("\t\ttrd_subtitle_"+str(i+1)+"."+str(j+1)+'.1\n')


