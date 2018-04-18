import os
import configparser
from shutil import rmtree

from . import chunkers
from . import filters
from .check import Check
from enchant import DictWithPWL
from enchant.checker import SpellChecker

def main():
    config = configparser.ConfigParser()
    config.read('setup.cfg')
    conf = config['potypo']

    chunker_list = []
    for chunker in conf['chunkers'].strip().split(","):
        if "." in chunker:
            components = chunker.rsplit('.',1)
            mod = __import__(components[0], fromlist=[components[1]])
            class_object = getattr(mod, components[1])
        else:
            class_object = getattr(chunkers, chunker)

        chunker_list.append(class_object)

    filter_list = []
    for f in conf['filters'].strip().split(","):
        if "." in f:
            components = f.rsplit('.',1)
            mod = __import__(components[0], fromlist=[components[1]])
            class_object = getattr(mod, components[1])
        else:
            class_object = getattr(filters, f)

        filter_list.append(class_object)

    if 'phrases' in conf:
        phrases = conf['phrases'].strip().split('\n')
        chunker_list.append(chunkers.make_PhraseChunker(phrases))

    if 'edgecase_words' in conf:
        words = conf['edgecase_words'].strip().split('\n')
        filter_list.append(filters.make_EdgecaseFilter(words))


    def errmsg(path, linenum, word):
        print("ERROR: {}:{}: {}".format(path, linenum, word))

    # checks contains one Check-Object for every po-file
    checks = []

    for root, dirs, files in os.walk(conf['locales_dir']):
        for f in files:
            if f.endswith(".po"):
                checks.append(Check(os.path.join(root, f), conf['ignores_dir'], chunker_list, filter_list))

    en_ignorefile = Check.get_ignorefile(conf['default_language'], conf['ignores_dir'])
    en_dict = DictWithPWL(conf['default_language'], pwl=en_ignorefile)
    en_ckr = SpellChecker(en_dict, chunkers=chunker_list, filters=filter_list)

    for c in checks:
        for entry in c.po:
            if entry.obsolete:
                continue

            en_ckr.set_text(entry.msgid)
            for err in en_ckr:
                path = os.path.relpath(c.popath, start=config['potypo']['locales_dir'])
                errmsg(path, entry.linenum, err.word)

            c.checker.set_text(entry.msgstr)
            for err in c.checker:
                path = os.path.relpath(c.popath, start=config['potypo']['locales_dir'])
                errmsg(path, entry.linenum, err.word)

    print("Spell-checking done.")

if __name__ == "__main__":
    main()
