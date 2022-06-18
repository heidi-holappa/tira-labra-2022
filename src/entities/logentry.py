class LogEntry:

    def __init__(self):
        self.logdata = {
            "compression_method": "",
            "original_filename": "",
            "compressed_filename": "",
            "uncompressed_filename": "",
            "uncompressed_size": "",
            "compressed_size": "",
            "compression_ratio": "",
            "compression_time": "",
            "uncompression_time": "",
            "data_fetch_and_process_time": "",
            "data_write_and_process_time": "",
            "huffman_max_frequency": "",
            "huffman_min_frequency": "",
            "huffman_freq_variance": "",
            "lz_avg_match_length": "",
            "lz_mean_offset": "",
            "action": ""
        }


    def get_logdata_as_csv_row(self):
        logdata_as_list = []
        for value in self.logdata.values():
            logdata_as_list.append(value)
        csv_data = ";".join(logdata_as_list)
        return csv_data
    
    def get_test_data_as_csv_row(self):
        logdata_as_list = []
        for key, value in self.logdata.items():
            if key == "uncompressed_filename":
                continue
            logdata_as_list.append(value)
        csv_data = ";".join(logdata_as_list)
        return csv_data


# if __name__ == "__main__":
    # l = LogEntry()
    # l.logdata["compression_method"] = "1"
    # l.logdata["original_filename"] = "file.txt"
    # l.logdata["compressed_filename"] = "file.lz"
    # l.logdata["uncompressed_filename"] = "file_uncompressed.txt"
    # l.logdata["uncompressed_size"] = "23454"
    # l.logdata["compressed_size"] = "17584"
    # l.logdata["compression_ratio"] = "75.0"
    # l.logdata["compression_time"] = "0.75"
    # l.logdata["uncompression_time"] = "0.02"
    # l.logdata["data_fetch_and_process_time"] = "2.9"
    # l.logdata["data_write_and_process_time"] = "0.1"
    # l.logdata["huffman_max_fequency"] = "0.3"
    # l.logdata["huffman_min_frequency"] = "0.00001"
    # l.logdata["huffman_freq_variance"] = "0.23"
    # l.logdata["lz_avg_match_length"] = "0"
    # print(l.get_logdata_as_csv_row())
    # print(l.get_test_data_as_csv_row())
    