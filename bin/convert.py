#!/usr/bin/env python

import sys
import subprocess as sb
import os.path

if len(sys.argv) != 2:
	print("USAGE: ./convert.py input.ipynb")
	sys.exit(0)

filename = sys.argv[1]
if filename.split(".")[-1] != "ipynb":
	print("ERROR: input file must be *.ipynb")
	sys.exit(0)

FILEROOT = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.abspath(filename)
basename = filename.split(".")[0]

command = "jupyter-nbconvert --to slides {} --reveal-prefix '//cdn.bootcss.com/reveal.js/3.2.0' --output {} --template={}".format(input_file, basename, os.path.join("./bin", "slides_reveal.tpl"))
print("CL: " + command)
sb.call(command, shell=True)

rename = "mv {}.slides.html {}.html".format(basename, basename)
print("CL: " + rename)
sb.call(rename, shell=True)
