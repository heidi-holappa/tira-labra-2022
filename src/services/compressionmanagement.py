from entities.huffman import HuffmanCoding

class CompressionManagement:

    def __init__(self):
        pass

    def initial_huffman_compression(self, filename: str):
        """A method for testing Huffman coding. 
        
        Gets a filename as a string to compresses. 

        Args:
            filename (str): filename to be read
        """
        compressed_filename = filename[:-3] + "huf"
        analysis_filename = filename[:-4] + "_compression_analysis.log"
        huffman_compressor = HuffmanCoding(filename, compressed_filename)
        huffman_compressor.execute_compression()
        huffman_compressor.huffman_analyze(analysis_filename)

        # with open(filename) as file_to_be_compressed:
        #     content = file_to_be_compressed.read()
        # print(content)


        pass

    def initial_huffman_uncompression(self, filename: str):
        """An initial method for testing Huffman decoding.

        Gets a filename as a string from where to fetch content to uncompress.

        Args:
            filename (str): file which content is to be uncompressed. 
        """
        
        uncompressed_filename = filename[:-4] + "_uncompressed.txt"
        analysis_filename = filename[:-4] + "_uncompression_analysis.log"
        huffman_uncompressor = HuffmanCoding(filename, uncompressed_filename)
        huffman_uncompressor.execute_uncompression()
        huffman_uncompressor.huffman_analyze(analysis_filename)


    def initial_lempel_ziv_test(self, content: str):
        """A method for testing Lempel-Ziv 77 compression. 

        Gets a string of content and compresses it. 

        Args:
            content (str): content to be compressed
        """

        pass

    def validate_file_extension(self, extension: str, accepted_extensions: str) -> bool:
        """A method to validate that the file extension is valid. 

        Args:
            extension (str): a string of file extension
            accepted_extensions (str): one or more extenstions that are valid. 

        Returns:
            boolean: True if valid, False otherwise
        """
        accepted = accepted_extensions.split(";")
        return bool(extension in accepted)


defaul_compression_management = CompressionManagement()