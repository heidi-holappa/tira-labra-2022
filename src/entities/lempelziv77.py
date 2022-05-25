# STILL A DRAFT. BUILDING THIS ON WEEK 3
import string

class LempelZiv77:

    def __init__(self, uncompressed_filename: str, compressed_filename: str):
        self.uncompressed_filename = uncompressed_filename
        self.compressed_filename = compressed_filename
        self.content = ""
        self.compressed_content = ""
        self.window_size = 10
        self.buffer_size = 15

    
    def fetch_uncompressed_content(self):
        with open(self.uncompressed_filename, encoding="utf-8") as source_content:
            self.content = source_content.read()


    def write_compressed_content_into_a_file(self):
        pass

    def lempel_ziv_activate_compression(self):
        self.fetch_uncompressed_content()
        self.compress_content()
        self.write_compressed_content_into_a_file()

    def compress_content(self):
        compressed_content_as_list = []
        i = 0
        while i < len(self.content):
            result = self.init_window_search(i)
            compressed_content_as_list.append(result)
            i += result[1]
        for i in compressed_content_as_list:
            print(i)

    def init_window_search(self, current_index: int) -> tuple:
        window_start_index = max(0, current_index - self.window_size)
        window_end_index = current_index
        buffer_end_index = min(current_index + self.buffer_size, len(self.content))
        result = self.find_longest_match(current_index, self.content[window_start_index:window_end_index], self.content[current_index:buffer_end_index])
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
                longest = (offset, match_length, self.content[next_character])
            i += 1
        if result == 0:
            longest = (0, 1, self.content[current_index])
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



if __name__ == "__main__":
    lz77 = LempelZiv77("filename.txt", "compressed_filename.txt")
    lz77.content = "ABCABCCCCDJSAJDSALOIWQEUIOQWENXCMXNCXZKJSHDASJDKLJASÖDLASOIEQUWOIEQWJLKDSJAÖLKDS"
    lz77.compress_content()
    # print(lz77.compressed_content)


