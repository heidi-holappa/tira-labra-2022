import unittest
import os
import string
from entities.huffman import HuffmanCoding


class TestHuffmanCompression(unittest.TestCase):

    def setUp(self):
        self.filename = "testfile.txt"
        self.compressed_filename = self.filename[:-3] + "huf"
        self.huffman_coder = HuffmanCoding(
            self.filename, self.compressed_filename)
        pass

    def tearDown(self):
        self.destroy_test_files()

    def test_calculate_frequencies_stores_correct_values(self):
        content = "AAABBC"
        self.create_test_file(content)
        self.huffman_coder.execute_compression()
        frequencies_total = 0
        for key, value in self.huffman_coder.frequencies.items():
            frequencies_total += value
        self.assertEqual(len(self.huffman_coder.content), frequencies_total)

    def test_calculate_frequencies_ascii_number_forms_of_ascii_letters_are_correct(self):
        self.create_test_file(string.ascii_letters)
        self.huffman_coder.execute_compression()
        all_found = True
        for character in self.huffman_coder.content:
            if ord(character) not in self.huffman_coder.frequencies:
                all_found = False
        self.assertEqual(True, all_found)

    def test_calculate_frequencies_ascii_number_forms_of_all_single_character_ascii_characters_are_correct(self):
        characters = [chr(i) for i in range(128)]
        test_content = ""
        for i in range(24, len(characters)):
            test_content += characters[i]
        self.create_test_file(test_content)
        self.huffman_coder.execute_compression()
        all_found = True
        for character in test_content:
            if ord(character) not in self.huffman_coder.frequencies:
                print(character)
                all_found = False
        print(test_content)
        self.assertEqual(True, all_found)

    def test_compressed_simple_file_has_same_content_uncompressed(self):
        content = "AABBBCDDEEEEFFFGHIJKLMN"
        self.create_test_file(content)
        self.huffman_coder.execute_compression()
        uncompressed_filename = self.filename[:-4] + "_uncompressed.txt"
        self.huffman_coder.uncompressed_filename = uncompressed_filename
        self.huffman_coder.execute_uncompression()
        content_matches = True
        print("original content: ", content, ", uncompressed content: ",
              self.huffman_coder.uncompressed)
        os.remove(uncompressed_filename)
        for i in range(len(content)):
            if content[i] != self.huffman_coder.uncompressed[i]:
                content_matches = False
        self.assertEqual(True, content_matches)

    def create_test_file(self, content: str):
        with open(self.filename, "w") as file:
            file.write(content)

    def destroy_test_files(self):
        os.remove(self.filename)
        os.remove(self.compressed_filename)
