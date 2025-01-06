"""
Some utilities written for use with/in faspellchecker
"""

import re
from typing import List

__all__ = ("is_persian_word", "ignore_non_persian_words")


def is_word_persian(word: str) -> bool:
    """
    Checks if the given word is Persian

    :param word: The word to determine if it's Persian
    :type word: str
    :return: True if the word is Persian
    :rtype: bool
    """

    # .. versionchanged:: 0.3.1
    #   Replacement for ^[آ-ی]+$ -> ^[\u0600-\u06FF\s]+$
    return re.fullmatch("^[\u0600-\u06FF\s]+$", word) is not None


def ignore_non_persian_words(words: List[str]) -> List[str]:
    """
    Removes non Persian words (or rather keeps the words which ONLY include
    Persian alphabet) from the given list then returns it!

    :param words: list of words to remove non Persian words
    :type words: List[str]
    :return: List of Persian words
    :rtype: List[str]
    """

    return [word for word in words if is_word_persian(word)]
