import os
from services.loghandler import default_loghandler
from entities.huffman import HuffmanCoding
from entities.lempelziv77 import LempelZiv77
from entities.logentry import LogEntry
from config import DEFAULT_DATA_PATH


class CompressionManagement:

    def __init__(self):
        self.last_analysis = {}
        self.loghandler = default_loghandler

    def initial_huffman_compression(self, filename: str):
        """A method for testing Huffman coding.

        Gets a filename as a string to compresses.

        Args:
            filename (str): filename to be read

        Returns:
            dict: a dictionary of analysis data to populate GUI labels
        """
        compressed_filename = filename[:-3] + "huf"
        logentry = LogEntry()
        huffman_compressor = HuffmanCoding(
            filename, compressed_filename, logentry)
        huffman_compressor.execute_compression()
        huffman_compressor.analyze_compression()
        self.add_size_and_compression_ratio_to_logentry(
            filename, compressed_filename, logentry)
        default_loghandler.write_csv_entry_to_file(
            logentry.get_logdata_as_csv_row())
        self.create_compression_logentry(logentry)

    def initial_huffman_uncompression(self, filename: str):
        """An initial method for testing Huffman decoding.

        Gets a filename as a string from where to fetch content to uncompress.

        Args:
            filename (str): file which content is to be uncompressed.
        """

        uncompressed_filename = filename[:-4] + "_uncompressed.txt"
        # analysis_filename = filename[:-4] + "_uncompression_analysis.log"
        logentry = LogEntry()
        huffman_uncompressor = HuffmanCoding(
            uncompressed_filename, filename, logentry)
        huffman_uncompressor.execute_uncompression()
        huffman_uncompressor.analyze_uncompression()
        self.add_size_and_compression_ratio_to_logentry(
            uncompressed_filename, filename, logentry)
        default_loghandler.write_csv_entry_to_file(
            logentry.get_logdata_as_csv_row())
        self.create_uncompression_logentry(logentry)

    def lempel_ziv_compress(self, filename: str):
        """A method for testing Lempel-Ziv 77 compression.

        Gets a string of content and compresses it.

        Args:
            content (str): content to be compressed
        """

        compressed_filename = filename[:-3] + "lz"
        logentry = LogEntry()
        lempel_ziv_compressor = LempelZiv77(
            filename, compressed_filename, logentry)
        lempel_ziv_compressor.lempel_ziv_activate_compression()
        lempel_ziv_compressor.analyze_compression()
        self.add_size_and_compression_ratio_to_logentry(
            filename, compressed_filename, logentry)
        default_loghandler.write_csv_entry_to_file(
            logentry.get_logdata_as_csv_row())
        self.create_compression_logentry(logentry)

    def lempel_ziv_uncompress(self, filename: str):
        uncompressed_filename = filename[:-3] + "_uncompressed.txt"
        logentry = LogEntry()
        lempel_ziv_uncompressor = LempelZiv77(
            uncompressed_filename, filename, logentry)
        lempel_ziv_uncompressor.lempel_ziv_activate_uncompression()
        lempel_ziv_uncompressor.analyze_uncompression()
        self.add_size_and_compression_ratio_to_logentry(
            uncompressed_filename, filename, logentry)
        default_loghandler.write_csv_entry_to_file(
            logentry.get_logdata_as_csv_row())
        self.create_uncompression_logentry(logentry)
        
    def create_compression_logentry(self, logentry: LogEntry):
        self.loghandler.create_compression_entry(logentry.logdata)

    def create_uncompression_logentry(self, logentry: LogEntry):
        self.loghandler.create_uncompression_entry(logentry.logdata)

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

    def add_size_and_compression_ratio_to_logentry(self,
                            uncompressed_filename,
                            compressed_filename,
                            logentry):
        file_stat = os.stat(uncompressed_filename)
        filesize = file_stat.st_size
        compressed_file_stat = os.stat(compressed_filename)
        compressed_filesize = compressed_file_stat.st_size
        logentry.logdata["uncompressed_size"] = str(filesize)
        logentry.logdata["compressed_size"] = str(compressed_filesize)
        logentry.logdata["compression_ratio"] = f"{compressed_filesize / filesize:.2f}"


default_compression_management = CompressionManagement()
