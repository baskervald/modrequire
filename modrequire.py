from sys import argv
import re
import os.path

pattern = re.compile('(?:require(?:\(|\ )(?:\"|\'))(.+)(?:\"|\')(?:\))?')
basedir = os.path.dirname(os.path.realpath(argv[1]))
requires = {}

def parsefile(path, outfile):
    with open(path, 'r') as infile:
        text = infile.read()
        matches = pattern.findall(text)
        return (text, matches)

def handlematches(matches, outfile):
    for match in matches:
        if not match in requires:
            path = match.split('.')
            path[-1] = path[-1] + '.lua'
            text, reqs = parsefile(os.path.join(basedir, *path), outfile)
            requires[match] = text
            handlematches(reqs, outfile)

def createfunctions(reqs, outfile):
    outfile.write('__modrequire_functions={}\n')
    for req in reqs:
        outfile.write('__modrequire_functions["' + req + '"]=function()\n' + reqs[req] + '\nend\n')


with open(argv[2], 'w+') as outfile:
    text, matches = parsefile(argv[1], outfile)
    handlematches(matches, outfile)
    createfunctions(requires, outfile)
    outfile.write('__modrequire_modules={} function require(req) if __modrequire_modules[req] == nil then __modrequire_modules[req] = __modrequire_functions[req]() end return __modrequire_modules[req] end\n')
    outfile.write(text)
