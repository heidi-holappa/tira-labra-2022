from heapq import heapify, heappush, heappop


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
        self.last_analysis = {
            "algorithm_used": "Huffman coding",
            "uncompressed_size": 0,
            "compressed_content": 0,
            "compressed_header": 0,
            "compressed_total": 0,
            "content_ratio": 0,
            "total_ratio": 0
        }

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
        self.compressed = ""
        for char in self.content:
            self.compressed += self.huffman_coded_values[ord(char)]

    def huffman_decode(self):
        """This method decodes a content compressed in huffman code.
        The huffman tree is traversed based on the bit information
        left (if 0) or right (if 1) until a leaf node is found. Then
        the character from that node is added to the uncompressed string.
        """
        self.uncompressed = ""
        node = self.root_node
        i = 0
        while i < len(self.compressed):
            byte = self.compressed[i]
            if byte == "1" and node.right_child:
                node = node.right_child
                i += 1
            elif byte == "0" and node.left_child:
                node = node.left_child
                i += 1
            else:
                self.uncompressed += chr(node.character)
                node = self.root_node
            # THIS PART NEEDS TO BE THINKED OVER. REFACTOR.
            # if i == len(self.compressed)-1:
            #     if byte == "1" and node.right_child:
            #         node = node.right_child
            #     elif byte == "0" and node.left_child:
            #         node = node.left_child
            #     else:
            #         self.uncompressed += chr(node.character)
            #         node = self.root_node
                    
        self.content = self.uncompressed

    def write_compressed_file(self, filename, content):
        """This method writes the compressed data into a file.

        At initial stage the filename is set. Later on, it will be created
        based on the file opened for compression.
        """
        with open(filename, "w", encoding="utf-8") as compressed_file:
            for key, value in self.frequencies.items():
                compressed_file.write(f"{str(key)};{value}\n")
            compressed_file.write(content)

    def write_uncompressed_file(self, filename, content):
        """This method writes the compressed data into a file.

        At initial stage the filename is set. Later on, it will be created
        based on the file opened for compression.
        """
        with open(filename, "w", encoding="utf-8") as compressed_file:
            compressed_file.write(content)

    def fetch_uncompressed_content(self):
        with open(self.uncompressed_filename, encoding="utf-8") as source_content:
            self.content = source_content.read()

    def fetch_compressed_content(self):
        self.frequencies = {}
        with open(self.compressed_filename, encoding="utf-8") as source_content:
            for row in source_content:
                if ";" in row:
                    row = row.replace("\n", "")
                    row_values = row.split(";")
                    self.frequencies[int(row_values[0])] = int(row_values[1])
                else:
                    self.compressed = row

    def huffman_analyze(self, filename: str):
        """An initial method for creating analysis data on compression.

        Args:
            filename (str): a filename to which to store the content.
        """

        uncompressed_size = len(self.content)*8
        stored_characters = len(self.frequencies) * 8 * 2
        coded_character_bits = 0
        for key, value in self.frequencies.items():
            coded_character_bits += int(value).bit_length()
        compressed_content_size = len(self.compressed)
        total_compressed = compressed_content_size + coded_character_bits + stored_characters
        with open(filename, "w", encoding="utf-8") as report:
            report.write(f"Uncompressed size: {uncompressed_size} bits\n")
            report.write("-----\n")
            report.write(f"Compressed content: {compressed_content_size} bits\n")
            report.write("frequencies:\n")
            report.write(f"characters: {stored_characters}\n")
            report.write(f"frequency int value bit size: {coded_character_bits}\n")
            report.write(f"compression total: {total_compressed}\n")
            report.write("-----\n")
            content_ratio = compressed_content_size / uncompressed_size
            report.write(f"Compression ratio on content: {content_ratio}\n")
            total_ratio = total_compressed / uncompressed_size
            report.write(f"Compression ratio on total: {total_ratio}\n")

        self.last_analysis["uncompressed_size"] = uncompressed_size
        self.last_analysis["compressed_total"] = total_compressed
        self.last_analysis["compressed_content"] = compressed_content_size
        self.last_analysis["compressed_header"] = coded_character_bits + stored_characters
        self.last_analysis["content_ratio"] = content_ratio
        self.last_analysis["total_ratio"] = total_ratio



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
        self.calculate_frequencies()
        self.build_huffman_tree()
        self.huffman_encode()
        self.write_compressed_file(self.compressed_filename, self.compressed)
        # for key, item in self.frequencies.items():
        #     print(key, item)

    def execute_uncompression(self):
        """This method handles the uncompression of a given content

        Step 1: Fetch content from the file
        Step 2: Create a huffman tree
        Step 3: Decode content
        Step 4: Write content to file
        """
        self.fetch_compressed_content()
        self.build_huffman_tree()
        self.huffman_decode()
        self.write_uncompressed_file(self.uncompressed_filename, self.uncompressed)


class HuffmanNode:

    def __init__(self, character: str, frequency: int, left=None, right=None):
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
    print("TEST-1: COMPRESSING FILE")
    huffman_compressor = HuffmanCoding("compress_this.txt", "compressed.huf")
    huffman_compressor.execute_compression()
    huffman_compressor.huffman_analyze("huffman_compression_report.log")
    print("TEST-2: UNCOMPRESSING FILE")
    huffman_uncompressor = HuffmanCoding("compressed.huf", "uncompressed.txt")
    huffman_uncompressor.execute_uncompression()
    huffman_uncompressor.huffman_analyze("huffman_uncompression_report.log")
