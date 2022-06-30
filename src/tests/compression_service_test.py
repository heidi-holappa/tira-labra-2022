import unittest
import pytest
import glob
import os
from config import DEFAULT_TEST_DATA_PATH
from services.compressionmanagement import default_compression_management


class TestCompressionManagement(unittest.TestCase):

    def setUp(self):
        self.compression_management = default_compression_management

    def test_data_compression_method_is_run_successfully(self):
        filename = "file.txt"
        compressed_filename = filename[:-3] + "huf"
        with open(filename, "w") as file:
            file.write("This is test content")
        self.compression_management.activate_huffman_compression(filename)
        compressed_file_created = bool(os.path.exists(compressed_filename))
        os.remove(filename)
        os.remove(compressed_filename)
        self.assertEqual(True, compressed_file_created)

    def test_validation_success_when_extension_is_valid(self):
        extension = "txt"
        accepted_extensions = "log;txt;md"
        return_value = self.compression_management.validate_file_extension(
            extension, accepted_extensions)
        self.assertEqual(True, return_value)

    def test_validation_failes_when_extension_is_not_valid(self):
        extension = "dxd"
        accepted_extensions = "log;txt;md"
        return_value = self.compression_management.validate_file_extension(
            extension, accepted_extensions)
        self.assertEqual(False, return_value)

    # @pytest.mark.extendedtest

    def content_validation_fails_if_file_has_one_unique_character(self):
        content = str("AAAAAAAAAAAAAAAAAAAAAAAAA")
        filename = "test_content_validation.txt"
        file_and_path = os.path.join(DEFAULT_TEST_DATA_PATH, filename)
        with open(file_and_path, "a", encoding="utf-8") as file:
            file.write(content)
        result = self.compression_management.validate_file_length_and_content(
            file_and_path)
        for filename in glob.glob(os.path.join(DEFAULT_TEST_DATA_PATH, "test_unsupported_characters*.*")):
            os.remove(filename)
        self.assertEqual(False, result)

    @pytest.mark.extendedtest
    def test_content_validation_fails_if_file_has_less_than_ten_characters(self):
        content = str("ABCDEF")
        filename = "test_content_validation.txt"
        file_and_path = os.path.join(DEFAULT_TEST_DATA_PATH, filename)
        with open(file_and_path, "a", encoding="utf-8") as file:
            file.write(content)
        result = self.compression_management.validate_file_length_and_content(
            file_and_path)
        for filename in glob.glob(os.path.join(DEFAULT_TEST_DATA_PATH, "test_content_validation*.*")):
            os.remove(filename)
        self.assertEqual(False, result)

    @pytest.mark.extendedtest
    def test_content_validation_succeeds_when_more_than_two_unique_chars_and_ten_characters(self):
        content = str("AAAAAAAAAAAAAAAAAAAAAAABC")
        filename = "test_content_validation.txt"
        file_and_path = os.path.join(DEFAULT_TEST_DATA_PATH, filename)
        with open(file_and_path, "a", encoding="utf-8") as file:
            file.write(content)
        result = self.compression_management.validate_file_length_and_content(
            file_and_path)
        for filename in glob.glob(os.path.join(DEFAULT_TEST_DATA_PATH, "test_content_validation*.*")):
            os.remove(filename)
        self.assertEqual(True, result)

    @pytest.mark.extendedtest
    def test_validation_fails_if_content_has_unsupported_characters(self):
        content = str(chr(29) + chr(30) + chr(31) + "ABC")
        filename = "test_unsupported_characters.txt"
        file_and_path = os.path.join(DEFAULT_TEST_DATA_PATH, filename)
        with open(file_and_path, "a", encoding="utf-8") as file:
            file.write(content)
        result, invalid_characters = self.compression_management.validate_uploaded_txt_file_content(
            file_and_path)
        for filename in glob.glob(os.path.join(DEFAULT_TEST_DATA_PATH, "test_unsupported_characters*.*")):
            os.remove(filename)
        self.assertFalse(result)

    @pytest.mark.extendedtest
    def test_correct_amount_of_unsupported_characters_is_returned(self):
        content = str(chr(28) + chr(29) + chr(31) + "ABC")
        filename = "test_unsupported_characters.txt"
        file_and_path = os.path.join(DEFAULT_TEST_DATA_PATH, filename)
        with open(file_and_path, "a", encoding="utf-8") as file:
            file.write(content)
        result, invalid_characters = self.compression_management.validate_uploaded_txt_file_content(
            file_and_path)
        for filename in glob.glob(os.path.join(DEFAULT_TEST_DATA_PATH, "test_unsupported_characters*.*")):
            os.remove(filename)
        self.assertTrue(3, len(invalid_characters))
