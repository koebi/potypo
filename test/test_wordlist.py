import os
from potypo.check import Check

def test_wldir():
    """
    The wldir is given.
    For "de", it should detect "test/data/wordlists/de.txt".
    """
    assert Check.get_wordlist("de", "test/data/wordlists", "test/data/de/LC_MESSAGES/django.po") == os.path.abspath("test/data/wordlists/de.txt")

def test_default_wordlist_file():
    """
    No wldir is given.
    For "en", it should detect "test/data/wordlist.txt".
    """
    assert Check.get_wordlist("en", "test/data/wordlists", "test/data") == os.path.abspath("test/data/wordlist.txt")


def test_language_wordlist_file():
    """
    No wldir is given.
    For "it", it should detect "test/data/it/wordlist.txt".
    """
    assert Check.get_wordlist("it", "test/data/wordlists", "test/data/it/LC_MESSAGES/django.po") == os.path.abspath("test/data/it/wordlist.txt")

    """
    No wldir is given.
    For "fr", it should detect "test/data/fr/LC_MESSAGES/wordlist.txt"
    """
    assert Check.get_wordlist("fr", "test/data/wordlists", "test/data/fr/LC_MESSAGES/django.po") == os.path.abspath("test/data/fr/LC_MESSAGES/wordlist.txt")

