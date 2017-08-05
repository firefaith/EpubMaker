#!/usr/bin/env python2
#coding:utf-8
import sys,os
from jinja2 import Template
from jinja2 import Environment,PackageLoader
import ConfigParser
from lib import const

reload(sys)
sys.setdefaultencoding('utf-8')
usage = \
'1: configuration file path \n' + \
'note: \n' + \
'    title ,author, document path, category path are in the conf file. \n '

def remkdir(input_dir):
  if os.path.exists(input_dir)==False:
    os.mkdir(input_dir)
  else:
    os.system('rm -rf '+ input_dir)
    os.mkdir(input_dir)

def buildEpub(cur_dir,tmp_dir,out_dir,name):
  # copy template/epubtmp/* tmp/
  # copy output/*.html tmp/OEBPS/Text/
  # copy output/content.opf tmp/OEBPS/
  # copy output/toc.ncx tmp/OEBPS/
  # cd tmp/ zip -r name.epub *
  # mv epub to current dir
  cmdstr = 'cp -r '+cur_dir+'/templates/epubtmp/* '+tmp_dir + ' && ' + \
  'cp -r '+out_dir+'/*.html '+tmp_dir+'/OEBPS/Text/ ' + ' && ' + \
  'cp -r '+out_dir+'/content.opf '+tmp_dir+'/OEBPS/'   + ' && ' + \
  'cp -r '+out_dir+'/toc.ncx '+tmp_dir+'/OEBPS/'   + ' && ' + \
  'cd '+tmp_dir+' && zip -r '+name+'.epub *' 
  os.system(cmdstr)
  os.system('mv '+tmp_dir+'/'+name+'.epub ' + cur_dir+'/' )

# current dir
pwd = sys.path[0]
if os.path.isfile(pwd):
  pwd = os.path.dirname(pwd)
print "current path:",pwd
if len(sys.argv)!=2:
    print usage
    sys.exit(1)

conf_path = sys.argv[1]
cf = ConfigParser.ConfigParser()
cf.read(conf_path)
book_name = cf.get(const.CONF_NAME,const.BOOK_NAME)
doc_prefix = cf.get(const.CONF_NAME,const.CONTENT_PATH)
cate_path = cf.get(const.CONF_NAME,const.CATE_PATH,cate_file)
author = cf.get(const.CONF_NAME,const.AUTHOR)
cf.get(const.CONF_NAME,const.DESC,'default book for testing')
cf.get(const.CONF_NAME,const.PUB,'Red over China')
cf.get(const.CONF_NAME,const.LANG,'zh.cn')

#cate_path = sys.argv[1]
#doc_prefix = sys.argv[2]
out_prefix = doc_prefix + '/output'
tmp_path = doc_prefix + '/tmp'

remkdir(out_prefix)
remkdir(tmp_path)

env = Environment(loader=PackageLoader(__name__, 'templates'))  
env.trim_blocks = True
env.lstrip_blocks = True

# read text file according to category file,and convert it to html
cate_f = open(cate_path,'r')
#book_name = cate_f.readline().strip() # read title
#author = cate_f.readline().strip() # read author
no=0
sections=[]
while 1:
    lines = cate_f.readlines(100)
    if not lines:
        break
    for title in lines:
        title = title.strip()
        print title
        input_path = doc_prefix + "/"+title +".txt"
        output_path = out_prefix+"/"+ str(no) +".html"
        item={}
        item['name'] = "x"+str(no)+".html"
        item['title']=title
        item['full'] = "Text/"+str(no)+".html"
        item['media_type'] = "application/xhtml+xml"
        sections.append(item)
        # convert content to html 
        page={}
        page['title']=title
        content=[]
        no = no + 1
        # read input file
        print 'read file ',input_path
        input_f = open(input_path,'r')
        while 1:
          content_lines = input_f.readlines(100)
          if not content_lines:
              break
          for l in content_lines:
              content.append(l.strip())
        page['content'] = content
        html_tpl = env.get_template('00_item.html')
        html = html_tpl.render(page)
        # write item.html
        output_f = open(output_path,'w')
        output_f.write(html)
        input_f.close()
        output_f.close()
        
# output toc.ncx
params={}
params['sections']=sections[:]
params['spine']=sections[:]
params['files']=sections[:]
params['title']=book_name
params['author']=author

env.trim_blocks = True
env.lstrip_blocks = True
toc_tpl = env.get_template('00_toc.ncx')
cnt_tpl = env.get_template('00_content.opf')

toc = toc_tpl.render(params)
cnt = cnt_tpl.render(params)

out_toc = open(out_prefix+'/toc.ncx','w')
out_cnt = open(out_prefix+'/content.opf','w')
out_toc.write(toc)
out_toc.close()

# output content.opf
out_cnt.write(cnt)
out_cnt.close()

# buildEpub
buildEpub(pwd,tmp_path,out_prefix,book_name)
