import unittest
import os
import string
from config import DEFAULT_TEST_DATA_PATH
from services.compressionmanagement import default_compression_management
from services.extensivetesthandler import default_test_handler

class TestExtensiveTesting(unittest.TestCase):

    def setUp(self):
        self.compression_management = default_compression_management
        self.extensive_test_handler = default_test_handler

    def supported_characters(self):
        characters = string.printable.split()[0]
        ascii_order_set = set()
        for char in characters:
            ascii_order_set.add(ord(char))
        ascii_order_set.add(32)
        ascii_order_set.add(10)
        ascii_order_set.add(228) # ä
        ascii_order_set.add(196) # Ä
        ascii_order_set.add(197) # Å
        ascii_order_set.add(229) # å
        ascii_order_set.add(246) # ö
        ascii_order_set.add(214) # Ö
        return ascii_order_set

    
    def test_printable_characters_include_all_supported_characters(self):
        ascii_order_set = self.supported_characters()
        fetched_characters = self.extensive_test_handler.create_printable_characters()
        all_accounted_for = True
        for char in ascii_order_set:
            if char not in fetched_characters:
                all_accounted_for = False
        self.assertTrue(True, all_accounted_for)

    def test_random_natural_language_content_only_has_supported_characters(self):
        ascii_order_set = self.supported_characters()
        self.extensive_test_handler.create_document_with_natural_language(101)
        filename = "natural-language-document-101-paragraphs.txt" 
        path_and_filename = os.path.join(DEFAULT_TEST_DATA_PATH, filename)
        with open(path_and_filename, "r", encoding="utf-8") as file:
            content = file.read()
        all_characters_supported = True
        for char in content:
            if char not in ascii_order_set:
                all_characters_supported = False
        os.remove(path_and_filename)
        self.assertTrue(True, all_characters_supported)

    def test_random_printable_ascii_content_only_has_supported_characters(self):
        ascii_order_set = self.supported_characters()
        self.extensive_test_handler.create_document_with_random_printable_ascii(101)
        filename = "random-printable-ascii-101-paragraphs.txt" 
        path_and_filename = os.path.join(DEFAULT_TEST_DATA_PATH, filename)
        with open(path_and_filename, "r", encoding="utf-8") as file:
            content = file.read()
        all_characters_supported = True
        for char in content:
            if char not in ascii_order_set:
                all_characters_supported = False
        os.remove(path_and_filename)
        self.assertTrue(True, all_characters_supported)

    def test_content_validation_succeeds_when_contents_match(self):
        content_one = "AAABCDEFGHIJKLMN"
        content_two = content_one
        is_valid = self.extensive_test_handler.validate_content_matches(content_one, content_two)
        self.assertEqual(True, is_valid)


    def test_content_validation_fails_when_contents_do_not_match(self):
        content_one = "AAABCDEFGHIJKLMN"
        content_two = content_one + "O"
        is_valid = self.extensive_test_handler.validate_content_matches(content_one, content_two)
        self.assertEqual(False, is_valid)

        

        
        
