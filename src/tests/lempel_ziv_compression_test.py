import unittest
import os
import random
import string
from entities.lempelziv77 import LempelZiv77


class TestLempelZivCompression(unittest.TestCase):

    def setUp(self):
        self.filename = "testfile.txt"
        self.compressed_filename = self.filename[:-2] + "lz"
        self.lz77_coder = LempelZiv77(
            self.filename, self.compressed_filename)

    def tearDown(self):
        self.destroy_test_files()

    def test_byte_to_string_transformation_works(self):
        values = [65]
        byte_array = bytearray(values)
        str_value = str(bin(values[0])[2:].zfill(8))
        self.lz77_coder.compressed_content = ""
        self.lz77_coder.tranform_bytes_into_string(byte_array)
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
        n = 50000
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

    def create_test_file(self, content: str):
        with open(self.filename, "w") as file:
            file.write(content)

    def destroy_test_files(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)
        if os.path.exists(self.compressed_filename):
            os.remove(self.compressed_filename)
