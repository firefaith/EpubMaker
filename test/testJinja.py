#!/usr/bin/env python2
# coding:utf-8
import sys
sys.path.append(r"../")
from jinja2 import Template
from lib.category import Category
from jinja2 import Environment, PackageLoader

template = Template("""                                                     
{%- for key, value in dictionary.items() recursive %}                       
  <li>{{ key }}                                                             
    {%- if value %}                                                         
      Recursive {{ key }}, {{value}}                                        
      <ul>{{ loop(value.items())}}</ul>                                     
    {%- endif %}                                                            
  </li>                                                                     
{%- endfor %}                                                               
{{ cate.title }}
{% macro printCate(cate) %}
{% if cate.hasSub %}
    <navPoint playOrder="{{ cate.id }}" class="navpoint-level-1">
      <navLabel>
        <text>{{ cate.title }}</text>
      </navLabel>
{% for c in cate.getSubCate() -%} {{ printCate(c) }} {%- endfor %}
     <content src="{{ cate.src }}"/>  <!-- {{ cate.title }} -->
    </navPoint>
{% else %}
    <navPoint playOrder="{{ cate.id }}" class="navpoint-level-1">
      <navLabel><text>{{ cate.title }}</text></navLabel>
      <content src="{{ cate.src }}"/>
    </navPoint>
{% endif %}
{% endmacro %}
{{ printCate(cate) }}
""",trim_blocks=True,lstrip_blocks=True,keep_trailing_newline=False)

# title, full path, order
# obj, list obj

cate = Category()
c1 = Category("t1")
c11 = Category("t1.1")
c111 = Category("t1.1.1")
c12 = Category("t1.2")
c12.setSrc("/c12.html")
cate.addSubCate(c1)
c1.addSubCate(c11)
c1.addSubCate(c12)
c11.addSubCate(c111)
c11.setSrc("/c11.html")
print template.render(dictionary={'a': {'b': {'c': {}}}},cate=cate)
