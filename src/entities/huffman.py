from heapq import heapify, heappush, heappop
import time
from services.filemanagement import default_file_manager
from services.loghandler import LogHandler


class HuffmanCoding:

    """Constructor for the class
    """

    def __init__(self, uncompressed_filename, compressed_filename):
        self.uncompressed_filename = uncompressed_filename
        self.compressed_filename = compressed_filename
        self.content = ""
        self.compressed = ""
        self.uncompressed = ""
        self.frequencies = {}
        self.huffman_coded_values = {}
        self.root_node = HuffmanNode("aa", 0)
        self.loghandler = LogHandler()
        self.last_analysis = {
            "algorithm_used": "Huffman coding",
            "uncompressed_size": 0,
            "compressed_content": 0,
            "compressed_header": 0,
            "compressed_total": 0,
            "content_ratio": 0,
            "total_ratio": 0}
        self.file_manager = default_file_manager

    def calculate_frequencies(self):
        """This method calculates the frequencies of all characters included
        in the given content.

        Note that the keys for the dictionary are ord-forms of characters, meaning
        their representation as is their order in ascii 256 code.
        """
        for i in range(len(self.content)):
            current = ord(self.content[i])
            if current not in self.frequencies:
                self.frequencies[current] = 0
            self.frequencies[current] += 1

    def build_huffman_tree(self):
        """A method for building the Huffman tree.
        First another method is called that creates the nodes
        for the tree. The method return a list of nodes.

        Then the tree is created following the Huffman method.
        """
        nodes = self.create_huffman_nodes()

        while len(nodes) > 1:
            left_child = heappop(nodes)
            right_child = heappop(nodes)

            left_node = left_child[1]
            right_node = right_child[1]

            left_node.huffman_code = "0"
            right_node.huffman_code = "1"

            parent_node = HuffmanNode("",
                                      left_node.frequency + right_node.frequency,
                                      left_node,
                                      right_node)
            heappush(nodes, (parent_node.frequency, parent_node))
        self.root_node = heappop(nodes)[1]
        self.collect_huffman_coded_values(self.root_node)

    def collect_huffman_coded_values(self, node, code_value=""):
        """Once the Huffman tree is created, the Huffman codes for
        all characters can be created. This method traverses the huffman tree
        until all leafs have been found.

        Args:
            node (HuffmanNode): the node under inspection
            code_value (str, optional): current huffman code value created so far
            while traversing the tree.
        """
        updated_value = code_value + node.huffman_code
        if node.left_child:
            self.collect_huffman_coded_values(node.left_child, updated_value)
        if node.right_child:
            self.collect_huffman_coded_values(node.right_child, updated_value)
        if not node.left_child and not node.right_child:
            self.huffman_coded_values[node.character] = updated_value

    def create_huffman_nodes(self):
        """This metdod creates the nodes for the Huffman tree.

        Returns:
            list: A list of Node objects to be inserted into the Huffman tree.
        """
        nodes = []
        heapify(nodes)
        for key, value in self.frequencies.items():
            heappush(nodes, (value, HuffmanNode(key, value)))

        return nodes

    def huffman_encode(self):
        """This method write the compressed content by replacing all
        characters in original content with huffman coded values.
        """

        huffman_tree, characters = self.storable_huffman_tree(self.root_node)
        tree_length = len(huffman_tree)
        characters_length = len(characters)
        n_of_characters = int(characters_length / 8)

        encoded_content = ""

        for char in self.content:
            encoded_content += self.huffman_coded_values[ord(char)]

        content_length = len(encoded_content)

        bits = 12 + 4 + tree_length + characters_length + content_length
        extra_bits_needed = 8 - bits % 8

        self.compressed += f"{bin(tree_length)[2:].zfill(12)}"
        self.compressed += f"{bin(extra_bits_needed)[2:].zfill(4)}"
        self.compressed += f"{bin(n_of_characters)[2:].zfill(8)}"
        self.compressed += huffman_tree
        self.compressed += characters
        self.compressed += encoded_content
        self.compressed += "0" * extra_bits_needed

    def storable_huffman_tree(self,
                              node,
                              tree_string: str = "",
                              tree_characters: str = ""):
        """Creates a storable version of the Huffman tree. The logic is that
        'traveling' to the left is 0 and 'traveling' to the right is 1.
        The tree is written in the following way:
        1) Travel left as many times as possible
        2) Travel right at the nearest possible location
        3) Continue steps 1 and 2.

        Args:
            node (HuffmanNode): Node currently under inspection
            tree_string (str, optional): Stored tree. Defaults to "".
            tree_characters (str, optional): Stored characters as bytes. Defaults to "".

        Returns:
            str, str: currently returns two strings.
        """
        if not node.left_child and not node.right_child:
            tree_characters += f"{bin(node.character)[2:].zfill(8)}"
        if node.left_child:
            tree_string += "0"
            tree_string, tree_characters = self.storable_huffman_tree(
                node.left_child,
                tree_string,
                tree_characters)
        if node.right_child:
            tree_string += "1"
            tree_string, tree_characters = self.storable_huffman_tree(
                node.right_child,
                tree_string,
                tree_characters)
        return tree_string, tree_characters

    def huffman_decode(self):
        """This method decodes a content compressed in huffman code.
        The huffman tree is traversed based on the bit information
        left (if 0) or right (if 1) until a leaf node is found. Then
        the character from that node is added to the uncompressed string.
        """
        self.uncompressed = ""
        node = self.root_node
        i = 0

        stdout = []
        travelpath = ""
        while i < len(self.compressed):
            bit = self.compressed[i]
            if bit == "1" and node.right_child:
                node = node.right_child
                if i == len(self.compressed) - 1:
                    self.uncompressed += chr(node.character)
                    stdout.append(node.character)
                travelpath += "1"
                i += 1
            elif bit == "0" and node.left_child:
                node = node.left_child
                if i == len(self.compressed) - 1:
                    self.uncompressed += chr(node.character)
                    stdout.append(node.character)
                travelpath += "0"
                i += 1
            else:
                self.uncompressed += chr(node.character)
                stdout.append(node.character)
                node = self.root_node
        self.content = self.uncompressed

    def write_compressed_file(self, filename, content):
        """Converts content into a bytearray and calls an instance
        of FileManagement from Service package to store content as
        bytes. 
        """
        content_as_integers = []
        for i in range(0, len(content), 8):
            content_as_integers.append(int(content[i:i+8], 2))
        byte_array = bytearray(content_as_integers)
        self.file_manager.create_binary_file(filename, byte_array)

    def write_uncompressed_file(self, filename, content):
        """This method writes the compressed data into a file.

        At initial stage the filename is set. Later on, it will be created
        based on the file opened for compression.
        """
        with open(filename, "w", encoding="utf-8") as compressed_file:
            compressed_file.write(content)

    def fetch_uncompressed_content(self):
        """Calls a method from an instant of FileManager object from service package
        to fetch the content of a selected file.
        """
        self.content = self.file_manager.fetch_uncompressed_content(
            self.uncompressed_filename)

    def new_fetch_compressed_content(self):
        """Method responsible for processing the stored content. Logic is as follows:
        Length of the stred tree: 12 bits
        Number of extra bits: 4 bits
        Number of ASCII-characters: byte
        Tree
        Characters
        Content
        Extra bits
        """
        compressed_content = ""
        byte_data = self.file_manager.fetch_compressed_content(
            self.compressed_filename)
        for byte in byte_data:
            compressed_content += str(bin(byte)[2:].zfill(8))

        tree_length = int(compressed_content[:12], 2)
        extra_bits = int(compressed_content[12:16], 2)
        n_of_characters = int(compressed_content[16:24], 2)
        tree_end_index = 24 + tree_length
        characters_end_index = 24 + tree_length + 8 * n_of_characters
        tree = compressed_content[24: tree_end_index]
        characters = compressed_content[tree_end_index: characters_end_index]

        self.compressed = compressed_content[characters_end_index: -extra_bits]

        node = HuffmanNode(0, 0)
        self.root_node = node
        self.decompress_huffman_tree(self.root_node, tree, characters)

    # TODO: At the moment a copy of string is created with each recursion step.
    # Consider using pointers more efficiency.
    def decompress_huffman_tree(self, node, tree, characters):
        """A recursive method that handles the decompression of the Huffman tree. Logic
        is as follows:
        1) If the next character is '0', insert child nodes and traverse left and right
        2) If the next character is '1', the current node is a leaf node. Insert a character
        and return indexes of next node/vertice and next character. 

        Args:
            node (HuffmanNode): Node currently under inspection
            tree (str): the structure of the tree
            characters (str): string of characters as string of binary-type content

        Returns:
            int, int: indexes of tree and character location
        """
        if len(tree) == 0:
            character = int(characters[:8], 2)
            node.character = character
            return "", ""
        if tree[0] == "0":
            left_child = HuffmanNode(0, 0)
            node.left_child = left_child
            tree, characters = self.decompress_huffman_tree(
                left_child,
                tree[1:],
                characters)
            right_child = HuffmanNode(0, 0)
            node.right_child = right_child
            tree, characters = self.decompress_huffman_tree(
                right_child,
                tree[1:],
                characters)
            return tree, characters
        if len(characters):
            node.character = int(characters[:8], 2)
            return tree, characters[8:]

    def analyze_compression(self):
        """An initial method for creating analysis data on compression.
        """

        self.loghandler.logdata["original_filename"] = self.uncompressed_filename
        self.loghandler.logdata["compressed_filename"] = self.compressed_filename
        self.loghandler.logdata["compression_method"] = "Huffman coding"
        self.loghandler.logdata["uncompressed_size"] = len(self.content) * 8
        self.loghandler.logdata["compressed_size"] = len(self.compressed)
        self.loghandler.create_compression_entry()

    def execute_compression(self):
        """This method calls the methods that handle different
        phases of compressing the wanted string.

        Step 1: Fetch content to be compressed
        Step 2: Calculate frequencies for characters in the given content.
        Step 3: Create nodes and huffman tree
        Step 4: compress
        Step 5: write content to file
        """

        self.fetch_uncompressed_content()

        starttime = time.time()

        self.calculate_frequencies()
        self.build_huffman_tree()
        self.huffman_encode()

        endtime = time.time()
        total_time = endtime - starttime
        self.loghandler.logdata["compression_time"] = f"{total_time:.2f}"

        self.write_compressed_file(self.compressed_filename, self.compressed)

        longest_value = 0
        for key, value in self.huffman_coded_values.items():
            if len(value) > longest_value:
                longest_value = len(value)

    def execute_uncompression(self):
        """This method handles the uncompression of a given content

        Step 1: Fetch content from the file
        Step 2: Create a huffman tree
        Step 3: Decode content
        Step 4: Write content to file
        """

        self.new_fetch_compressed_content()

        self.huffman_decode()
        self.write_uncompressed_file(
            self.uncompressed_filename, self.uncompressed)

    def activate_preorder_traversal(self):
        """A method used by automated tests to verify that the Huffman tree
        is correctly re-created

        Returns:
            str, str: returns character order and travel path
        """
        result = []
        travel_path = []
        self.preorder_traversal(self.root_node, result, travel_path)
        str_result = ""
        for char in result:
            str_result += char
        str_travel_path = ""
        for vertice in travel_path:
            str_travel_path += str(vertice)
        return str_result, str_travel_path

    def preorder_traversal(self, node, result: list, travel_path: list):
        """A recursive method that travels the tree in pre-order. 

        Args:
            node (HuffmanNode): Node currently under inspection
            result (list): a reference to list collecting return values
            travel_path (list): a reference to a list collecting travel path values.
        """
        if not node.left_child and not node.right_child:
            result.append(chr(node.character))
        if node.left_child:
            travel_path.append(0)
            self.preorder_traversal(node.left_child, result, travel_path)
        if node.right_child:
            travel_path.append(1)
            self.preorder_traversal(node.right_child, result, travel_path)


class HuffmanNode:

    def __init__(self, character, frequency: int, left=None, right=None):
        """Constructor for the class.

        Node has two chilren and a Huffman code variable used
        to create the Huffman code value when traversin the tree.

        Args:
            character (str): a unique string symbol present in the content to be compressed
            frequency (int): number of occations the symbol is in the content
        """

        self.character = character
        self.frequency = frequency
        self.left_child = left
        self.right_child = right
        self.huffman_code = ""

    def __lt__(self, other_node):
        """__lt__ is a special method for less than operator between
        instances of the same object.

        Args:
            other_node (HuffmanNode): the other instance of HuffmanNode

        Returns:
            boolean: Is the frequency of this instance less than
        """
        return (self.frequency, other_node.frequency)

    def __str__(self):
        """__str__ is a special method for return a string representation of
        the instance of the object.

        Returns:
            str: returns a pre-defined string form.
        """
        return "Character: " + str(self.character) + ", frequency: " + str(self.frequency)


if __name__ == "__main__":
    pass
