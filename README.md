# EpubMaker

## Intrudoction
本项目通过python制作简单的epub电子书
v1.0 版本仅支持文本类型的电子书

## Depedencies
python > 2.6
jinjia2

## Usage
准备好目录文件，如 cate.txt,每一行为目录的标题
准备好文本文件，存放与一个目录中，如documents，每个文件的文件名为目录中的标题名，后缀为.txt
buildEpub.py cate.txt documents
或
运行testBuild.sh，会在当前目录下创建一个测试的epub电子书
