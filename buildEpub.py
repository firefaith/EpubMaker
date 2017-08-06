#!/usr/bin/env python2
# coding:utf-8
import sys
import os
from jinja2 import Template
from jinja2 import Environment, PackageLoader
import ConfigParser
from lib import const
from lib.category import Category
from lib.util import zip_dir
import shutil

reload(sys)
sys.setdefaultencoding('utf-8')

# global variable 
usage = \
    '1: configuration file path \n' + \
    'note: \n' + \
    '    title ,author, document path, category path are in the conf file. \n '
no = 0 # page number
orderId = 0 # page order id
env = Environment(loader=PackageLoader(__name__, 'templates'))
env.trim_blocks = True
env.lstrip_blocks = True
sections = [] # contains all page
params = {} # write to toc and content.opf file

def remkdir(input_dir):
    if os.path.exists(input_dir) == False:
        os.makedirs(input_dir)
    else:
        shutil.rmtree(input_dir)
        os.mkdir(input_dir)


def buildEpub(cur_dir, tmp_dir, out_dir, name):
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
    os.system('mv '+tmp_dir+'/'+name+'.epub ' + cur_dir+'/')

# read each article ,return lines[]
def readContent(input_path):
    content = []
    print 'read file ', input_path
    input_f = open(input_path, 'r')
    while 1:
        content_lines = input_f.readlines(100)
        if not content_lines:
            break
        for l in content_lines:
            content.append(l.strip())
    input_f.close()
    return content


# category item
def getItem(title, no):
    item = {}
    item['name'] = "x"+str(no)+".html"
    item['title'] = title
    item['full'] = "Text/"+str(no)+".html"
    item['media_type'] = "application/xhtml+xml"
    return item


def writeOnePage(title, no, input_prefix, output_prefix):
    global env
    input_path = input_prefix + "/"+title + ".txt"
    output_path = output_prefix+"/" + str(no) + ".html"
    # read input file
    content = readContent(input_path)
    page = {}
    page['title'] = title
    page['content'] = content
    html_tpl = env.get_template('00_item.html')
    html = html_tpl.render(page)
    # write item.html
    output_f = open(output_path, 'w')
    output_f.write(html)
    output_f.close()


def processCate(cate,input_prefix,output_prefix):
    global no,sections,orderId
    cate.setOrderId(orderId)
    orderId += 1
    if cate.hasSub:
        print "parent cate:", cate.title, cate.level, no
        for c in cate.getSubCate():
            processCate(c,input_prefix,output_prefix)
        cate.setSrc(cate.getSubCate()[0].src)  # for  render template toc
    else:
        print "text :", cate.title, cate.level, no
        item = getItem(cate.title, no)
        cate.setSrc( item['full'] )  # for  render template toc
        sections.append(item)
        # convert content to html
        writeOnePage(cate.title, no,input_prefix, output_prefix) 
        no += 1

def readConf(conf_path):
	#  read configuration
	global params
	cf = ConfigParser.ConfigParser()
	cf.read(conf_path)
	params['title'] = cf.get(const.CONF_NAME, const.BOOK_NAME)
	doc_prefix = cf.get(const.CONF_NAME, const.CONTENT_PATH)
	cate_path = cf.get(const.CONF_NAME, const.CATE_PATH)
	params['author'] = cf.get(const.CONF_NAME, const.AUTHOR)
	params['description'] = cf.get(const.CONF_NAME, const.DESC)
	params['publisher'] = cf.get(const.CONF_NAME, const.PUB)
	params['language'] = cf.get(const.CONF_NAME, const.LANG)
	return (doc_prefix,cate_path)

def init_epubdir(doc_prefix,template_dir):
	#META-INF/ mimetype  OEBPS/
	remkdir(doc_prefix)
	shutil.copytree(template_dir+"/META-INF", doc_prefix+"/META-INF")
	shutil.copyfile(template_dir+"/mimetype", doc_prefix+"/mimetype")
	shutil.copytree(template_dir+"/OEBPS", doc_prefix+"/OEBPS")


# current dir
pwd = sys.path[0]
if os.path.isfile(pwd):
    pwd = os.path.dirname(pwd)
print "current path:", pwd

if len(sys.argv) != 2:
    print usage
    sys.exit(1)

conf_path = sys.argv[1]

(doc_prefix,cate_path) = readConf(conf_path)

# output_prefix = doc_prefix + '/output'	# store html file
epub_path = doc_prefix + '/epub'

init_epubdir(epub_path,'templates/epubtmp')


cate = Category("category")
cate.readCate(cate_path)

# convert txt to html
processCate(cate,doc_prefix,epub_path+'/OEBPS/Text')

# output toc.ncx
params['cate'] = cate
params['spine'] = sections[:]
params['files'] = sections[:]

env.trim_blocks = True
env.lstrip_blocks = True
toc_tpl = env.get_template('00_toc.ncx')
content_tpl = env.get_template('00_content.opf')

toc = toc_tpl.render(params)
cnt = content_tpl.render(params)

out_toc = open(epub_path+'/OEBPS/toc.ncx', 'w')
out_cnt = open(epub_path+'/OEBPS/content.opf', 'w')

# ouput toc
out_toc.write(toc)
out_toc.close()

# output content.opf
out_cnt.write(cnt)
out_cnt.close()

# buildEpub
zip_dir(epub_path,params['title']+'.epub')
