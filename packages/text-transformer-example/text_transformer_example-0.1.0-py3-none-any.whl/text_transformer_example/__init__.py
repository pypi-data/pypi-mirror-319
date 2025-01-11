# -*- coding: utf-8 -*-

"""
__init__.py

初始化包，将核心函数暴露给外部调用。
"""

from .core import (
    remove_punctuation,
    to_uppercase,
    to_lowercase,
    split_sentences,
    word_frequency
)

__all__ = [
    'remove_punctuation',
    'to_uppercase',
    'to_lowercase',
    'split_sentences',
    'word_frequency'
]
