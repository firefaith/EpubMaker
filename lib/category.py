#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
cateFormatLines = []
class Category:
	global cateFormatLines 
	def __init__(self,title = 'category',level=-1): #-1 as top category
		self.title  = title
		self.level = level
		self.subCategory = []
		self.hasSub = False
		
	def setTitle(self,title):
		self.title = title
	def setLevel(self,level):
		self.level = level
	def getLevel(self,level):
		return self.level

	def hasSubCate(self):
		return self.hasSub

	def updateLevel(self,topLevel):
		self.level = topLevel
		for subcate in self.subCategory:
			subcate.updateLevel(topLevel + 1)

	def addSubCate(self,cate):
		self.hasSub = True
		cate.updateLevel(self.level + 1)
		self.subCategory.append(cate)

	def addSubTitle(self,title):
		subCate = Category(title)
		self.addSubCate(subCate)
	
	def getSubCate(self):
		return self.subCategory

	def printSubCate(self):
		if(len(self.subCategory)!=0):
			for cate in self.subCategory:
				print cate.title

	def geneCateLines(self):
		prefix=''
		if(self.level!=0):
			for i in range(self.level):
				prefix += '\t'
		if(self.level >= 0):
			cateFormatLines.append(prefix+self.title)
		if(self.hasSubCate()):
			for cate in self.subCategory:
				cate.geneCateLines()

	def printCate(self):
		prefix=''
		if(self.level>0):
			for i in range(self.level):
				prefix += '\t'
			print prefix,self.title
		if(self.level==0) :
			print self.title
		if(self.hasSubCate()):
			for cate in self.subCategory:
				cate.printCate()
	
	def write2file(self,outpath):
		global cateFormatLines
		cateFormatLines = [] #clear cache
		self.geneCateLines() # reformat cate lines
		outfile = open(outpath,'w')
		for line in cateFormatLines:
			#print line
			outfile.write(line+'\n')
		outfile.close()

	def getLevel(self,line):
		count = 0
		for w in line:
			if (w=='\t'): count +=1
			else: return count
		return count
	# 0 to sub,1 to last sub sub,...
	def put2Cate(self,title,level):
		if level==0:
			self.addSubTitle(title)
		else:
			self.getSubCate()[-1].put2Cate(title,level-1)

	def readCate(self,cate_path):
		self.__init__()
		cate_f = open(cate_path,'r')
		level = 0
		while 1:
			lines = cate_f.readlines(100)
			if not lines:
				break
			for title in lines:
				if(title.strip()==''):
					continue
				level = self.getLevel(title)				
				title = title.strip()
				self.put2Cate(title,level)

def test():
		cate =  Category()
		c1 = Category("t1")
		c11 = Category("t1.1")
		c111 = Category("t1.1.1")
		c12 = Category("t1.2")
		cate.addSubCate(c1)
		c1.addSubCate(c11)
		c1.addSubCate(c12)
		c11.addSubCate(c111)

		outpath = 'test_cate.txt'
		print "write ",outpath
		cate.write2file(outpath)
		c1.printCate()
		print "read ",outpath
		c1.readCate(outpath)
		c1.printCate()

if __name__ == "__main__":
	print "test Category..."
	test()