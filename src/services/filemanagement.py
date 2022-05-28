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
        with open(filename, "wb") as compressed_file:
            compressed_file.write(content)

default_file_manager = FileManagement()
