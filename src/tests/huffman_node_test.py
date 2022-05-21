import unittest
from entities.huffman import HuffmanNode


class TestHuffmanCompression(unittest.TestCase):

    def setUp(self):
        pass

    def test_huffman_node_comparison_works(self):
        node_one = HuffmanNode("A", 41)
        node_two = HuffmanNode("B", 42)
        comparison = bool(node_one < node_two)
        self.assertEqual(True, comparison)

    def tearDown(self):
        pass

