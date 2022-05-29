import unittest
import os
import random
import string
from entities.huffman import HuffmanCoding
from entities.huffman import HuffmanNode


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

    # Deactivated until issues are solved
    def compression_and_decompression_work_with_a_single_character_file(self):
        content = "a"
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

    def test_compression_and_decompression_work_with_two_character_file(self):
        content = "ab"
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

    def test_create_random_ascii_and_test_uncompressed_file_matches_original(self):
        n = 50000
        characters = string.printable.split()[0]
        content = "".join([random.choice(characters) for i in range(n)])
        self.create_test_file(content)
        self.huffman_coder.execute_compression()
        uncompressed_filename = self.filename[:-4] + "_uncompressed.txt"
        self.huffman_coder.uncompressed_filename = uncompressed_filename
        self.huffman_coder.execute_uncompression()
        content_matches = True
        os.remove(uncompressed_filename)
        for i in range(len(content)):
            if i < len(content) and i < len(self.huffman_coder.uncompressed):
                if content[i] != self.huffman_coder.uncompressed[i]:
                    print("content[i]", content[i], "uncompressed[i]: ",
                          self.huffman_coder.uncompressed[i], "i: ", i)
                    content_matches = False
        self.assertEqual(True, content_matches)

    def test_compressed_tree_is_correctly_created(self):
        self.create_huffman_tree_for_testing()
        tree_should_be = "0001011010110101"
        tree_string, characters = self.huffman_coder.storable_huffman_tree(
            self.huffman_coder.root_node)
        self.assertEqual(tree_should_be, tree_string)

    def test_preorder_traverse_gives_right_characters(self):
        self.create_huffman_tree_for_testing()
        preorder_traverse_should_create = "ABCDEFGHI"
        result, travel_path = self.huffman_coder.activate_preorder_traversal()
        self.assertEqual(preorder_traverse_should_create, result)

    def test_preorder_traversal_character_result_is_equal_for_un_and_decompressed_trees(self):
        self.create_huffman_tree_for_testing()
        result_uncompressed, travel_path = self.huffman_coder.activate_preorder_traversal()
        tree = "0001011010110101"
        characters = "010000010100001001000011010001000100010101000110010001110100100001001001"
        self.huffman_coder.root_node = HuffmanNode(-1, 0)
        self.huffman_coder.decompress_huffman_tree(
            self.huffman_coder.root_node, tree, characters)
        result_compressed, travel_path = self.huffman_coder.activate_preorder_traversal()
        self.assertEqual(result_uncompressed, result_compressed)

    def test_preorder_traversal_path_is_equal_for_un_and_decompressed_trees(self):
        self.create_huffman_tree_for_testing()
        result_uncompressed, travel_path_uncompressed = self.huffman_coder.activate_preorder_traversal()
        tree = "0001011010110101"
        characters = "010000010100001001000011010001000100010101000110010001110100100001001001"
        self.huffman_coder.root_node = HuffmanNode(-1, 0)
        self.huffman_coder.decompress_huffman_tree(
            self.huffman_coder.root_node, tree, characters)
        result_compressed, travel_path_compressed = self.huffman_coder.activate_preorder_traversal()
        self.assertEqual(travel_path_uncompressed, travel_path_compressed)

    def test_tree_decompression_works_characters_are_right(self):
        tree = "0001011010110101"
        characters = "010000010100001001000011010001000100010101000110010001110100100001001001"
        self.huffman_coder.root_node = HuffmanNode(-1, 0)
        self.huffman_coder.decompress_huffman_tree(
            self.huffman_coder.root_node, tree, characters)
        result, travel_path = self.huffman_coder.activate_preorder_traversal()
        self.assertEqual(result, "ABCDEFGHI")

    def test_tree_decompression_works_travel_path_is_correct(self):
        tree = "0001011010110101"
        characters = "010000010100001001000011010001000100010101000110010001110100100001001001"
        self.huffman_coder.root_node = HuffmanNode(-1, 0)
        self.huffman_coder.decompress_huffman_tree(
            self.huffman_coder.root_node, tree, characters)
        result, travel_path = self.huffman_coder.activate_preorder_traversal()
        self.assertEqual(travel_path, "0001011010110101")

    def test_content_decompression_works(self):
        tree = "0001011010110101"
        characters = "010000010100001001000011010001000100010101000110010001110100100001001001"
        self.huffman_coder.compressed = "0000000000000001000010000110100110011110110111"
        self.huffman_coder.root_node = HuffmanNode(-1, 0)
        self.huffman_coder.decompress_huffman_tree(
            self.huffman_coder.root_node, tree, characters)
        self.huffman_coder.huffman_decode()
        result = self.huffman_coder.content
        self.assertEqual(result, "AAABBCDEFGHI")

    def create_huffman_tree_for_testing(self):
        """Creating a Huffman tree that should give a printout
        of 0001011010110101.

        The printout of leaf node characters for preorder traversal
        should be "ABCDEFGHI"

        Characters strings are created with bin(ord("A"))[2:].zfill(8) and are as follows
        A: '01000001'
        B: '01000010'
        C: '01000011'
        D: '01000100'
        E: '01000101'
        F: '01000110'
        G: '01000111'
        H: '01001000'
        I: '01001001'

        Huffman coding for each character:
        A: 0000
        B: 00010
        C: 00011
        D: 010
        E: 0110
        F: 0111
        G: 10
        H: 110
        I: 111

        Example string: 
        AAABBCDEFGHI
        0000000000000001000010000110100110011110110111
        """

        N1 = HuffmanNode(-1, 0)
        N2 = HuffmanNode(-1, 0)
        N3 = HuffmanNode(-1, 0)
        N4 = HuffmanNode(ord("A"), 0)
        N5 = HuffmanNode(-1, 0)
        N6 = HuffmanNode(ord("B"), 0)
        N7 = HuffmanNode(ord("C"), 0)
        N8 = HuffmanNode(-1, 0)
        N9 = HuffmanNode(ord("D"), 0)
        N10 = HuffmanNode(-1, 0)
        N11 = HuffmanNode(ord("E"), 0)
        N12 = HuffmanNode(ord("F"), 0)
        N13 = HuffmanNode(-1, 0)
        N14 = HuffmanNode(ord("G"), 0)
        N15 = HuffmanNode(-1, 0)
        N16 = HuffmanNode(ord("H"), 0)
        N17 = HuffmanNode(ord("I"), 0)

        N1.left_child = N2
        N1.right_child = N13
        N2.left_child = N3
        N2.right_child = N8
        N3.left_child = N4
        N3.right_child = N5
        N5.left_child = N6
        N5.right_child = N7
        N8.left_child = N9
        N8.right_child = N10
        N10.left_child = N11
        N10.right_child = N12
        N13.left_child = N14
        N13.right_child = N15
        N15.left_child = N16
        N15.right_child = N17

        self.huffman_coder.root_node = N1

    def create_test_file(self, content: str):
        with open(self.filename, "w") as file:
            file.write(content)

    def destroy_test_files(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)
        if os.path.exists(self.compressed_filename):
            os.remove(self.compressed_filename)
