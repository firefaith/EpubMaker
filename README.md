# EpubMaker

## Intrudoction
本项目通过python制作简单的epub电子书
v1.1 版本支持多级目录，从配置文件读取电子书meta信息
v1.0 版本仅支持文本类型的电子书

## Depedencies
python > 2.6

jinja2

## Usage
v1.1
- 生成测试样例 generate example configuration and ebook raw files:`python test/testBuild.py`
- 生成epub，generate epub book: `python buildEpub.py book.conf`
- 填充配置文件，如book.conf，定义目录文件路径cate.txt 及 文本文件路径
- cate.txt 文件的结构：tab符作为次级目录的标识，如
> first level title # 第一级目录

> \tsecond level title # 第二级目录

> \t\tthrid level title # 第三级目录

- Note:
基本的逻辑：

读取 title in cate.txt ==> 再读取 content_path/title.txt ==> render to html
``` shell
list t1,t2
  t1=tuple(title,list)
list(tuple(string,list))
data struct: cate title,list sub cate
```
v1.0

- 准备好目录文件，如 cate.txt,每一行为目录的标题

- 准备好文本文件，存放与一个目录中，如documents，每个文件的文件名为目录中的标题名，后缀为.txt

- buildEpub.py cate.txt documents 或 运行testBuild.sh，会在当前目录下创建一个测试的epub电子书
