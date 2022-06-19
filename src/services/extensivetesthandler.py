import os
import time
import glob
import string
from random import randint, choice
from datetime import datetime
from essential_generators import DocumentGenerator
from services.filemanagement import default_file_manager
from services.compressionmanagement import default_compression_management
from services.loghandler import default_loghandler
from config import DEFAULT_TEST_DATA_PATH
from config import CSV_LOG, HTML_LOG, TKINTER_LOG, ARCHIVE_LOG


class InvalidCharactersError(Exception):
    """Raises an error if file in test-folder contains invalid characters.

    Args:
        Exception: general exception
    """


class ExtensiveTestHandler:
    """A class that handles the manually operated tests and creation of
    random test material.
    """

    def __init__(self) -> None:
        """Constructor for the class.
        """
        self.document_generator = DocumentGenerator()
        self.file_manager = default_file_manager
        self.compression_management = default_compression_management
        self.loghandler = default_loghandler
        self.log_file = os.path.join(DEFAULT_TEST_DATA_PATH, TKINTER_LOG)
        self.html_log_file = os.path.join(
            DEFAULT_TEST_DATA_PATH, HTML_LOG)
        self.log_archive = os.path.join(
            DEFAULT_TEST_DATA_PATH, ARCHIVE_LOG)

    def create_printable_characters(self):
        characters = string.printable.split()[0]
        ascii_order_set = set()
        for char in characters:
            ascii_order_set.add(ord(char))
        ascii_order_set.add(32)
        ascii_order_set.add(10)
        ascii_order_set.add(228)  # ä
        ascii_order_set.add(196)  # Ä
        ascii_order_set.add(197)  # Å
        ascii_order_set.add(229)  # å
        ascii_order_set.add(246)  # ö
        ascii_order_set.add(214)  # Ö
        return ascii_order_set

    def create_document_with_natural_language(self, n_of_paragraphs: int = 100):
        """Uses the libary Essential Generators to create random
        natural content. The created data has to be manipulated as
        it contains characters not suitable for the current algorithms.

        Args:
            n (int, optional): Number of paragraphs to be created. Defaults to 100.
        """
        created_content = ""
        for _ in range(n_of_paragraphs):
            created_content += self.document_generator.paragraph() + "\n\n"
        document_content = ""
        ascii_order_set = self.create_printable_characters()
        for char in created_content:
            if ord(char) in ascii_order_set:
                document_content += char
        file = f"natural-language-document-{n_of_paragraphs}-paragraphs.txt"
        filename = os.path.join(DEFAULT_TEST_DATA_PATH, file)
        print("creating file ", filename)
        self.file_manager.create_txt_file(filename, document_content)

    def create_document_with_random_printable_ascii(self, n_of_paragraphs: int = 100):
        """Creates paragraphs of random ascii-characters.

        Args:
            n (int, optional): Number of paragraps to create. Defaults to 100.
        """
        document_content = ""
        characters = string.printable.split()[0]
        for _ in range(n_of_paragraphs):
            characters_in_paragraph = randint(500, 1000)
            document_content += "".join([choice(characters)
                                        for _ in range(characters_in_paragraph)]) + "\n\n"
        file = f"random-printable-ascii-{n_of_paragraphs}-paragraphs.txt"
        filename = os.path.join(DEFAULT_TEST_DATA_PATH, file)
        print("creating file ", filename)
        self.file_manager.create_txt_file(filename, document_content)

    def activate_extensive_tests(self, min_characters: int = 0, max_characters: int = 100000):
        """Activates extensive tests. Formats the log file and picks
        up files that meet the given limitation for character length.
        For each file that meets the limitation the tests are then run.

        Args:
            max_characters (int, optional): Maximum character length for files. Defaults to 100000.
        """

        self.loghandler.init_html_file()
        self.validate_test_files()
        extensive_test_starttime = time.time()
        if os.path.exists(self.log_file):
            self.archive_log_content()
        success = 0
        fail = 0
        for filename in glob.glob(os.path.join(DEFAULT_TEST_DATA_PATH, '*.txt')):
            with open(filename, 'r', encoding="utf-8") as file:
                content = file.read()
                if len(content) >= min_characters and len(content) <= max_characters:
                    if self.run_tests_on_file(filename, content):
                        success += 1
                    else:
                        fail += 1
        self.remove_extensive_test_files()
        extensive_test_endtime = time.time()
        test_total_time = extensive_test_endtime - extensive_test_starttime
        total = f"{test_total_time:.2f}"
        self.log_end(success, fail, total)
        self.html_log_end(success, fail, total)

    def validate_test_files(self):
        ascii_order_set = self.create_printable_characters()
        for filename in glob.glob(os.path.join(DEFAULT_TEST_DATA_PATH, '*.txt')):
            with open(filename, 'r', encoding="utf-8") as file:
                content = file.read()
                for char in content:
                    if ord(char) not in ascii_order_set:
                        file_split = filename.split("/")
                        print(
                            f"Error! {file_split[-1]} includes non-supported characters")
                        raise InvalidCharactersError(
                            f"Error! {file_split[-1]} includes non-supported characters. \
Non-supported character: {char}")

    def remove_extensive_test_files(self):
        for filename in glob.glob(os.path.join(DEFAULT_TEST_DATA_PATH, '*_uncompressed.txt')):
            os.remove(filename)
        for filename in glob.glob(os.path.join(DEFAULT_TEST_DATA_PATH, '*.huf')):
            os.remove(filename)
        for filename in glob.glob(os.path.join(DEFAULT_TEST_DATA_PATH, '*.lz')):
            os.remove(filename)



    def run_tests_on_file(self, filename: str, content: str):
        """Runs tests on a given file. Compresses and uncompresses
        data on both compression algorithms. Validates that uncompressed
        data matches the original.

        Args:
            filename (str): File to be compressed
            content (str): Content of the file

        Returns:
            bool: Status of test success. If tests fail, return False.
        """
        tests_succeeded = True
        tests_succeeded = self.test_huffman_compression(filename, content)
        tests_succeeded = self.test_lempelziv_compression(filename, content)
        return tests_succeeded

    def test_lempelziv_compression(self, filename: str, content: str):
        tests_succeeded = True

        try:
            self.compression_management.lempel_ziv_compress(filename)
            self.compression_management.lempel_ziv_uncompress(
                filename[:-3] + "lz")
            with open(filename[:-4] + "_uncompressed.txt", "r", encoding="utf-8") as file:
                lz77_uncompressed_content = file.read()
            result = self.validate_content_matches(
                content, lz77_uncompressed_content)
            if not result:
                tests_succeeded = False
                self.log_entry(filename,
                               "Failure: Original and uncompressed contents in previous \
                                test did not match.",
                               "Lempel-Ziv77 compression or uncompression")
        except Exception as exption:
            tests_succeeded = False
            self.log_entry(filename, str(
                exption), "Lempel-Ziv77 compression or uncompression")
        return tests_succeeded

    # TODO: Refactor error handling to log files
    def test_huffman_compression(self, filename: str, content: str):
        tests_succeeded = True
        try:
            self.compression_management.initial_huffman_compression(
                filename)
            self.compression_management.initial_huffman_uncompression(
                filename[:-3] + "huf")
            with open(filename[:-4] + "_uncompressed.txt", "r", encoding="utf-8") as file:
                huffman_uncompressed_content = file.read()
            result = self.validate_content_matches(
                content, huffman_uncompressed_content)
            if not result:
                tests_succeeded = False
                self.log_entry(filename,
                               "Failure: Original and uncompressed contents in previous \
                                test did not match.",
                               "Huffman compression or uncompression")
                self.html_log_entry(filename,
                                    "Failure: Original and uncompressed contents in previous \
                                test did not match.",
                                    "Huffman compression or uncompression")
        except Exception as exption:
            self.log_entry(filename, str(
                exption), "Huffman compression or uncompression")
            self.html_log_entry(filename, str(
                exption), "Huffman compression or uncompression")
            tests_succeeded = False
        return tests_succeeded

    def validate_content_matches(self, original_content: str, uncompressed_content: str) -> bool:
        """Validates that the uncompressed content matches the original

        Args:
            original_content (str): Original content
            uncompressed_content (str): Content that has been compressed and then uncompressed.

        Returns:
            bool: True if validation is successful
        """
        if len(original_content) != len(uncompressed_content):
            return False
        content_valid = True
        for char in enumerate(original_content):
            if original_content[char[0]] != uncompressed_content[char[0]]:
                content_valid = False
        return content_valid

    def log_end(self, success, fail, total_time):
        """Once tests are done, a summary of tests is written to the file.

        Uses 'r+' to write to the start of the file.

        Args:
            success (int): number of successful tests
            fail (int): number of failed tests
        """
        with open(self.log_file, 'r+', encoding='utf-8') as file:
            content = file.read()
            file.seek(0)
            log_time = datetime.now()
            log_time_strf = log_time.strftime("%d.%m.%Y %H:%M:%S")
            analysis = f"""------ EXTENSIVE TEST SUMMARY  -------\n\
------ TIME: {log_time_strf} ------\n\
Total runtime: {total_time} seconds\n\
Successful tests: {success}\n\
Failed tests: {fail}\n\n\
------ DETAILED SUMMARY ------\n\n"""
            file.write(analysis)
            file.write(content)
            file.write("\n\n----- EXTENSIVE TEST SUMMARY ENDS ------\n\n")

    def log_entry(self, filename: str, error_content: str, phase: str) -> None:
        """If a test fails a log entry is created.

        Args:
            filename (str): File for which the failure happened.
            error_content (str): Error content.
            phase (str): Clarification on which algorithm the error occured.
        """
        content = "--------- ERROR NOTIFICATION ---------\n"
        content += f"Filename: {filename}\n"
        content += f"Failed task: {phase}\n"
        content += f"Description: {error_content}\n"
        content += "------ END OF ERROR NOTIFICATION ------\n\n"
        with open(self.log_file, "a", encoding="utf-8") as file:
            file.write(content)

    def html_log_entry(self, filename: str, error_content: str, phase: str) -> None:
        """If a test fails a log entry is created.

        Args:
            filename (str): File for which the failure happened.
            error_content (str): Error content.
            phase (str): Clarification on which algorithm the error occured.
        """
        content = "<H2> ERROR NOTIFICATION </H2><br>\n"
        content += f"<b>Filename:</b> {filename}<br>\n"
        content += f"<b>Failed task:</b> {phase}<br>\n"
        content += f"<b>Description:</b> {error_content}<br>\n"
        with open(self.html_log_file, "a", encoding="utf-8") as file:
            file.write(content)

    def html_log_end(self, success, fail, total_time):
        """Once tests are done, a summary of tests is written to the file.

        Uses 'r+' to write to the start of the file.

        Args:
            success (int): number of successful tests
            fail (int): number of failed tests
        """
        # with open(self.log_file, 'r', encoding='utf-8') as file:
        #     content = file.read()
        #     content_as_list = content.split("\n")
        # with open(self.html_log_file, 'w', encoding="utf-8") as file:
        #     log_time = datetime.now()
        #     log_time_strf = log_time.strftime("%d.%m.%Y %H:%M:%S")
        self.loghandler.create_html_file(total_time, success, fail)

        # file.write(analysis)
        # bar_huffman = content_as_list[0].split(";")
        # bar_lempelziv = content_as_list[1].split(";")
        # for row in content_as_list[2:]:
        #     file.write(row + "<br>\n")

    def archive_log_content(self):
        """Archives log content of previous test run.
        """
        content = ""
        with open(self.log_file, "r", encoding="utf-8") as file:
            content = file.read()
        with open(self.log_archive, "a", encoding="utf-8") as file:
            file.write(content)
        os.remove(self.log_file)
        with open(self.log_file, "a", encoding="utf-8") as file:
            file.close()


default_test_handler = ExtensiveTestHandler()
