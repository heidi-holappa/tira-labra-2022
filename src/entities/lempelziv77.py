from statistics import mean
import time
from entities.logentry import LogEntry
from entities.supportedcharacters import default_supported_characters
from services.filemanagement import default_file_manager

class NoCompressedContentError(Exception):
    """Gives an understandable error incase compression fails because
    no content is given.

    Args:
        Exception: A general exeption message that is logged.
    """


class LempelZiv77:

    """Class responsible for compressing/uncompressing data with LZ77
    compression algorithm.
    """

    def __init__(self,
                 uncompressed_filename: str,
                 compressed_filename: str,
                 logentry: LogEntry = LogEntry()):
        """Construction for the class

        Args:
            uncompressed_filename (str): name and location of the file with
            uncompressed data
            compressed_filename (str): name and location of the file with
            compressed data
        """
        self.uncompressed_filename = uncompressed_filename
        self.compressed_filename = compressed_filename
        self.content = ""
        self.compressed_content = ""
        self.compressed_content_as_list = []
        self.window_size = 4095
        self.buffer_size = 15
        self.file_manager = default_file_manager
        self._bytearray_list = []
        self.bytearray_data = None
        self.logentry = logentry
        self.supported_characters = default_supported_characters

    def fetch_uncompressed_content(self):
        """Calls FileManagement from service package to fetch uncompressed content
        """
        self.content = self.file_manager.fetch_uncompressed_content(
            self.uncompressed_filename)

    def fetch_compressed_content(self):
        """Calls FileManagement from service package to fetch compressed content and
        another method to transform the fetched content into a string.
        """
        compressed_content_as_bytes: bytes = self.file_manager.fetch_compressed_content(
            self.compressed_filename)
        self.tranform_bytes_into_string(compressed_content_as_bytes)

    def tranform_bytes_into_string(self, byte_data):
        """Transforms the byte data into string of ones and zeroes.

        Args:
            byte_data (bytes): Stored content as bytes of data
        """

        data_as_list = []
        for byte in byte_data:
            data_as_list.append(str(bin(byte)[2:].zfill(8)))
        self.compressed_content = "".join(data_as_list)

    def write_txt_content_into_a_file(self, filename, content_to_write):
        """Calls file management to write content to a file

        Args:
            filename (str): file to write to
            content_to_write (str): content to be written
        """
        self.file_manager.create_txt_file(filename, content_to_write)

    def write_binary_content_into_a_file(self, filename, content_to_write):
        """Calls FileManagement from service package to write byte content
        to a file.

        Args:
            filename (str): file to write into
            content_to_write (bytes): byte-data to be written
        """
        self.file_manager.create_binary_file(filename, content_to_write)

    def lempel_ziv_activate_compression(self):
        """A method to activate and manage different steps of compression.

        Method also includes run-time logging on different phases.
        """
        fetch_starttime = time.time()
        self.fetch_uncompressed_content()
        fetch_endtime = time.time()
        fetch_total_time = fetch_endtime - fetch_starttime
        self.logentry.logdata["data_fetch_and_process_time"] = f"{fetch_total_time:.2f}"

        compress_starttime = time.time()
        self.compress_content()
        compress_endtime = time.time()
        compress_total_time = compress_endtime - compress_starttime
        self.logentry.logdata["compression_time"] = f"{compress_total_time:.2f}"

        write_starttime = time.time()
        self.write_binary_content_into_a_file(
            self.compressed_filename, self.bytearray_data)
        write_endtime = time.time()
        write_total_time = write_endtime - write_starttime
        self.logentry.logdata["data_write_and_process_time"] = f"{write_total_time:.2f}"

    def lempel_ziv_activate_uncompression(self):
        """A method to activate and manage different steps of uncopmpression.

        Method also includes run-time logging.
        """
        fetch_starttime = time.time()
        self.fetch_compressed_content()
        fetch_endtime = time.time()
        fetch_total_time = fetch_endtime - fetch_starttime
        self.logentry.logdata["data_fetch_and_process_time"] = f"{fetch_total_time:.2f}"

        compress_starttime = time.time()
        self.lempel_ziv_handle_uncompression()
        compress_endtime = time.time()
        compress_total_time = compress_endtime - compress_starttime
        self.logentry.logdata["compression_time"] = f"{compress_total_time:.2f}"

        write_starttime = time.time()
        self.write_txt_content_into_a_file(
            self.uncompressed_filename, self.content)
        write_endtime = time.time()
        write_total_time = write_endtime - write_starttime
        self.logentry.logdata["data_write_and_process_time"] = f"{write_total_time:.2f}"

    def lempel_ziv_handle_uncompression(self):
        """A method to handle the steps of data uncompression. First data is transformed
        to tuples. Then the content is uncompressed.
        """
        self.construct_tuples_from_fetched_content()
        self.lempel_ziv_uncompress()

    def compress_content(self):
        """A method to compress the given content.
        """
        self.compressed_content_as_list = []
        i = 0
        while i < len(self.content):
            result = self.init_window_search(i)
            self.compressed_content_as_list.append(result)
            i += result[1]
        self.construct_binary_version_of_content()

    # TODO: Remove after demo-session if new version is favorable
    def create_binary_version_of_content(self):
        """A method to create binary type content of the data. The logic is the following:
        Offset: 12 bits
        Length of match: 4 bits
        Next character: a byte"""
        content_as_bits = []
        for member in self.compressed_content_as_list:
            offset = member[0]
            match_length = member[1]
            next_character = member[2]
            content_as_bits.append(str(bin(offset)[2:].zfill(12)))
            content_as_bits.append(str(bin(match_length)[2:].zfill(4)))
            if offset == 0:
                content_as_bits.append(str(bin(next_character)[2:].zfill(8)))
        self.compressed_content = "".join(content_as_bits)
        for i in range(0, len(self.compressed_content), 8):
            value = ord(chr(int(self.compressed_content[i:i+8], 2)))
            self._bytearray_list.append(value)
        self.bytearray_data = bytearray(self._bytearray_list)

    def construct_binary_version_of_content(self):
        """A method to create binary type content of the data. The logic is the following:
        Offset: 12 bits
        Length of match: 4 bits
        Next character: a byte"""
        content_as_bits = []
        for member in self.compressed_content_as_list:
            offset = member[0]
            match_length = member[1]
            next_character = member[2]
            next_char_index = self.supported_characters.char_to_index_dict[next_character]
            if offset == 0:
                content_as_bits.append("0")
                # content_as_bits.append(str(bin(next_character)[2:].zfill(8)))
                content_as_bits.append(str(bin(next_char_index)[2:].zfill(7)))
            else:
                content_as_bits.append("1")
                content_as_bits.append(str(bin(offset)[2:].zfill(12)))
                content_as_bits.append(str(bin(match_length)[2:].zfill(4)))
        content_as_bits.append("0000000")
        remaining_bits = str((8 - len(content_as_bits) % 8) * "0")
        content_as_bits.append(remaining_bits)
        self.compressed_content = "".join(content_as_bits)
        for i in range(0, len(self.compressed_content), 8):
            value = ord(chr(int(self.compressed_content[i:i+8], 2)))
            self._bytearray_list.append(value)
        self.bytearray_data = bytearray(self._bytearray_list)

    def init_window_search(self, current_index: int) -> tuple:
        """A method to initialize the window search.

        Args:
            current_index (int): Index from which the sliding windows starts.

        Returns:
            tuple: result of compression (offset, length, next character)
        """
        window_start_index = max(0, current_index - self.window_size)
        buffer_end_index = min(
            current_index + self.buffer_size, len(self.content))
        result = self.find_matches_in_sliding_window(
            window_start_index,
            current_index,
            buffer_end_index)
        return result

    def find_matches_in_sliding_window(
        self,
        window_start_index: int,
        buffer_start_index: int,
        buffer_end_index: int
    ):
        """An iterative method to find the longest string match in a sliding window.
        Uses Python's built-in method str.rfind() to find longest match iteratively.
        Based on documentation str.find() worst case time complexity is O(n*m),
        on average time complexity is O(m).

        Args:
            window_start_index (int): index from which the sliding window begins.
            buffer_start_index (int): index from which the lookahead buffer start
            buffer_end_index (int): index in which the buffer and the sliding windows end.

        Returns:
            tuple: offset, match length and character, if no match is found.
        """
        longest = (0, 0, 0)
        for i in range(buffer_start_index+3, buffer_end_index):
            found_index = self.content[window_start_index:buffer_start_index].rfind(
                self.content[buffer_start_index:i])
            if found_index != -1:
                longest = (buffer_start_index - (window_start_index +
                           found_index), i - buffer_start_index, 0)
            else:
                break

        if longest[1] == 0:
            longest = (0, 1, ord(self.content[buffer_start_index]))
        return longest


    def construct_tuples_from_fetched_content(self):
        """A method that transforms the fetched data into tuples.

        The first bit indicates whether a match exists. If bit value is 0,
        not match exists and the next 7 bits include the index of the next character.
        If a match exists, the next 12 bits include the offset and the following 4 bits
        the match length.
        """

        self.compressed_content_as_list = []
        i = 0
        while i < len(self.compressed_content):
            if self.compressed_content[i] == "0":
                if self.compressed_content[i+1:i+8] == "0000000":
                    break
                offset = 0
                length = 1
                character_index = int(self.compressed_content[i+1:i+8], 2)
                character = chr(self.supported_characters.index_to_char_dict[character_index])
                i += 8
            else:
                offset = int(self.compressed_content[i+1:i+13], 2)
                length = int(self.compressed_content[i+13:i+17], 2)
                character = ""
                i += 17
            self.compressed_content_as_list.append((offset, length, character))

    def lempel_ziv_uncompress(self):
        """A method to handle the uncompression of the data.

        Raises:
            NoCompressedContentError: A general error to be raised if no data is given.
        """
        if len(self.compressed_content_as_list) == 0:
            raise NoCompressedContentError()
        variable_n = len(self.compressed_content_as_list)
        content = []
        for i in range(variable_n):
            if self.compressed_content_as_list[i][0] == 0:
                content.append(self.compressed_content_as_list[i][2])
            else:
                variable_m = self.compressed_content_as_list[i][1]
                offset = self.compressed_content_as_list[i][0]
                for _ in range(variable_m):
                    content.append(content[-offset])
        uncompressed_string = "".join(content)
        self.content = uncompressed_string

    def calculate_mean_length_and_mean_offset_for_log(self):
        """Handles calculating the mean length and mean offset of
        the matching content in the events when a match is found
        """
        lengths = []
        offsets = []
        for entry in self.compressed_content_as_list:
            if entry[0] > 0:
                offsets.append(entry[0])
                lengths.append(entry[1])
        self.logentry.logdata["lz_avg_match_length"] = str(mean(lengths))
        self.logentry.logdata["lz_mean_offset"] = str(mean(offsets))

    def analyze_compression(self):
        """An initial method for creating analysis data on compression.
        """

        self.logentry.logdata["original_filename"] = self.uncompressed_filename.split(
            "/")[-1]
        self.logentry.logdata["compressed_filename"] = self.compressed_filename.split(
            "/")[-1]
        self.logentry.logdata["compression_method"] = "Lempel-Ziv 77"
        self.logentry.logdata["action"] = "0"
        self.calculate_mean_length_and_mean_offset_for_log()

    def analyze_uncompression(self):
        """An initial method for creating analysis data on compression.
        """

        self.logentry.logdata["compressed_filename"] = self.compressed_filename.split(
            "/")[-1]
        self.logentry.logdata["uncompressed_filename"] = self.uncompressed_filename.split(
            "/")[-1]
        self.logentry.logdata["compression_method"] = "Lempel-Ziv 77"
        self.logentry.logdata["action"] = "1"
        self.calculate_mean_length_and_mean_offset_for_log()


if __name__ == "__main__":
    pass
