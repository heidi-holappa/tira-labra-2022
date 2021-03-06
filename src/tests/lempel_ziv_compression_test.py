import pytest
import unittest
import os
import random
import string
from entities.lempelziv77 import LempelZiv77
from config import DEFAULT_TEST_DATA_PATH


class TestLempelZivCompression(unittest.TestCase):

    def setUp(self):
        self.filename = "testfile.txt"
        self.compressed_filename = self.filename[:-2] + "lz"
        self.uncompressed_filename = self.filename[:-3] + "_uncompressed.txt"
        self.lz77_coder = LempelZiv77(
            self.filename, self.compressed_filename)
        self.lz77_decoder = LempelZiv77(
            self.uncompressed_filename, self.compressed_filename
        )

    def tearDown(self):
        self.destroy_test_files()

    def test_byte_to_string_transformation_works(self):
        values = [65]
        byte_array = bytearray(values)
        str_value = str(bin(values[0])[2:].zfill(8))
        self.lz77_coder.compressed_content = ""
        self.lz77_coder._transform_bytes_into_string(byte_array)
        result = self.lz77_coder.compressed_content
        self.assertEqual(result, str_value)

    def test_compression_and_decompression_work_with_a_simple_content_file(self):
        content = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.create_test_file(content)
        self.lz77_coder.lempel_ziv_activate_compression()
        uncompressed_filename = self.filename[:-4] + "_uncompressed.txt"
        self.lz77_coder.uncompressed_filename = uncompressed_filename
        self.lz77_coder.lempel_ziv_activate_uncompression()
        content_matches = True
        print("original content: ", content, ", uncompressed content: ",
              self.lz77_coder.content)
        os.remove(uncompressed_filename)
        for i in range(len(content)):
            if content[i] != self.lz77_coder.content[i]:
                content_matches = False
        self.assertEqual(True, content_matches)

    def test_create_random_ascii_and_test_uncompressed_file_matches_original(self):
        n = 5000
        characters = string.printable.split()[0]
        content = "".join([random.choice(characters) for i in range(n)])
        self.create_test_file(content)
        self.lz77_coder.lempel_ziv_activate_compression()
        uncompressed_filename = self.filename[:-4] + "_uncompressed.txt"
        self.lz77_coder.uncompressed_filename = uncompressed_filename
        self.lz77_coder.lempel_ziv_activate_uncompression()
        content_matches = True
        print("original content: ", content, ", uncompressed content: ",
              self.lz77_coder.content)
        os.remove(uncompressed_filename)
        for i in range(len(content)):
            if content[i] != self.lz77_coder.content[i]:
                content_matches = False
        self.assertEqual(True, content_matches)

    def test_compressed_data_matches_after_file_transformation(self):
        n = 10000
        characters = string.printable.split()[0]
        content = "".join([random.choice(characters) for i in range(n)])
        self.create_test_file(content)
        self.lz77_coder.lempel_ziv_activate_compression()
        content_as_list = self.lz77_coder.compressed_content_as_list
        uncompressed_filename = self.filename[:-4] + "_uncompressed.txt"
        self.lz77_coder.uncompressed_filename = uncompressed_filename
        self.lz77_coder.lempel_ziv_activate_uncompression()
        content_as_list_from_file = self.lz77_coder.compressed_content_as_list
        content_matches = True
        os.remove(uncompressed_filename)
        for i in range(len(content_as_list)):
            if content_as_list[i][2] == 0:
                value = (content_as_list[i][0], content_as_list[i][1], '')
            else:
                value = (content_as_list[i][0], content_as_list[i][1], chr(
                    content_as_list[i][2]))
            if value != content_as_list_from_file[i]:
                print(content_as_list[i], content_as_list_from_file[i])
                content_matches = False
        self.assertEqual(True, content_matches)

    def test_list_of_tuples_are_created_correctly(self):
        """For this test a correct output for the given content has been manually deducted.
        It is then compared to the output of the algorithm.
        """
        test_content = "AABCABCDABCDABCD"
        list_of_tuples_should_be = [
            (0, 1, ord("A")),
            (0, 1, ord("A")),
            (0, 1, ord("B")),
            (0, 1, ord("C")),
            (3, 3, 0),
            (0, 1, ord("D")),
            (4, 4, 0),
            (4, 4, 0),
        ]
        self.lz77_coder.content = test_content
        self.lz77_coder._lempel_ziv_compress_content()
        created_list = self.lz77_coder.compressed_content_as_list
        print(list_of_tuples_should_be, created_list)
        self.assertEqual(list_of_tuples_should_be, created_list)

    @pytest.mark.extendedtest
    def test_edge_case_content_max_match_size_is_correctly_transformed_to_tuples(self):
        """For this test a correct output for the given content has been manually deducted.
        It is then compared to the output of the algorithm.
        """
        test_content = "ABCDEFGHIJKLMNOABCDEFGHIJKLMNOABCDEFGHIJKLMNO"
        list_of_tuples_should_be = [
            (0, 1, ord("A")),
            (0, 1, ord("B")),
            (0, 1, ord("C")),
            (0, 1, ord("D")),
            (0, 1, ord("E")),
            (0, 1, ord("F")),
            (0, 1, ord("G")),
            (0, 1, ord("H")),
            (0, 1, ord("I")),
            (0, 1, ord("J")),
            (0, 1, ord("K")),
            (0, 1, ord("L")),
            (0, 1, ord("M")),
            (0, 1, ord("N")),
            (0, 1, ord("O")),
            (15, 15, 0),
            (15, 15, 0),
        ]
        self.lz77_coder.content = test_content
        self.lz77_coder._lempel_ziv_compress_content()
        created_list = self.lz77_coder.compressed_content_as_list
        print(list_of_tuples_should_be, created_list)
        self.assertEqual(list_of_tuples_should_be, created_list)

    def test_compressed_data_matches_after_file_transformation_with_separate_decoder(self):
        n = 10000
        characters = string.printable.split()[0]
        content = "".join([random.choice(characters) for i in range(n)])
        self.create_test_file(content)
        self.lz77_coder.lempel_ziv_activate_compression()
        content_as_list = self.lz77_coder.compressed_content_as_list
        self.lz77_decoder.lempel_ziv_activate_uncompression()
        content_as_list_from_file = self.lz77_coder.compressed_content_as_list
        content_matches = True
        os.remove(self.uncompressed_filename)
        for i in range(len(content_as_list)):
            if content_as_list[i] != content_as_list_from_file[i]:
                print(content_as_list[i], content_as_list_from_file[i])
                content_matches = False
        self.assertEqual(True, content_matches)

    def test_compressed_data_matches_with_an_existing_file(self):
        filename = os.path.join(DEFAULT_TEST_DATA_PATH,
                                "natural-language-document-15-paragraphs.txt")
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()
        self.create_test_file(content)
        self.lz77_coder.lempel_ziv_activate_compression()
        content_as_list = self.lz77_coder.compressed_content_as_list
        self.lz77_decoder.lempel_ziv_activate_uncompression()
        content_as_list_from_file = self.lz77_coder.compressed_content_as_list
        content_matches = True
        os.remove(self.uncompressed_filename)
        for i in range(len(content_as_list)):
            if content_as_list[i] != content_as_list_from_file[i]:
                print(content_as_list[i], content_as_list_from_file[i])
                content_matches = False
        self.assertEqual(True, content_matches)

    def test_compressed_data_matches_with_a_longer_existing_file(self):
        filename = os.path.join(DEFAULT_TEST_DATA_PATH,
                                "random-printable-ascii-100-paragraphs.txt")
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()
        self.create_test_file(content)
        self.lz77_coder.lempel_ziv_activate_compression()
        content_as_list = self.lz77_coder.compressed_content_as_list
        self.lz77_decoder.lempel_ziv_activate_uncompression()
        content_as_list_from_file = self.lz77_coder.compressed_content_as_list
        content_matches = True
        os.remove(self.uncompressed_filename)
        for i in range(len(content_as_list)):
            if content_as_list[i] != content_as_list_from_file[i]:
                print(content_as_list[i], content_as_list_from_file[i])
                content_matches = False
        self.assertEqual(True, content_matches)

    @pytest.mark.extendedtest
    def test_compressed_data_matches_with_a_very_long_existing_file(self):
        filename = os.path.join(DEFAULT_TEST_DATA_PATH,
                                "gutenberg-top-10.txt")
        self.uncompressed_filename = filename[:-4] + "_uncompressed.txt"
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()
        self.create_test_file(content)
        self.lz77_coder.lempel_ziv_activate_compression()
        content_as_list = self.lz77_coder.compressed_content_as_list
        self.lz77_decoder.lempel_ziv_activate_uncompression()
        content_as_list_from_file = self.lz77_coder.compressed_content_as_list
        content_matches = True
        os.remove(self.uncompressed_filename)
        for i in range(len(content_as_list)):
            if content_as_list[i] != content_as_list_from_file[i]:
                print(content_as_list[i], content_as_list_from_file[i])
                content_matches = False
        self.assertEqual(True, content_matches)

    def create_test_file(self, content: str):
        with open(self.filename, "w") as file:
            file.write(content)

    def destroy_test_files(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)
        if os.path.exists(self.compressed_filename):
            os.remove(self.compressed_filename)
