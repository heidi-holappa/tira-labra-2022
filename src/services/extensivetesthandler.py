import os, glob
import string
from random import randint, choice
from datetime import datetime
from essential_generators import DocumentGenerator
from services.filemanagement import default_file_manager
from services.compressionmanagement import default_compression_management
from config import DEFAULT_TEST_DATA_PATH

class ExtensiveTestHandler:

    def __init__(self) -> None:
        self.document_generator = DocumentGenerator()
        self.file_manager = default_file_manager
        self.compression_management = default_compression_management
        self.log_file = os.path.join(DEFAULT_TEST_DATA_PATH, "compression.log")
        self.log_archive = os.path.join(DEFAULT_TEST_DATA_PATH, "compression_archive.log")

    def create_document_with_natural_language(self, n: int = 100):
        created_content = ""
        for i in range(n):
            created_content += self.document_generator.paragraph() + "\n\n"
        document_content = ""
        characters = string.printable.split()[0]
        ascii_order_set = set()
        for char in characters:
            ascii_order_set.add(ord(char))
        ascii_order_set.add(32)
        ascii_order_set.add(10)
        for char in created_content:
            if ord(char) in ascii_order_set:
                document_content += char
        file = f"natural-language-document-{n}-paragraphs.txt"
        filename = os.path.join(DEFAULT_TEST_DATA_PATH, file)
        print("creating file ", filename)
        self.file_manager.create_txt_file(filename, document_content)
    
    def create_document_with_random_printable_ascii(self, n: int = 100):
        document_content = ""
        characters = string.printable.split()[0]
        for i in range(n):
            m = randint(500, 1000)
            document_content += "".join([choice(characters) for i in range(m)]) + "\n\n"
        file = f"random-printable-ascii-{n}-paragraphs.txt"
        filename = os.path.join(DEFAULT_TEST_DATA_PATH, file)
        print("creating file ", filename)
        self.file_manager.create_txt_file(filename, document_content)
    
    def activate_extensive_tests(self, max_characters: int = 100000):
        if os.path.exists(self.log_file):
            self.archive_log_content()
            os.remove(self.log_file)
        with open(self.log_file, "a", encoding="utf-8") as file:
            file.close()
        success = 0
        fail = 0
        for filename in glob.glob(os.path.join(DEFAULT_TEST_DATA_PATH, '*.txt')):
            with open(filename, 'r', encoding="utf-8") as file:
                content = file.read()
                if len(content) <= max_characters:
                    result = self.run_tests_on_file(filename, content)
                    if result:
                        success += 1
                    else:
                        fail += 1
        for filename in glob.glob(os.path.join(DEFAULT_TEST_DATA_PATH, '*_uncompressed.txt')):
            os.remove(filename)
        for filename in glob.glob(os.path.join(DEFAULT_TEST_DATA_PATH, '*.huf')):
            os.remove(filename)
        for filename in glob.glob(os.path.join(DEFAULT_TEST_DATA_PATH, '*.lz')):
            os.remove(filename)
        self.log_end(success, fail)

    def run_tests_on_file(self, filename: str, content: str):
        filepath = DEFAULT_TEST_DATA_PATH
        tests_succeeded = True
        try:
            self.compression_management.initial_huffman_compression(filename, filepath)
            self.compression_management.initial_huffman_uncompression(filename[:-3] + "huf", filepath)
            with open(filename[:-4] + "_uncompressed.txt", "r", encoding="utf-8") as file:
                huffman_uncompressed_content = file.read()
            result = self.validate_content_matches(content, huffman_uncompressed_content)
            if not result:
                tests_succeeded = False
                self.log_entry(filename,
                            "Failure: Original and uncompressed contents in previous test did not match.",
                            "Huffman compression or uncompression")
        except Exception as e:
            self.log_entry(filename, str(e), "Huffman compression or uncompression")
            tests_succeeded = False
        try:
            self.compression_management.lempel_ziv_compress(filename, filepath)
            self.compression_management.lempel_ziv_uncompress(filename[:-3] + "lz", filepath)
            with open(filename[:-4] + "_uncompressed.txt", "r", encoding="utf-8") as file:
                lz77_uncompressed_content = file.read()
            result = self.validate_content_matches(content, lz77_uncompressed_content)
            if not result:
                tests_succeeded = False
                self.log_entry(filename,
                            "Failure: Original and uncompressed contents in previous test did not match.",
                            "Lempel-Ziv77 compression or uncompression")
        except Exception as e:
            tests_succeeded = False
            self.log_entry(filename, str(e), "Lempel-Ziv77 compression or uncompression")
        return tests_succeeded
    
    def validate_content_matches(self, original_content: str, uncompressed_content: str) -> bool:
        if len(original_content) != len(uncompressed_content):
            return False
        content_valid = True
        for char in range(len(original_content)):
            if original_content[char] != uncompressed_content[char]:
                content_valid = False
        return content_valid
    

    def log_end(self, success, fail):
        with open(self.log_file, 'r+', encoding='utf-8') as file:
            content = file.read()
            file.seek(0)
            log_time = datetime.now()
            log_time_strf = log_time.strftime("%d.%m.%Y %H:%M:%S")
            file.write("------ EXTENSIVE TEST SUMMARY  -------\n")
            file.write(f"------ TIME: {log_time_strf} ------\n")
            file.write(f"Successful tests: {success}\n")
            file.write(f"Failed tests: {fail}\n\n")
            file.write(f"------ DETAILED SUMMARY ------\n\n")
            file.write(content)
            file.write("\n\n----- EXTENSIVE TEST SUMMARY ENDS ------\n\n")

    def log_entry(self, filename: str, error_content: str, phase: str) -> None:
        content = "--------- ERROR NOTIFICATION ---------\n"
        content += f"Filename: {filename}\n"
        content += f"Failed task: {phase}\n"
        content += f"Description: {error_content}\n"
        content += "------ END OF ERROR NOTIFICATION ------\n\n"
        with open(self.log_file, "a", encoding="utf-8") as file:
            file.write(content)
    
    def archive_log_content(self):
        content = ""
        with open(self.log_file, "r", encoding="utf-8") as file:
            content = file.read()
        with open(self.log_archive, "a", encoding="utf-8") as file:
            file.write(content)


default_test_handler = ExtensiveTestHandler()