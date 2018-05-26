import os, sys
import configparser
from shutil import rmtree

from . import chunkers
from . import filters
from .check import Check
from enchant import DictWithPWL, errors
from enchant.checker import SpellChecker


def load_classes(module, config):
    classes = []
    for item in config.split(','):
        item = item.strip()
        if '.' in item:
            components = item.rsplit('.', 1)
            mod = __import__(components[0], fromlist=[components[1]])
            class_object = getattr(mod, components[1])
        else:
            class_object = getattr(module, item)

        classes.append(class_object)
    return classes


def main():
    config = configparser.ConfigParser()
    config.read(['setup.cfg', 'tox.ini'])
    conf = config['potypo']

    if 'locales_dir' not in conf:
        print("No locales_dir specified. Aborting."
        sys.exit(1)

    if 'default_language' not in conf:
        print("No default_language specified. Aborting."
        sys.exit(1)

    chunker_list = load_classes(chunkers, conf.get('chunkers', ''))
    filter_list = load_classes(filters, conf.get('filters', ''))

    if 'phrases' in conf:
        phrases = conf['phrases'].strip().split('\n')
        chunker_list.append(chunkers.make_PhraseChunker(phrases))

    if 'edgecase_words' in conf:
        words = conf['edgecase_words'].strip().split('\n')
        filter_list.append(filters.make_EdgecaseFilter(words))

    def errmsg(path, linenum, word):
        print("ERROR: {}:{}: {}".format(path, linenum, word))

    wl_dir = conf.get('wl_dir', None)

    # checks contains one Check-Object for every po-file
    checks = []

    for root, dirs, files in os.walk(conf['locales_dir']):
        for f in files:
            if f.endswith(".po"):
                try:
                    checks.append(Check(os.path.join(root, f), wl_dir, chunker_list, filter_list))
                except errors.DictNotFoundError as err:
                    print(err, "Potypo will not check for spelling errors in this language.")

    en_wordlist = Check.get_wordlist(conf['default_language'], wl_dir, conf['locales_dir'])
    en_dict = DictWithPWL(conf['default_language'], pwl=en_wordlist)
    en_ckr = SpellChecker(en_dict, chunkers=chunker_list, filters=filter_list)

    fail = False # used for tracking whether failing errors occurred
    for c in checks:
        print("Checking Errors in file", c.popath, "for lang", c.lang)
        for entry in c.po:
            if entry.obsolete:
                continue

            en_ckr.set_text(entry.msgid)
            for err in en_ckr:
                fail = True
                path = os.path.relpath(c.popath, start=config['potypo']['locales_dir'])
                errmsg(path, entry.linenum, err.word)

            c.checker.set_text(entry.msgstr)
            for err in c.checker:
                if c.lang not in conf.get('no_fail', []):
                    fail = True
                path = os.path.relpath(c.popath, start=config['potypo']['locales_dir'])
                errmsg(path, entry.linenum, err.word)

    print("Spell-checking done.")

    if fail:
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()
