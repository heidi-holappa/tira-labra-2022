from datetime import datetime
import os
from config import DEFAULT_TEST_DATA_PATH
from config import HTML_LOG
from config import CSV_LOG
from config import ARCHIVE_LOG
from config import TKINTER_LOG
from services.graphmanagement import default_graph_manager


class LogHandler:
    """A class to handle creating log entries.
    """

    def __init__(self) -> None:
        """Constructor for the class. Uses the default data path defined
        in the .env file.
        """
        self.tkinter_log = os.path.join(DEFAULT_TEST_DATA_PATH, TKINTER_LOG)
        self.html_filename = os.path.join(
            DEFAULT_TEST_DATA_PATH, HTML_LOG)
        self.archive_filename = os.path.join(
            DEFAULT_TEST_DATA_PATH, ARCHIVE_LOG)
        self.data_csv = os.path.join(
            DEFAULT_TEST_DATA_PATH, CSV_LOG)
        self.graph_management = default_graph_manager
        self.init_tkinter_log_file()

    def init_tkinter_log_file(self):
        if os.path.exists(self.tkinter_log):
            os.remove(self.tkinter_log)
        with open(self.tkinter_log, "a", encoding="utf-8") as file:
            file.close()

    def init_html_file(self):
        if os.path.exists(self.html_filename):
            os.remove(self.html_filename)
        with open(self.html_filename, "a", encoding="utf-8") as file:
            file.close()

    def init_csv_file(self):
        if os.path.exists(self.data_csv):
            self.archive_csv_content(self.data_csv)
            os.remove(self.data_csv)
        with open(self.data_csv, "a", encoding="utf-8") as file:
            file.close()

    def archive_csv_content(self, filename):
        content = ""
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()
        with open(self.archive_filename, "a", encoding="utf-8") as file:
            file.write(content)

    def write_csv_entry_to_file(self, logentry):
        with open(self.data_csv, "a", encoding="utf-8") as file:
            file.write(logentry + "\n")

    def create_compression_entry(self,
                                 logdata: dict) -> None:
        """Creates a log entry with the given values. Basic information is
        collected from both compressin methods (Huffman coding, LZ77). Additional
        log-content can also be given.

        Args:
            additional_content (str, optional): Additional algorithm specific content.
            Defaults to "".
        """

        if not os.path.exists(self.tkinter_log):
            with open(self.tkinter_log, "a", encoding="utf-8") as file:
                file.close()

        compression_ratio = int(logdata['compressed_size']) / \
            int(logdata['uncompressed_size']) * 100

        with open(self.tkinter_log, "a", encoding="utf-8") as file:
            log_time = datetime.now()
            log_time_strf = log_time.strftime("%d.%m.%Y %H:%M:%S")
            content = f"""------ NEW ENTRY: COMPRESSING DATA ------\n\
Log entry created: {log_time_strf}\n\
File accessed: {logdata['original_filename']}\n\
File created: {logdata['compressed_filename']}\n\
Compression method: {logdata['compression_method']}\n\
Uncompressed_size: {logdata['uncompressed_size']} bits\n\
Compressed size: {logdata['compressed_size']} bits\n"""
            content += f"Compression ratio: {compression_ratio:.2f}\n"
            content += f"""Time used for fetching and processing data: \
{logdata['data_fetch_and_process_time']} seconds\n\
Time used for compression: {logdata['compression_time']}\n\
Time used for writing and processing data: \
{logdata['data_write_and_process_time']} seconds\n"""
            file.write(content)
            file.write("------ END OF ENTRY ------\n\n")

    def create_html_file(self,
                         total_time,
                         success,
                         fail):
        log_time = datetime.now()
        log_time_strf = log_time.strftime("%d.%m.%Y %H:%M:%S")
        with open(self.html_filename, "a", encoding="utf_8") as file:
            forewords = f"\
<h1>Extended testing report</h1><br>\n\
<p>This document includes a report of the extended testing executed on \
<b>{log_time_strf}</b>. The tables include information on compression and \
uncompression of test files. You can also find graphs that measure perfomance \
of compression algorithms based on selected measurers. Note that running the \
extended tests overwrites the report.</p><br>\n\n"
            file.write(forewords)
            analysis = f"""<H2>EXTENSIVE TEST SUMMARY</H2><br>\n\
<b>Total runtime:</b> {total_time} seconds<br>\n\
<b>Successful tests:</b> {success}<br>\n\
<b>Failed tests:</b> {fail}<br>\n\n\
<h2>Detailed summary</h2><br>\n\n"""
            file.write(analysis)
            compression_table = self.create_html_compression_table()
            uncompression_table = self.create_html_uncompression_table()
            file.write(compression_table)
            file.write("<br>\n")
            file.write(uncompression_table)
            file.write("<h2>Graphs</h2>\n\
<p>Below you can review visual comparison of test results. The labels indicate the \
number of the file in question. Filenames can be found with the number from the tables \
above.</p>\n")
            bar_chart_filename = self.create_compression_ratio_bar_chart()
            file.write(f"<img src='{bar_chart_filename}' alt='Compression ratio comparison'>\
</img><br>\n")
            file.write(self.graph_management.graph_explanations["compression-ratio"])
            huffman_frequency_bar_chart = self.create_huffman_frequency_bar_chart()
            file.write(f"<img src='{huffman_frequency_bar_chart}' \
alt='Huffman frequency variances'></img><br>\n")
            file.write(self.graph_management.graph_explanations["huffman-frequency-variance"])
            huffman_character_count_graph = self.create_huffman_character_count_chart()
            file.write(f"<img src='{huffman_character_count_graph}' \
alt='Huffman character count'></img><br>\n")
            file.write(self.graph_management.graph_explanations["huffman-character-count"])
            lempel_ziv_avg_match = self.create_lempel_ziv_bar_chart()
            file.write(f"<img src='{lempel_ziv_avg_match}' alt='Lempel-Ziv average match length'>\
</img><br>\n")
            file.write(self.graph_management.graph_explanations["lempel-ziv-mean-length"])
            lempel_ziv_avg_offset = self.create_lempel_ziv_offset_bar_chart()
            file.write(f"<img src='{lempel_ziv_avg_offset}' alt='Lempel-Ziv average offset length'>\
</img><br>\n")
            file.write(self.graph_management.graph_explanations["lempel-ziv-mean-offset"])

    def create_compression_ratio_bar_chart(self):
        with open(self.data_csv, "r", encoding="utf-8") as file:
            content = file.read()
            data_as_rows = content.split("\n")[:-1]
        huffman_ratio = []
        lempelziv_ratio = []
        labels = []
        for row in data_as_rows:
            data = row.split(";")
            if data[16] == "0":
                if data[0][0] == "H":
                    huffman_ratio.append(float(data[6]))
                else:
                    lempelziv_ratio.append(float(data[6]))
                if data[1] not in labels:
                    labels.append(data[1])
        filename = self.graph_management.construct_compression_ratio_bar_chart(
            huffman_ratio,
            lempelziv_ratio,
            labels)
        return filename

    def create_huffman_frequency_bar_chart(self):
        with open(self.data_csv, "r", encoding="utf-8") as file:
            content = file.read()
            data_as_rows = content.split("\n")[:-1]
        huffman_frequency_variance = []
        for row in data_as_rows:
            data = row.split(";")
            if data[16] == "0":
                if data[0][0] == "H":
                    huffman_frequency_variance.append(float(data[13]))
        filename = self.graph_management.construct_huffman_frequency_variance_bar_chart(
            huffman_frequency_variance)
        return filename

    def create_huffman_character_count_chart(self):
        with open(self.data_csv, "r", encoding="utf-8") as file:
            content = file.read()
            data_as_rows = content.split("\n")[:-1]
        huffman_character_count = []
        for row in data_as_rows:
            data = row.split(";")
            if data[16] == "0":
                if data[0][0] == "H":
                    huffman_character_count.append(float(data[17]))
        filename = self.graph_management.construct_huffman_character_count_bar_chart(
            huffman_character_count)
        return filename

    def create_lempel_ziv_bar_chart(self):
        with open(self.data_csv, "r", encoding="utf-8") as file:
            content = file.read()
            data_as_rows = content.split("\n")[:-1]
        lempel_ziv_avg_match = []
        for row in data_as_rows:
            data = row.split(";")
            if data[16] == "0":
                if data[0][0] == "L":
                    lempel_ziv_avg_match.append(float(data[14]))
        filename = self.graph_management.construct_lempel_ziv_average_length_bar_chart(
            lempel_ziv_avg_match)
        return filename

    def create_lempel_ziv_offset_bar_chart(self):
        with open(self.data_csv, "r", encoding="utf-8") as file:
            content = file.read()
            data_as_rows = content.split("\n")[:-1]
        lempel_ziv_avg_offset = []
        for row in data_as_rows:
            data = row.split(";")
            if data[16] == "0":
                if data[0][0] == "L":
                    lempel_ziv_avg_offset.append(float(data[15]))
        filename = self.graph_management.construct_lempel_ziv_average_offset_bar_chart(
            lempel_ziv_avg_offset)
        return filename

    def create_html_compression_table(self):
        compression_log = "\
<table border='1'>\n\
    <tr>\n\
        <th>#</th>\n\
        <th>Filename</th>\n\
        <th>Algorithm</th>\n\
        <th>Original size</th>\n\
        <th>Compressed size</th>\n\
        <th>Compression ratio</th>\n\
        <th>Compression time (s)</th>\n\
        <th>Pre-process (s)</th>\n\
        <th>Post-process (s)</th>\n\
    </tr><br>\n"
        with open(self.data_csv, "r", encoding="utf-8") as file:
            content = file.read()
            data_as_rows = content.split("\n")[:-1]
        with open(self.html_filename, "a", encoding="utf-8") as file:
            file_number = -1
            for row in data_as_rows:
                data = row.split(";")
                if data[16] == "0":
                    file_number += 1
                    if float(data[6]) <= 0.6:
                        color = "green"
                    else:
                        color = "red"
                    compression_log += f"\
    <tr>\n\
        <th>{file_number // 2 + 1}</th>\n\
        <td>{data[1]}</td>\n\
        <td>{data[0]}</td>\n\
        <td>{data[4]}</td>\n\
        <td>{data[5]}</td>\n\
        <td style='color:{color};text-align: center'>{data[6]}</style></td>\n\
        <td style='text-align: center'>{data[7]}</td>\n\
        <td style='text-align: center'>{data[9]}</td>\n\
        <td style='text-align: center'>{data[10]}</td>\n\
    </tr>\n"
        compression_log += "</table>\n"
        return compression_log

    def create_html_uncompression_table(self):
        uncompression_log = "\
<table border='1'>\n\
    <tr cellspacing='3'>\n\
        <th>#</th>\n\
        <th>Filename</th>\n\
        <th>Algorithm</th>\n\
        <th>Original size</th>\n\
        <th>Compressed size</th>\n\
        <th>Compression ratio</th>\n\
        <th>Uncompression time (s)</th>\n\
        <th>Pre-process (s)</th>\n\
        <th>Post-process (s)</th>\n\
    </tr>\n"
        with open(self.data_csv, "r", encoding="utf-8") as file:
            content = file.read()
            data_as_rows = content.split("\n")[:-1]
        with open(self.html_filename, "a", encoding="utf-8") as file:
            file_number = -1
            for row in data_as_rows:
                data = row.split(";")
                if data[16] == "1":
                    file_number += 1
                    if float(data[6]) <= 0.6:
                        color = "green"
                    else:
                        color = "red"
                    uncompression_log += f"\
    <tr>\n\
        <th>{file_number // 2 + 1}</th>\n\
        <td>{data[2]}</td>\n\
        <td>{data[0]}</td>\n\
        <td>{data[4]}</td>\n\
        <td>{data[5]}</td>\n\
        <td style='color:{color};text-align: center'>{data[6]}</style></td>\n\
        <td style='text-align: center'>{data[7]}</td>\n\
        <td style='text-align: center'>{data[9]}</td>\n\
        <td style='text-align: center'>{data[10]}</td>\n\
    </tr>\n"
        uncompression_log += "</table>\n"

        return uncompression_log

    def create_uncompression_entry(self,
                                   logdata: dict) -> None:
        """Writes log data for uncompression event.

        Args:
            additional_content (str, optional): Optional additional information. Defaults to "".
        """

        if not os.path.exists(self.tkinter_log):
            with open(self.tkinter_log, "a", encoding="utf-8") as file:
                file.close()

        with open(self.tkinter_log, "a", encoding="utf-8") as file:
            log_time = datetime.now()
            log_time_strf = log_time.strftime("%d.%m.%Y %H:%M:%S")
            content = f"""------ NEW ENTRY: UNCOMPRESSING DATA ------\n\
Log entry created: {log_time_strf}\n"\
File accessed: {logdata['compressed_filename']}\n\
File created: {logdata['uncompressed_filename']}\n\
Compression method: {logdata['compression_method']}\n\
Compressed size: {logdata['compressed_size']} bits\n\
Uncompressed_size: {logdata['uncompressed_size']} bits\n"""
            compression_ratio = int(logdata['compressed_size']) / \
                int(logdata['uncompressed_size']) * 100
            content += f"""Compression ratio: {compression_ratio:.2f}\n\
Time used for fetching and processing data: \
{logdata['data_fetch_and_process_time']} seconds\n\
Time used for compression: {logdata['compression_time']} seconds\n\
Time used for writing and processing data: \
{logdata['data_write_and_process_time']} seconds\n"""
            file.write(content)
            file.write("------ END OF ENTRY ------\n\n")


    def single_tkinter_compression_log_entry(self, logdata: dict):
        self.create_compression_entry(logdata)
    
    def single_tkinter_uncompression_log_entry(self, logdata: dict):
        self.create_uncompression_entry(logdata)


default_loghandler = LogHandler()
