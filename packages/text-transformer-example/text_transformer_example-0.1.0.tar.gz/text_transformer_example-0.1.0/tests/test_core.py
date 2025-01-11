# -*- coding: utf-8 -*-

import unittest
from text_transformer_example.core import (
    remove_punctuation,
    to_uppercase,
    to_lowercase,
    split_sentences,
    word_frequency
)

class TestTextTransformer(unittest.TestCase):
    def test_remove_punctuation(self):
        self.assertEqual(remove_punctuation("Hello, World!"), "Hello World")

    def test_to_uppercase(self):
        self.assertEqual(to_uppercase("Hello, World!"), "HELLO, WORLD!")

    def test_to_lowercase(self):
        self.assertEqual(to_lowercase("Hello, World!"), "hello, world!")

    def test_split_sentences(self):
        text = "Hello world! This is a test. Are you ready?"
        expected = ["Hello world", " This is a test", " Are you ready", ""]
        self.assertEqual(split_sentences(text), expected)

    def test_word_frequency(self):
        text = "Hello world Hello"
        freq = word_frequency(text)
        self.assertEqual(freq.get("hello"), 2)
        self.assertEqual(freq.get("world"), 1)

if __name__ == '__main__':
    unittest.main()
