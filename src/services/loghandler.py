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
        """Initializes the log-file displayed in the TKinter
        Text-widgets.
        """
        if os.path.exists(self.tkinter_log):
            os.remove(self.tkinter_log)
        with open(self.tkinter_log, "a", encoding="utf-8") as file:
            file.close()

    def init_html_file(self):
        """Initializes the HTML-log file for reconstruction."""
        if os.path.exists(self.html_filename):
            os.remove(self.html_filename)
        with open(self.html_filename, "a", encoding="utf-8") as file:
            file.close()

    def init_csv_file(self):
        """Initializes the csv-log-file for new use.
        """
        if os.path.exists(self.data_csv):
            self.archive_csv_content(self.data_csv)
            os.remove(self.data_csv)
        with open(self.data_csv, "a", encoding="utf-8") as file:
            file.close()

    def archive_csv_content(self, filename: str):
        """Archives the content in the csv-file before overwriting the file.

        Args:
            filename (str): filename of the csv-log -file.
        """
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
Uncompressed_size: {logdata['uncompressed_size']} bytes\n\
Compressed size: {logdata['compressed_size']} bytes\n"""
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
        """A method that handles calling the methods that create the content
        for the HTML-log file.

        Args:
            total_time (str): Total time used for running tests.
            success (str): The number of tests that were successful
            fail (str): The number of failed tests
        """

        with open(self.html_filename, "a", encoding="utf_8") as file:

            file.write(
                self._create_forewords_for_html_log()
            )
            file.write(
                self._create_overview_data_for_html_log(
                    total_time, success, fail)
            )
            file.write(
                self._create_tables_for_html_log()
            )
            file.write(
                self._create_graphs_for_html_log()
            )

    def _create_forewords_for_html_log(self) -> str:
        """Creates the forewords for the HTML-log file.

        Returns:
            str: created content as a string
        """
        log_time = datetime.now()
        log_time_strf = log_time.strftime("%d.%m.%Y %H:%M:%S")
        forewords = f"\
<h1>ANALYSIS REPORT</h1>\n\
<p>This document contains a report for the analysis testing executed on \
<b>{log_time_strf}</b>. The included tables contain information on compression and \
uncompression phases. Graphs visualize perfomance of compression algorithms based on \
selected measurers. Note that running the analysis tests overwrites the report.</p>\n\n\
<h2>OVERVIEW</h2>\n\n"
        return forewords

    def _create_overview_data_for_html_log(self, total_time, success, fail) -> str:
        """Creates the HTML-content with the overview analysis of tests run.

        Returns:
            str: created content as a string
        """
        analysis = f"""<b>Total runtime:</b> {total_time} seconds<br>\n\
<b>Tests run:</b> {success + fail}<br>\n\
<ul>\n\
    <li><b>Successful tests:</b> {success}<br></li>\n\
    <li><b>Failed tests:</b> {fail}<br></li>\n\
</ul>\n\n\
<h2>DETAILED SUMMARY</h2>\n\n"""
        return analysis

    def _create_tables_for_html_log(self) -> str:
        """Creates the HTML-content related to the tables

        Returns:
            str: content as a string
        """
        tables = "<h3>Tables</h3>\n\
<p>The tables contain detailed information on compression and uncompression \
phases. The sought after compression ratio for this project was 0.4-0.6. \
The files on which this compression ratio was less than or equal to 0.6 are \
colored green and other are colored red.</p>\n\n\
<h4>Compression analysis</h4>\n"
        tables += self._create_html_compression_table()
        tables += "<h4>Uncompression analysis</h4>\n\n"
        tables += self._create_html_uncompression_table()
        tables += "<br>\n"
        return tables

    def _create_graphs_for_html_log(self) -> str:
        """Constructs the HTML-content related to the graphs.

        Returns:
            str: created content as a string
        """
        graphs = "<h3>Graphs</h3>\n\
<p>Below you can review visual comparison of test results. The labels indicate the \
number of the file in question. Filenames can be found with the number from the tables \
above.</p>\n"
        bar_chart_filename = self._create_compression_ratio_bar_chart()
        graphs += f"<img src='{bar_chart_filename}' alt='Compression ratio comparison'>\
</img><br>\n"
        graphs += self.graph_management.graph_explanations["compression-ratio"]
        huffman_frequency_bar_chart = self._create_huffman_frequency_bar_chart()
        graphs += f"<img src='{huffman_frequency_bar_chart}' \
alt='Huffman frequency variances'></img><br>\n"
        graphs += self.graph_management.graph_explanations["huffman-frequency-variance"]
        huffman_character_count_graph = self._create_huffman_character_count_chart()
        graphs += f"<img src='{huffman_character_count_graph}' \
alt='Huffman character count'></img><br>\n"
        graphs += self.graph_management.graph_explanations["huffman-character-count"]
        lempel_ziv_avg_match = self._create_lempel_ziv_bar_chart()
        graphs += f"<img src='{lempel_ziv_avg_match}' alt='Lempel-Ziv average match length'>\
</img><br>\n"
        graphs += self.graph_management.graph_explanations["lempel-ziv-mean-length"]
        lempel_ziv_avg_offset = self._create_lempel_ziv_offset_bar_chart()
        graphs += f"<img src='{lempel_ziv_avg_offset}' alt='Lempel-Ziv average offset length'>\
</img><br>\n"
        graphs += self.graph_management.graph_explanations["lempel-ziv-mean-offset"]
        return graphs

    def _create_compression_ratio_bar_chart(self) -> str:
        """Creates a bar chart detailing the compression ratio comparison
        between Huffman coding and LZ77.

        Returns:
            str: path for the graph created.
        """
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

    def _create_huffman_frequency_bar_chart(self) -> str:
        """Handles calling fo the constructin of a bar chart detailing
        the frequencies for the Huffman compression

        Returns:
            str: path to the graph created.
        """
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

    def _create_huffman_character_count_chart(self) -> str:
        """Handles calling for the constructin of a bar chart detailing
        the character counts for the Huffman compression.

        Returns:
            str: path to the graph created.
        """
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

    def _create_lempel_ziv_bar_chart(self) -> str:
        """Handles calling for the construction of bar chart detailing
        the mean lengths for LZ77 compression.

        Returns:
            str: returns path to the graph as a string
        """
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

    def _create_lempel_ziv_offset_bar_chart(self) -> str:
        """Handles calling for construction of a bar chart.

        Returns:
            str: filename to the graph created
        """
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

    def _create_html_compression_table(self) -> str:
        """Creates an HTML table of the compression analysis data.

        Returns:
            str: HTML-table as a string
        """
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

    def _create_html_uncompression_table(self) -> str:
        """Creates an HTML-table of the uncompression results."""
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
        """Writes log data for uncompression event for the Tkinter Text-widget.

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
Compressed size: {logdata['compressed_size']} bytes\n\
Uncompressed_size: {logdata['uncompressed_size']} bytes\n"""
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
        """Creates a single log entry. This method is called when using
        the compression view to just create a log entry for the Tkinter
        Text widget.

        Args:
            logdata (dict): data from which the entry is created
        """
        self.create_compression_entry(logdata)

    def single_tkinter_uncompression_log_entry(self, logdata: dict):
        """Creates a single log entry. This method is called when using
        the compression view to just create a log entry for the Tkinter
        Text widget.

        Args:
            logdata (dict): data from which the entry is created
        """
        self.create_uncompression_entry(logdata)


default_loghandler = LogHandler()
