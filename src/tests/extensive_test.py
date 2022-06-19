import unittest
import os
import string
from config import DEFAULT_TEST_DATA_PATH
from config import HTML_LOG, CSV_LOG, ARCHIVE_LOG, TKINTER_LOG
from services.compressionmanagement import default_compression_management
from services.extensivetesthandler import default_test_handler


class TestExtensiveTesting(unittest.TestCase):

    def setUp(self):
        self.compression_management = default_compression_management
        self.extensive_test_handler = default_test_handler

    def tearDown(self):
        self.destroy_test_files()

    def supported_characters(self):
        characters = string.printable.split()[0]
        ascii_order_set = set()
        for char in characters:
            ascii_order_set.add(ord(char))
        ascii_order_set.add(32)
        ascii_order_set.add(10)
        ascii_order_set.add(228)  # ä
        ascii_order_set.add(196)  # Ä
        ascii_order_set.add(197)  # Å
        ascii_order_set.add(229)  # å
        ascii_order_set.add(246)  # ö
        ascii_order_set.add(214)  # Ö
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
        self.extensive_test_handler.create_document_with_random_printable_ascii(
            101)
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
        is_valid = self.extensive_test_handler.validate_content_matches(
            content_one, content_two)
        self.assertEqual(True, is_valid)

    def test_content_validation_fails_when_contents_do_not_match(self):
        content_one = "AAABCDEFGHIJKLMN"
        content_two = content_one + "O"
        is_valid = self.extensive_test_handler.validate_content_matches(
            content_one, content_two)
        self.assertEqual(False, is_valid)

    def test_activated_extensive_tests_create_an_html_log(self):
        self.extensive_test_handler.activate_extensive_tests(1, 10000)
        filepath = os.path.join(DEFAULT_TEST_DATA_PATH, HTML_LOG)
        result = os.path.exists(filepath)
        self.assertEqual(result, True)


    def destroy_test_files(self):
        html_path = os.path.join(DEFAULT_TEST_DATA_PATH, HTML_LOG)
        csv_path = os.path.join(DEFAULT_TEST_DATA_PATH, CSV_LOG)
        archive_path = os.path.join(DEFAULT_TEST_DATA_PATH, ARCHIVE_LOG)
        tkinter_log_path = os.path.join(DEFAULT_TEST_DATA_PATH, TKINTER_LOG)
        if os.path.exists(html_path):
            os.remove(html_path)
        if os.path.exists(archive_path):
            os.remove(archive_path)
        if os.path.exists(csv_path):
            os.remove(csv_path)
        if os.path.exists(tkinter_log_path):
            os.remove(tkinter_log_path)

