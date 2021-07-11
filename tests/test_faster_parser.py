#!/usr/bin/env python

"""Tests for `faster_parser` package."""


import unittest

from faster_parser import faster_parser
import random
import time

class TestParser:
    def parse_data(self,  list_item_to_parse):
        time.sleep(1)
        return list_item_to_parse * 2

    def parse_dict_data(self,  dict_item, **kwargs):
        time.sleep(1)
        print(kwargs)
        return dict_item.get(dict_item.keys[0]) * 2


class TestFaster_parser(unittest.TestCase):
    """Tests for `faster_parser` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_list_parse(self):
        list_data = random.sample(range(1, 50000), 2)
        tp = TestParser()
        faster_parser.fast_parse(tp, 'parse_list_data', list_data)

    def test_001_dict_parse(self):
        dict_data = {"abc": "def", "GEF": "ASD"}
        tp = TestParser()
        faster_parser.fast_parse(tp, 'parse_data', dict_data)

