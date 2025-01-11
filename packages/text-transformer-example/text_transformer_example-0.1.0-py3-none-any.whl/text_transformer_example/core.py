# -*- coding: utf-8 -*-

"""
core.py

实现文本转换和统计相关功能。
"""

import string

def remove_punctuation(text):
    """
    去除文本中的标点符号。
    示例：
        输入: "Hello, World!"
        输出: "Hello World"
    """
    # string.punctuation 包含常见的标点符号: !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)

def to_uppercase(text):
    """
    将文本转换为大写。
    示例：
        输入: "Hello, World!"
        输出: "HELLO, WORLD!"
    """
    return text.upper()

def to_lowercase(text):
    """
    将文本转换为小写。
    示例：
        输入: "Hello, World!"
        输出: "hello, world!"
    """
    return text.lower()

def split_sentences(text):
    """
    简易句子分割（按 . ! ? 分割），仅作演示，可能不适合实际复杂文本。
    示例：
        输入: "Hello world! This is a test. Are you ready?"
        输出: ["Hello world", " This is a test", " Are you ready", ""]
    """
    import re
    # 按 . 或 ! 或 ? 进行分割，保留可能的空字符串
    return re.split(r'[.!?]', text)

def word_frequency(text):
    """
    统计文本中每个单词出现的频率，返回字典。
    示例：
        输入: "Hello world hello"
        输出: {"hello": 2, "world": 1}
    """
    # 去除标点并转小写
    clean_text = remove_punctuation(text).lower()
    words = clean_text.split()
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    return freq
