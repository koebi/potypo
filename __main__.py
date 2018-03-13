import os
import configparser
from shutil import rmtree

from .chunkers import make_PhraseChunker
from .filters import PythonFormatFilter, make_EdgecaseFilter, HTMLFilter
from .check import Check
from enchant import DictWithPWL
from enchant.checker import SpellChecker
from enchant.tokenize import HTMLChunker, URLFilter

# TODO: aus config-file lesen
# TODO: packaging
# TODO: gh + README
# TODO: alle .po-files finden
# TODO: tests schreiben
# TODO: bei typo: exit 1

config = configparser.ConfigParser()
config.read('/home/koebi/github/potypo/potypo/setup.cfg')

def errmsg(outputfile, path, linenum, word):
    print("ERROR: {}:{}: {}".format(path, linenum, word))
    outputfile.write("ERROR: {}:{}: {}\n".format(path, linenum, word))

try:
    print('Creating build directory at', config['potypo']['build_dir'])
    os.mkdir(config['potypo']['build_dir'])
except FileExistsError:
    print("File or directory", config['potypo']['build_dir'], "already exists, deleting")
    rmtree(config['potypo']['build_dir'])
    print('Recreating build directory')
    os.mkdir(config['potypo']['build_dir'])
    print('Build directory created')

# checks contains one Check-Object for every po-file
checks = []

for root, dirs, files in os.walk(config['potypo']['locales_dir']):
    for f in files:
        if f.endswith(".po"):
            checks.append(Check(os.path.join(root, f), config['potypo']['build_dir'], config['potypo']['ignores_dir'], config['potypo']['chunkers'], config['potypo']['filters']))

en_dict = DictWithPWL(config['potypo']['default_language'], pwl='./ignore_en.txt')
en_ckr = spellchecker(en_dict, chunkers=config['potypo']['chunkers'], filters=config['potypo']['filters'])
output_file = open(os.path.join(config['potypo']['build_dir'], 'en_output.txt'), 'w')

for c in checks:
    for entry in c.po:
        if entry.obsolete:
            continue

        en_ckr.set_text(entry.msgid)
        for err in en_ckr:
            path = os.path.relpath(c.popath, start=config['potypo']['locales_dir'])
            errmsg(output_file, path, entry.linenum, err.word)

        c.checker.set_text(entry.msgstr)
        for err in c.checker:
            path = os.path.relpath(c.popath, start=config['potypo']['locales_dir'])
            errmsg(c.output_file, path, entry.linenum, err.word)

print("Spell-checking done. You can find the outputs in", config['potypo']['build_dir'] + "/<lang>/{js_}output")
