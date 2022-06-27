from heapq import heapify, heappush, heappop
from statistics import variance
import time
from entities.logentry import LogEntry
from services.filemanagement import default_file_manager


class HuffmanCoding:

    """Constructor for the class. The constructor contains more
    than Pylint's recommended amount of instance-attributes.
    With the permission of the course assistant this pylint
    notification (R0902) has been disabled.
    """

    # pylint: disable=too-many-instance-attributes
    def __init__(self,
                 uncompressed_filename,
                 compressed_filename,
                 logentry: LogEntry = LogEntry()):
        self.uncompressed_filename = uncompressed_filename
        self.compressed_filename = compressed_filename
        self.content = ""
        self.compressed = ""
        self.uncompressed = ""
        self.frequencies = {}
        self.huffman_coded_values = {}
        self.root_node = HuffmanNode("aa", 0)
        self.logentry = logentry
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
        their representation as is their order in ASCII 256 code.
        """
        for i in enumerate(self.content):
            current = ord(self.content[i[0]])
            if current not in self.frequencies:
                self.frequencies[current] = 0
            self.frequencies[current] += 1

    def build_huffman_tree(self):
        """A method for building the Huffman tree.

        First another method is called that creates the nodes for the tree
        and returns a minimum heap of tuples (a heapifyed list). Each tuple
        contains a frequency value and a node. The frequency value is used
        to order the nodes into ascending order.

        After this a new node is created that has the two nodes with the smallest
        frequencies as child nodes. The popped node with a lower frequency is
        placed as the left child and the one with higher frequency as the right
        child. The frequency of the created parent node is the sum of the
        frequencies of the child nodes. After these steps the new parent node
        is pushed into the heap.

        Once the tree is created another method is called to collect the Huffman
        coded values for each character.
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

        content_as_list = []

        content_as_list.append(f"{bin(tree_length)[2:].zfill(12)}")
        content_as_list.append(f"{bin(extra_bits_needed)[2:].zfill(4)}")
        content_as_list.append(f"{bin(n_of_characters)[2:].zfill(8)}")
        content_as_list.append(huffman_tree)
        content_as_list.append(characters)
        content_as_list.append(encoded_content)
        content_as_list.append("0" * extra_bits_needed)
        self.compressed = "".join(content_as_list)

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
        uncompressed_as_list, node, i = self._init_huffman_decode()

        while i < len(self.compressed):
            bit = self.compressed[i]
            if bit == "1" and node.right_child:
                node = node.right_child
                if i == len(self.compressed) - 1:
                    uncompressed_as_list.append(chr(node.character))
                i += 1
            elif bit == "0" and node.left_child:
                node = node.left_child
                if i == len(self.compressed) - 1:
                    uncompressed_as_list.append(chr(node.character))
                i += 1
            else:
                uncompressed_as_list.append(chr(node.character))
                node = self.root_node
        self.uncompressed = "".join(uncompressed_as_list)
        self.content = uncompressed_as_list

    def _init_huffman_decode(self) -> tuple:
        self.uncompressed = ""
        initialized_list = []
        node = self.root_node
        i = 0
        return initialized_list, node, i

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

    def fetch_compressed_content(self):
        """Method responsible for processing the stored content. Logic is as follows:
        Length of the stored tree: 12 bits
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

    # TODO: At the moment a copy of a string object is created with each recursive step.
    def decompress_huffman_tree(self, node, tree: str, characters: str):
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
        return None

    def log_add_frequencies(self):
        freqs = []
        for freq in self.huffman_coded_values.values():
            freqs.append(len(freq))
        self.logentry.logdata["huffman_max_frequency"] = str(max(freqs))
        self.logentry.logdata["huffman_min_frequency"] = str(min(freqs))
        self.logentry.logdata["huffman_freq_variance"] = f"{(variance(freqs)):.2f}"

    def log_add_character_count(self):
        self.logentry.logdata["huffman-character-count"] = str(len(self.frequencies))

    def analyze_compression(self):
        """Creates analysis data on Huffman compression.
        """

        self.logentry.logdata["original_filename"] = self.uncompressed_filename.split(
            "/")[-1]
        self.logentry.logdata["compressed_filename"] = self.compressed_filename.split(
            "/")[-1]
        self.logentry.logdata["compression_method"] = "Huffman coding"
        self.logentry.logdata["action"] = "0"
        self.log_add_frequencies()
        self.log_add_character_count()

    # pylint: disable=duplicate-code
    def analyze_uncompression(self):
        """A method for creating analysis data on Huffman uncompression.
        Note that compressed content length is included in the data in the method
        that fetches content from a compressed file.
        """

        self.logentry.logdata["compressed_filename"] = self.compressed_filename.split(
            "/")[-1]
        self.logentry.logdata["uncompressed_filename"] = self.uncompressed_filename.split(
            "/")[-1]
        self.logentry.logdata["compression_method"] = "Huffman coding"
        self.logentry.logdata["action"] = "1"

    def execute_compression(self):
        """This method calls the methods that handle different
        phases of compressing the wanted string.

        Step 1: Fetch content to be compressed
        Step 2: Calculate frequencies for characters in the given content.
        Step 3: Create nodes and huffman tree
        Step 4: compress
        Step 5: write content to file
        """

        starttime = time.time()
        self.fetch_uncompressed_content()
        endtime = time.time()
        fetch_total_time = endtime - starttime
        self.logentry.logdata["data_fetch_and_process_time"] = f"{fetch_total_time:.2f}"

        compress_starttime = time.time()

        self.calculate_frequencies()
        self.build_huffman_tree()
        self.huffman_encode()

        compress_endtime = time.time()
        compress_total_time = compress_endtime - compress_starttime
        self.logentry.logdata["compression_time"] = f"{compress_total_time:.2f}"

        write_starttime = time.time()
        self.write_compressed_file(self.compressed_filename, self.compressed)
        write_endtime = time.time()
        write_total_time = write_endtime - write_starttime
        self.logentry.logdata["data_write_and_process_time"] = f"{write_total_time:.2f}"

    def execute_uncompression(self):
        """This method handles the uncompression of a given content

        Step 1: Fetch content from the file
        Step 2: Create a huffman tree
        Step 3: Decode content
        Step 4: Write content to file
        """

        starttime = time.time()
        self.fetch_compressed_content()
        endtime = time.time()
        fetch_total_time = endtime - starttime
        self.logentry.logdata["data_fetch_and_process_time"] = f"{fetch_total_time:.2f}"

        uncompress_starttime = time.time()
        self.huffman_decode()
        uncompress_endtime = time.time()
        uncompress_total_time = uncompress_endtime - uncompress_starttime
        self.logentry.logdata["compression_time"] = f"{uncompress_total_time:.2f}"

        write_starttime = time.time()
        self.write_uncompressed_file(
            self.uncompressed_filename, self.uncompressed)
        write_endtime = time.time()
        write_total_time = write_endtime - write_starttime
        self.logentry.logdata["data_write_and_process_time"] = f"{write_total_time:.2f}"

    def activate_preorder_traversal(self):
        """A method used by automated tests to verify that the Huffman tree
        is correctly re-created

        Returns:
            str, str: returns character order and travel path
        """
        result = []
        travel_path = []
        self.preorder_traversal(self.root_node, result, travel_path)
        list_result = []
        for char in result:
            list_result.append(char)
        str_result = "".join(list_result)
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
