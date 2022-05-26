import string

from services.filemanagement import default_file_manager

class NoCompressedContentError(Exception):
    pass


class LempelZiv77:

    def __init__(self, uncompressed_filename: str, compressed_filename: str):
        self.uncompressed_filename = uncompressed_filename
        self.compressed_filename = compressed_filename
        self.content = ""
        self.compressed_content = ""
        self.compressed_content_as_list = []
        self.window_size = 4095
        self.buffer_size = 15
        self.file_manager = default_file_manager
        

    def fetch_uncompressed_content(self):
        self.content = self.file_manager.fetch_uncompressed_content(self.uncompressed_filename)
    
    def fetch_compressed_content(self):
        compressed_content_as_bytes: bytes = self.file_manager.fetch_compressed_content(self.compressed_filename)
        self.tranform_bytes_into_string(compressed_content_as_bytes)

    def tranform_bytes_into_string(self, byte_data):
        for byte in byte_data:
            self.compressed_content += str(bin(byte)[2:].zfill(8))

    def write_txt_content_into_a_file(self, filename, content_to_write):
        self.file_manager.create_txt_file(filename, content_to_write)

    def write_binary_content_into_a_file(self, filename, content_to_write):
        self.file_manager.create_binary_file(filename, content_to_write)

    def lempel_ziv_activate_compression(self):
        self.fetch_uncompressed_content()
        self.compress_content()
        self.write_binary_content_into_a_file(self.compressed_filename, self.bytearray_data)

    def lempel_ziv_activate_uncompression(self):
        self.fetch_compressed_content()
        self.lempel_ziv_handle_uncompression()
        self.write_txt_content_into_a_file(self.uncompressed_filename, self.content)

    def lempel_ziv_handle_uncompression(self):
        self.transform_fetched_content_to_tuples()
        self.lempel_ziv_uncompress()

    def compress_content(self):
        self.compressed_content_as_list = []
        i = 0
        while i < len(self.content):
            result = self.init_window_search(i)
            self.compressed_content_as_list.append(result)
            i += result[1]
        self.create_binary_version_of_content()


    def create_binary_version_of_content(self):
        self.compressed_content = ""
        self._bytearray_list = []
        for member in self.compressed_content_as_list:
            offset = member[0]
            match_length = member[1]
            next_character = member[2]
            self.compressed_content += str(bin(offset)[2:].zfill(12))
            self.compressed_content += str(bin(match_length)[2:].zfill(4))
            self.compressed_content += str(bin(next_character)[2:].zfill(8))
        for i in range(0, len(self.compressed_content), 8):
            value = ord(chr(int(self.compressed_content[i:i+8], 2)))
            self._bytearray_list.append(value)
        self.bytearray_data = bytearray(self._bytearray_list)


    def init_window_search(self, current_index: int) -> tuple:
        window_start_index = max(0, current_index - self.window_size)
        window_end_index = current_index
        buffer_end_index = min(
            current_index + self.buffer_size, len(self.content))
        result = self.find_longest_match(
            current_index, self.content[window_start_index:window_end_index], self.content[current_index:buffer_end_index])
        return result

    def find_longest_match(self, current_index: int, window: str, buffer: str) -> tuple:
        longest = (0, 0, 0)
        result = 0
        i = 0
        while i < len(window):
            # print("Window pointer: ", max(0, current_index - self.window_size) + i, "character: ", self.content[current_index + i], "Buffer: ", current_index + len(window), "buffer_character: ", self.content[current_index + len(window)] )
            match_length = self.repeating_length_recursion(window[i:], buffer)
            if match_length > result:
                result = match_length
                offset = len(window) - i
                next_character = current_index + match_length
                if next_character >= len(self.content):
                    next_character = 0
                longest = (offset, match_length, ord(self.content[next_character]))
            i += 1
        if result == 0:
            longest = (0, 1, ord(self.content[current_index]))
        return longest

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
            return 1 + self.repeating_length_recursion(window[1:] + string_buffer[0], string_buffer[1:])
        else:
            return 0        

    def transform_fetched_content_to_tuples(self):
        # print("now transforming", self.compressed_content)

        self.compressed_content_as_list = []
        i = 0
        while i < len(self.compressed_content):
            offset = int(self.compressed_content[i:i+12], 2)
            length = int(self.compressed_content[i+12:i+16], 2)
            character = chr(int(self.compressed_content[i+16:i+24], 2))
            self.compressed_content_as_list.append((offset, length, character))
            i += 24
        print(self.compressed_content_as_list)

    
    def lempel_ziv_uncompress(self):
        # print(self.compressed_content_as_list)
        if len(self.compressed_content_as_list) == 0:
            raise NoCompressedContentError()
        n = len(self.compressed_content_as_list)
        uncompressed_string = ""
        for i in range(n):
            if self.compressed_content_as_list[i][0] == 0:
                uncompressed_string += self.compressed_content_as_list[i][2]
            else:
                m = self.compressed_content_as_list[i][1]
                offset = self.compressed_content_as_list[i][0]
                for i in range(m):
                    uncompressed_string += uncompressed_string[-offset]
        self.content = uncompressed_string
        # match = True
        # for i in range(len(uncompressed_string)):
        #     if uncompressed_string[i] != self.content[i]:
        #         match = False
        # print(uncompressed_string, match)


if __name__ == "__main__":
    lz77 = LempelZiv77("filename.txt", "compressed_filename.txt")
    lz77.content = "ABCABCCCCDJSAJDSALOIWQEUIOQWENXCMXNCXZKJSHDASJDKLJASÖDLASOIEQUWOIEQWJLKDSJAÖLKDS"
    lz77.compress_content()
    lz77.lempel_ziv_uncompress()
    # print(lz77.compressed_content)
