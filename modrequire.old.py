from sys import argv
import re
import os.path
from os import getcwd

pattern = re.compile('((?:require(?:\(|\ )(?:\"|\'))(.+)(?:\"|\')(?:\))?)')
basedir = os.path.dirname(os.path.realpath(argv[1]))

def parsefile(path, outfile):
    with open(path, 'r') as infile:
        for line in infile:
            match = pattern.search(line)
            if match is None:
                outfile.write(line)
            else:
                split = line.split(match.group(1))
                outfile.write(split[0] + '(function()\n')
                splitreq = match.group(2).split('.')
                splitreq[-1] = splitreq[-1] + '.lua'
                parsefile(os.path.join(basedir, *splitreq), outfile)
                outfile.write('\nend)() ' + split[1])


with open(argv[2], 'w+') as outfile:
    parsefile(argv[1], outfile)
