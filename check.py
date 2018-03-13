import os

import polib
from enchant import DictWithPWL
from enchant.checker import SpellChecker

class Check:
    """
    A Check represents a po-file and a corresponding spellchecker for the
    po-files language. It also handles the output-file and some metadata.

    :param popath: The path to the po-file
    :type popath: path
    :param po: The po-file itself
    :type po: pofile
    :param checker: The spellchecker corresponding to the po-file's language
    :type checker: SpellChecker
    :param output_file: The file to write the checks output to
    :type output_file: file
    """
    def __init__(self, path, build_dir, wl_dir, chunkers, filters):
        self.popath = path
        self.po = polib.pofile(path)
        lang = self.po.metadata["Language"]
        ignore = Check.get_ignorefile(lang, wl_dir)
        check_dict = DictWithPWL(lang, pwl=ignore)
        self.checker = SpellChecker(check_dict, chunkers=chunkers, filters=filters)
        self.set_output(lang, build_dir)

    def set_output(self, lang, build_dir):
        out_dir = os.path.join(build_dir, lang)
        os.makedirs(out_dir, exist_ok=True)
        name = 'output.txt'
        self.output_file = open(os.path.join(out_dir, name), 'a')

    @staticmethod
    def get_ignorefile(lang, wl_dir):
        for f in os.listdir(wl_dir):
            if lang == f.split(".")[0]:
                return os.path.join(wl_dir, f)  # as there should be only one language file
