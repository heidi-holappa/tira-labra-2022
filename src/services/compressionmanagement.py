import os
from entities.huffman import HuffmanCoding
from entities.lempelziv77 import LempelZiv77
from config import DEFAULT_DATA_PATH


class CompressionManagement:

    def __init__(self):
        self.last_analysis = {}

    def initial_huffman_compression(self, filename: str, filepath=DEFAULT_DATA_PATH):
        """A method for testing Huffman coding.

        Gets a filename as a string to compresses.

        Args:
            filename (str): filename to be read

        Returns:
            dict: a dictionary of analysis data to populate GUI labels
        """
        compressed_filename = filename[:-3] + "huf"
        # analysis_filename = filename[:-4] + "_compression_analysis.log"
        huffman_compressor = HuffmanCoding(filename, compressed_filename)
        huffman_compressor.execute_compression()
        huffman_compressor.analyze_compression(filepath)
        # self.last_analysis = huffman_compressor.last_analysis

    def initial_huffman_uncompression(self, filename: str, filepath=DEFAULT_DATA_PATH):
        """An initial method for testing Huffman decoding.

        Gets a filename as a string from where to fetch content to uncompress.

        Args:
            filename (str): file which content is to be uncompressed.
        """

        uncompressed_filename = filename[:-4] + "_uncompressed.txt"
        # analysis_filename = filename[:-4] + "_uncompression_analysis.log"
        huffman_uncompressor = HuffmanCoding(uncompressed_filename, filename)
        huffman_uncompressor.execute_uncompression()
        huffman_uncompressor.analyze_uncompression(filepath)
        # huffman_uncompressor.huffman_analyze(analysis_filename)

    def lempel_ziv_compress(self, filename: str, filepath=DEFAULT_DATA_PATH):
        """A method for testing Lempel-Ziv 77 compression.

        Gets a string of content and compresses it.

        Args:
            content (str): content to be compressed
        """

        compressed_filename = filename[:-3] + "lz"
        # analysis_filename = filename[:-4] + "_compression_analysis.log"
        lempel_ziv_compressor = LempelZiv77(filename, compressed_filename)
        lempel_ziv_compressor.lempel_ziv_activate_compression()
        lempel_ziv_compressor.analyze_compression(filepath)
        # lempel_ziv_compressor.lempel_ziv_analyze(analysis_filename)
        # self.last_analysis = lempel_ziv.last_analysis

    def lempel_ziv_uncompress(self, filename: str, filepath=DEFAULT_DATA_PATH):
        uncompressed_filename = filename[:-3] + "_uncompressed.txt"
        lempel_ziv_uncompressor = LempelZiv77(uncompressed_filename, filename)
        lempel_ziv_uncompressor.lempel_ziv_activate_uncompression()
        lempel_ziv_uncompressor.analyze_uncompression(filepath)

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

    def compress_all_txt_files_in_directory(self):
        for file in os.listdir(DEFAULT_DATA_PATH):
            if file.endswith(".txt"):
                self.lempel_ziv_compress(os.path.join(DEFAULT_DATA_PATH, file))
                self.initial_huffman_compression(
                    os.path.join(DEFAULT_DATA_PATH, file))
        print("DONE!")


default_compression_management = CompressionManagement()
