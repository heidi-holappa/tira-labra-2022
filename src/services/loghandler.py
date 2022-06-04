from datetime import datetime
import os
from config import DEFAULT_DATA_PATH


class LogHandler:
    """A class to handle creating log entries.
    """

    def __init__(self) -> None:
        """Constructor for the class. Uses the default data path defined
        in the .env file.
        """
        self.filename = "compression.log"
        self.archive_filename = "compression_archive.log"
        self.logdata = {
            "original_filename": "",
            "compressed_filename": "",
            "uncompressed_filename": "",
            "compression_method": "",
            "uncompressed_size": 0,
            "compressed_size": 0,
            "compression_time": "",
            "uncompression_time": "",
            "data_fetch_and_process_time": "",
            "data_write_and_process_time": "",
        }

        self.init_log_file()

    def init_log_file(self):
        file_and_path = os.path.join(DEFAULT_DATA_PATH, self.filename)
        if os.path.exists(file_and_path):
            self.archive_log_content(file_and_path)
            os.remove(file_and_path)
        with open(file_and_path, "a", encoding="utf-8") as file:
            file.close()

    def archive_log_content(self, filename):
        content = ""
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()
        archive_file_and_path = os.path.join(
            DEFAULT_DATA_PATH, self.archive_filename)
        with open(archive_file_and_path, "a", encoding="utf-8") as file:
            file.write(content)

    def create_compression_entry(self, filepath=DEFAULT_DATA_PATH, additional_content: str = "") -> None:
        """Creates a log entry with the given values. Basic information is
        collected from both compressin methods (Huffman coding, LZ77). Additional
        log-content can also be given.

        Args:
            additional_content (str, optional): Additional algorithm specific content.
            Defaults to "".
        """

        log_filename = os.path.join(filepath, self.filename)

        if not os.path.exists(log_filename):
            with open(log_filename, "a", encoding="utf-8") as file:
                file.close()

        # TODO: REFACTOR. CREATE CONTENT FIRST, THEN JUST SINGLE WRITE.
        with open(log_filename, "a", encoding="utf-8") as file:
            log_time = datetime.now()
            log_time_strf = log_time.strftime("%d.%m.%Y %H:%M:%S")
            file.write("------ NEW ENTRY: COMPRESSING DATA ------\n")
            file.write(f"Log entry created: {log_time_strf}\n")
            file.write(f"File accessed: {self.logdata['original_filename']}\n")
            file.write(
                f"File created: {self.logdata['compressed_filename']}\n")
            file.write(
                f"Compression method: {self.logdata['compression_method']}\n")
            file.write(
                f"Uncompressed_size: {self.logdata['uncompressed_size']} bits\n")
            file.write(
                f"Compressed size: {self.logdata['compressed_size']} bits\n")
            compression_ratio = self.logdata['compressed_size'] / \
                self.logdata['uncompressed_size'] * 100
            file.write(f"Compression ratio: {compression_ratio:.2f}\n")
            file.write(
                f"Time used for fetching and processing data: {self.logdata['data_fetch_and_process_time']} seconds\n")
            file.write(
                f"Time used for compression: {self.logdata['compression_time']}\n")
            file.write(
                f"Time used for writing and processing data: {self.logdata['data_write_and_process_time']} seconds\n")
            if additional_content:
                file.write(additional_content)
            file.write("------ END OF ENTRY ------\n\n")

    # TODO: REFACTOR. CREATE CONTENT FIRST, THEN JUST SINGLE WRITE.
    def create_uncompression_entry(self, filepath=DEFAULT_DATA_PATH, additional_content: str = "") -> None:
        """Writes log data for uncompression event.

        Args:
            additional_content (str, optional): Optional additional information. Defaults to "".
        """
        log_filename = os.path.join(filepath, self.filename)

        if not os.path.exists(log_filename):
            with open(log_filename, "a", encoding="utf-8") as file:
                file.close()

        with open(log_filename, "a", encoding="utf-8") as file:
            log_time = datetime.now()
            log_time_strf = log_time.strftime("%d.%m.%Y %H:%M:%S")
            file.write("------ NEW ENTRY: UNCOMPRESSING DATA ------\n")
            file.write(f"Log entry created: {log_time_strf}\n")
            file.write(
                f"File accessed: {self.logdata['compressed_filename']}\n")
            file.write(
                f"File created: {self.logdata['uncompressed_filename']}\n")
            file.write(
                f"Compression method: {self.logdata['compression_method']}\n")
            file.write(
                f"Compressed size: {self.logdata['compressed_size']} bits\n")
            file.write(
                f"Uncompressed_size: {self.logdata['uncompressed_size']} bits\n")
            compression_ratio = self.logdata['compressed_size'] / \
                self.logdata['uncompressed_size'] * 100
            file.write(f"Compression ratio: {compression_ratio:.2f}\n")
            file.write(
                f"Time used for fetching and processing data: {self.logdata['data_fetch_and_process_time']} seconds\n")
            file.write(
                f"Time used for compression: {self.logdata['compression_time']} seconds\n")
            file.write(
                f"Time used for writing and processing data: {self.logdata['data_write_and_process_time']} seconds\n")
            if additional_content:
                file.write(additional_content)
            file.write("------ END OF ENTRY ------\n\n")
