#!/usr/bin/env python2
from lib.category import Category

c1 = Category("t1")
c11 = Category("t1.1")
c111 = Category("t1.1.1")
c12 = Category("t1.2")
c1.addCate(c11)
c1.addCate(c12)
c11.addCate(c111)
c1.printCate()
