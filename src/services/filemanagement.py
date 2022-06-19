import os
from config import DEFAULT_DATA_PATH
from config import TKINTER_LOG

class FileManagement:

    def __init__(self):
        pass

    def fetch_uncompressed_content(self, filename: str) -> str:
        """Fetch uncompressed content from a file.

        Args:
            filename (str): name and location of the file to be accessed.

        Returns:
            str: content of the file as a String
        """
        with open(filename, encoding="utf-8") as source_content:
            content = source_content.read()
        return content

    def fetch_compressed_content(self, filename: str) -> bytes:
        """Read a file and returns the raw content to the calling method.

        Args:
            filename (str): name and location of file to be read

        Returns:
            str: raw content of the file to be read
        """
        with open(filename, "rb") as source_content:
            raw_content = source_content.read()
        return raw_content

    def create_txt_file(self, filename: str, content: str):
        """This method writes the compressed data into a file.

        At initial stage the filename is set. Later on, it will be created
        based on the file opened for compression.

        Args:
            filename (str): name and location of file to be read
            content (str): content to be written
            as_bytes (bool): if true, transform content to bytes and store content
        """
        with open(filename, "w", encoding="utf-8") as uncompressed_file:
            uncompressed_file.write(content)

    def create_binary_file(self, filename: str, content: bytearray):
        """Creates a file with binary content

        Args:
            filename (str): filename of the file to be created
            content (bytearray): content to be written into the file
        """
        with open(filename, "wb") as compressed_file:
            compressed_file.write(content)

    def get_log_content(self, filepath=DEFAULT_DATA_PATH):
        """Fetches log content from the given file and path

        Args:
            filepath (_type_, optional): Directory for the log file. Defaults to DEFAULT_DATA_PATH.

        Returns:
            str: Returns log file content.
        """
        filename = os.path.join(filepath, TKINTER_LOG)
        content = ""
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as file:
                content = file.read()
        if not content:
            content = "No log content yet. Compress something to get log data."
        return content


default_file_manager = FileManagement()
