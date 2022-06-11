import time
from services.filemanagement import default_file_manager
from services.loghandler import LogHandler
from config import DEFAULT_DATA_PATH


class NoCompressedContentError(Exception):
    pass


class LempelZiv77:

    """Class responsible for compressing/uncompressing data with LZ77
    compression algorithm.
    """

    def __init__(self, uncompressed_filename: str, compressed_filename: str):
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
        self.loghandler = LogHandler()

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
        for byte in byte_data:
            self.compressed_content += str(bin(byte)[2:].zfill(8))

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
        """A method to activate and manage different steps of compression
        """
        fetch_starttime = time.time()
        self.fetch_uncompressed_content()
        fetch_endtime = time.time()
        fetch_total_time = fetch_endtime - fetch_starttime
        self.loghandler.logdata["data_fetch_and_process_time"] = f"{fetch_total_time:.2f}"

        compress_starttime = time.time()
        self.compress_content()
        compress_endtime = time.time()
        compress_total_time = compress_endtime - compress_starttime
        self.loghandler.logdata["compression_time"] = f"{compress_total_time:.2f}"

        write_starttime = time.time()
        self.write_binary_content_into_a_file(
            self.compressed_filename, self.bytearray_data)
        write_endtime = time.time()
        write_total_time = write_endtime - write_starttime
        self.loghandler.logdata["data_write_and_process_time"] = f"{write_total_time:.2f}"

    def lempel_ziv_activate_uncompression(self):
        """A method to activate and manage different steps of uncopmpression
        """
        fetch_starttime = time.time()
        self.fetch_compressed_content()
        fetch_endtime = time.time()
        fetch_total_time = fetch_endtime - fetch_starttime
        self.loghandler.logdata["data_fetch_and_process_time"] = f"{fetch_total_time:.2f}"

        compress_starttime = time.time()
        self.lempel_ziv_handle_uncompression()
        compress_endtime = time.time()
        compress_total_time = compress_endtime - compress_starttime
        self.loghandler.logdata["compression_time"] = f"{compress_total_time:.2f}"

        write_starttime = time.time()
        self.write_txt_content_into_a_file(
            self.uncompressed_filename, self.content)
        write_endtime = time.time()
        write_total_time = write_endtime - write_starttime
        self.loghandler.logdata["data_write_and_process_time"] = f"{write_total_time:.2f}"

    def lempel_ziv_handle_uncompression(self):
        """A method to handle the steps of data uncompression. First data is transformed
        to tuples. Then the content is uncompressed.
        """
        self.transform_fetched_content_to_tuples()
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
        self.create_binary_version_of_content()

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

    def init_window_search(self, current_index: int) -> tuple:
        """A method to initialize the window search.

        Args:
            current_index (int): Index from which the sliding windows starts.

        Returns:
            tuple: result of compression (offset, length, next character)
        """
        window_start_index = max(0, current_index - self.window_size)
        window_end_index = current_index
        buffer_end_index = min(
            current_index + self.buffer_size, len(self.content))
        # result = self.find_longest_match(
        #     current_index,
        #     self.content[window_start_index:window_end_index],
        #     self.content[current_index:buffer_end_index])
        # result = self.find_matches_in_sliding_window(
        #     self.content[window_start_index:window_end_index],
        #     self.content[current_index:buffer_end_index])
        result = self.find_matches_in_sliding_window_with_built_in_find(
            window_start_index,
            current_index,
            buffer_end_index)
        return result

    # TODO: NOT CURRENTLY USED, REMOVE IF NOT NEEDED
    def find_longest_match(self, current_index: int, window: str, buffer: str) -> tuple:
        """A method to find the longest match in the sliding window

        Args:
            current_index (int): Index from which the sliding window starts
            window (str): content in the window area
            buffer (str): content in the lookahead buffer

        Returns:
            tuple: returns the match (offset, length, next character)
        """
        longest = (0, 0, 0)
        result = 0
        i = 0
        while i < len(window):
            match_length = self.repeating_length_recursion(window[i:], buffer)
            # match_length = self.find_matches_in_sliding_window(window[i:], buffer)
            if match_length > result:
                result = match_length
                offset = len(window) - i
                next_character = current_index + match_length
                if next_character >= len(self.content):
                    next_character = 0
                longest = (offset, match_length, ord(
                    self.content[next_character]))
            i += 1
        if result == 0:
            longest = (0, 1, ord(self.content[current_index]))
        return longest

    # TODO: CURRENTLY DEACTIVATED, REMOVE IF NOT NEEDED ANYMORE
    def repeating_length_recursion(self, window: str, string_buffer: str):
        """A recursion that finds the total length of the string match.

        This method was referenced from Tim Guite's tutorial:
        https://github.com/TimGuite/lz77/blob/master/python/compress.py

        Maximum recursion depth is the size of the lookahead buffer. Please
        be aware of this when configuring the buffer value.

        Args:
            window (str): the window from which matches are looked for
            string_buffer (str): the lookahead buffer for searching matches.

        Returns:
            int: lenght of match
        """
        if window == "" or string_buffer == "":
            return 0

        if window[0] == string_buffer[0]:
            return 1 + self.repeating_length_recursion(
                window[1:] + string_buffer[0], string_buffer[1:])
        return 0

    def find_matches_in_sliding_window(self, window: str, stringbuffer: str):
        """An iterative method to find the longest string match in a sliding window.

        Args:
            window (str): sliding window from which to search for matches.
            stringbuffer (str): lookahead buffer for which the longest match is searched
            for

        Returns:
            tuple: offset, match length and character, if no match is found.
        """
        len_window = len(window)
        window = window + stringbuffer
        i_window = 0
        i_buffer = 0
        len_buffer = len(stringbuffer)
        longest = (0, 0, 0)
        for i_window in range(len_window):
            result = 0
            if window[i_window] == stringbuffer[i_buffer]:
                result = 1
                for i in range(1, len_buffer):
                    if window[i_window + i] == stringbuffer[i]:
                        result += 1
                    else:
                        break
            if result > longest[1]:
                longest = (len_window - i_window, result, 0)
            if result == len_buffer - 1:
                break
        if longest[1] == 0:
            longest = (0, 1, ord(stringbuffer[0]))
        return longest

    def find_matches_in_sliding_window_with_pointers(
        self,
        window_start_index: int,
        buffer_start_index: int,
        buffer_end_index: int
    ):
        """An iterative method to find the longest string match in a sliding window.

        Args:
            window_start_index (int): index from which the sliding window begins.
            buffer_start_index (int): index from which the lookahead buffer start
            buffer_end_index (int): index in which the buffer and the sliding windows end.            

        Returns:
            tuple: offset, match length and character, if no match is found.
        """
        len_buffer = buffer_end_index - buffer_start_index
        longest = (0, 0, 0)
        for i_window in range(window_start_index, buffer_start_index):
            result = 0
            if self.content[i_window] == self.content[buffer_start_index]:
                result = 1
                for i_buffer in range(1, len_buffer):
                    if self.content[i_window + i_buffer] == self.content[buffer_start_index + i_buffer]:
                        result += 1
                    else:
                        break
            if result > longest[1]:
                longest = (buffer_start_index - i_window, result, 0)
            if result == len_buffer - 1:
                break
        if longest[1] == 0:
            longest = (0, 1, ord(self.content[buffer_start_index]))
        return longest

    def find_matches_in_sliding_window_with_built_in_find(
        self,
        window_start_index: int,
        buffer_start_index: int,
        buffer_end_index: int
    ):
        """An iterative method to find the longest string match in a sliding window.

        Args:
            window_start_index (int): index from which the sliding window begins.
            buffer_start_index (int): index from which the lookahead buffer start
            buffer_end_index (int): index in which the buffer and the sliding windows end.            

        Returns:
            tuple: offset, match length and character, if no match is found.
        """
        longest = (0, 0, 0)
        for i in range(buffer_start_index+2, buffer_end_index):
            found_index = self.content[window_start_index:buffer_start_index].find(
                self.content[buffer_start_index:i])
            if found_index != -1:
                longest = (buffer_start_index - (window_start_index +
                           found_index), i - buffer_start_index, 0)
            else:
                break

            # if self.content[i_window] == self.content[buffer_start_index]:
            #     result = 1
            #     for i_buffer in range(1, len_buffer):
            #         if self.content[i_window + i_buffer] == self.content[buffer_start_index + i_buffer]:
            #             result += 1
            #         else:
            #             break
            # if result > longest[1]:
            #     longest = (buffer_start_index - i_window, result, 0)
            # if result == len_buffer - 1:
            #     break
        if longest[1] == 0:
            longest = (0, 1, ord(self.content[buffer_start_index]))
        return longest

    def transform_fetched_content_to_tuples(self):
        """A method that transforms the fetched data into tuples.
        """

        self.compressed_content_as_list = []
        i = 0
        while i < len(self.compressed_content):
            offset = int(self.compressed_content[i:i+12], 2)
            length = int(self.compressed_content[i+12:i+16], 2)
            if offset == 0:
                character = chr(int(self.compressed_content[i+16:i+24], 2))
                i += 24
            else:
                character = ""
                i += 16
            self.compressed_content_as_list.append((offset, length, character))

    # TODO: Remove commented lines when not needed
    def lempel_ziv_uncompress(self):
        """A method to handle the uncompression of the data.

        Raises:
            NoCompressedContentError: A general error to be raised if no data is given.
        """
        if len(self.compressed_content_as_list) == 0:
            raise NoCompressedContentError()
        variable_n = len(self.compressed_content_as_list)
        # uncompressed_string = ""
        content = []
        for i in range(variable_n):
            if self.compressed_content_as_list[i][0] == 0:
                # uncompressed_string += self.compressed_content_as_list[i][2]
                content.append(self.compressed_content_as_list[i][2])
            else:
                variable_m = self.compressed_content_as_list[i][1]
                offset = self.compressed_content_as_list[i][0]
                for _ in range(variable_m):
                    # uncompressed_string += uncompressed_string[-offset]
                    content.append(content[-offset])
        uncompressed_string = "".join(content)
        self.content = uncompressed_string

    def analyze_compression(self, filepath=DEFAULT_DATA_PATH):
        """An initial method for creating analysis data on compression.
        """

        self.loghandler.logdata["original_filename"] = self.uncompressed_filename
        self.loghandler.logdata["compressed_filename"] = self.compressed_filename
        self.loghandler.logdata["compression_method"] = "Lempel-Ziv 77"
        self.loghandler.logdata["uncompressed_size"] = len(self.content) * 8
        self.loghandler.logdata["compressed_size"] = len(
            self.compressed_content)
        self.loghandler.create_compression_entry(filepath)

    def analyze_uncompression(self, filepath=DEFAULT_DATA_PATH):
        """An initial method for creating analysis data on compression.
        """

        self.loghandler.logdata["compressed_filename"] = self.compressed_filename
        self.loghandler.logdata["compressed_filename"] = self.uncompressed_filename
        self.loghandler.logdata["compression_method"] = "Lempel-Ziv 77"
        self.loghandler.logdata["uncompressed_size"] = len(self.content) * 8
        self.loghandler.logdata["compressed_size"] = len(
            self.compressed_content)
        self.loghandler.create_uncompression_entry(filepath)


if __name__ == "__main__":
    lz77 = LempelZiv77("filename.txt", "compressed_filename.txt")
    lz77.content = "ABCABCCCCDJSAJDSALOIWQEUIOQWENXCMXNCXZKJSHDASJDKLJASÖDLASOIEQUWOIEQWJLKDSJAÖLKDS"
    lz77.compress_content()
    lz77.lempel_ziv_uncompress()
