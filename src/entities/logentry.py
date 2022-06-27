class LogEntry:
    """Creates an object instance of the current log entry.
    """

    def __init__(self):
        """Constructor for the class. For the purposes of this project
        a dictionary containing the log values was sufficient. There are
        however quality issues with this solution, as updating the code
        contains risks, because the data is fetched from a csv without
        value keys.

        A good upgrade would be to include the keys into the start of
        the log and the match values with keys when retrieving data.
        """
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
            "action": "",
            "huffman-character-count": ""
        }

    def get_logdata_as_csv_row(self) -> str:
        """Returns a csv-compatible version of the logdata.

        Returns:
            str: logdata separated with semicolons.
        """
        logdata_as_list = []
        for value in self.logdata.values():
            logdata_as_list.append(value)
        csv_data = ";".join(logdata_as_list)
        return csv_data
