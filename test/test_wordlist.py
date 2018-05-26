import os
import pytest
from potypo.check import Check

@pytest.mark.parametrize("lang, use_wl_dir, po_path, result", [
    ("de", True, "test/data/de/LC_MESSAGES/django.po", "test/data/wordlists/de.txt"),
    ("de", False, "test/data/de/LC_MESSAGES/django.po", None),
    ("en", True, "test/data", "test/data/wordlist.txt"),
    ("en", False, "test/data", "test/data/wordlist.txt"),
    ("fr", True, "test/data/fr/LC_MESSAGES/django.po", "test/data/fr/LC_MESSAGES/wordlist.txt"),
    ("fr", False, "test/data/fr/LC_MESSAGES/django.po", "test/data/fr/LC_MESSAGES/wordlist.txt"),
    ("it", True, "test/data/it/LC_MESSAGES/django.po", "test/data/it/wordlist.txt"),
    ("it", False, "test/data/it/LC_MESSAGES/django.po", "test/data/it/wordlist.txt"),
])

def test_wordlist(lang, use_wl_dir, po_path, result):
    wl_dir = "test/data/wordlists" if use_wl_dir else None

    get = Check.get_wordlist(lang, wl_dir, po_path)
    gotten = os.path.abspath(get) if get is not None else None

    expected = os.path.abspath(result) if result is not None else None

    assert gotten == expected
