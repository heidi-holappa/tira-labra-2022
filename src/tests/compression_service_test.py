import unittest
import os
from services.compressionmanagement import defaul_compression_management

class TestCompressionManagement(unittest.TestCase):

    def setUp(self):
        self.compression_management = defaul_compression_management

    def test_data_compression_method_is_run_successfully(self):
        filename = "file.txt"
        compressed_filename = filename[:-3] + "huf"
        with open(filename, "w") as file:
            file.write("This is test content")
        self.compression_management.initial_huffman_compression(filename)
        compressed_file_created = bool(os.path.exists(compressed_filename))
        os.remove(filename)
        os.remove(compressed_filename)
        self.assertEqual(True, compressed_file_created)

    
    
    
    def test_validation_success_when_extension_is_valid(self):
        extension = "txt"
        accepted_extensions = "log;txt;md"
        return_value = self.compression_management.validate_file_extension(extension, accepted_extensions)
        self.assertEqual(True, return_value)

    def test_validation_failes_when_extension_is_not_valid(self):
        extension = "dxd"
        accepted_extensions = "log;txt;md"
        return_value = self.compression_management.validate_file_extension(extension, accepted_extensions)
        self.assertEqual(False, return_value)

    