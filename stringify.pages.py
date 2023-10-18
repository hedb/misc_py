

import re

pattern = re.compile("[^\\\]\"")


file_name = 'demo_config.html'

fi = open(file_name, "r")
fo = open(file_name + ".string", "w")

str = ""

no_free_quotes = True

for line in [line.rstrip('\n') for line in fi]:
    if (pattern.search(line) ):
        no_free_quotes = False
    str += (line + " ")

if (no_free_quotes):
    fo.write(str)
else :
    fo.write("Found \" , Please fix")

fo.close()