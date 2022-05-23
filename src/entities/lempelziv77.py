from bz2 import compress


class LempelZiv77:

    def __init__(self, uncompressed_filename: str, compressed_filename: str):
        self.uncompressed_filename = uncompressed_filename
        self.compressed_filename = compressed_filename
        self.content = ""
        self.compressed_content = ""
        self.window = 400
        self.buffer = 15

    
    def fetch_uncompressed_content(self):
        with open(self.uncompressed_filename, encoding="utf-8") as source_content:
            self.content = source_content.read()

    def compress_content(self):
        i = 0
        while i < len(self.content):
            
            pass
    
    def find_longest_match(self, i):
        buffer_index = min(self.buffer, len(self.content)-1)
        window_index = max(0, i - self.window)
        pass



    def write_compressed_content_into_a_file(self):
        pass


    def lempel_ziv_activate_compression(self):
        self.fetch_uncompressed_content()
        self.compress_content()
        self.write_compressed_content_into_a_file()

if __name__ == "__main__":
    lz77 = LempelZiv77("filename.txt", "compressed_filename.txt")
    lz77.content = "ABCABCCCC"
    lz77.compress_content()
    print(lz77.compressed_content)
