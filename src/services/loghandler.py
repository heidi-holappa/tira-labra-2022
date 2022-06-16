from datetime import datetime
import os
from config import DEFAULT_DATA_PATH
from config import DEFAULT_TEST_DATA_PATH


class LogHandler:
    """A class to handle creating log entries.
    """

    def __init__(self) -> None:
        """Constructor for the class. Uses the default data path defined
        in the .env file.
        """
        self.filename = os.path.join(DEFAULT_TEST_DATA_PATH, "compression.log")
        self.html_filename = os.path.join(DEFAULT_TEST_DATA_PATH,"compression-log.html")
        self.archive_filename = os.path.join(DEFAULT_TEST_DATA_PATH,"compression_archive.log")
        self.data_csv = os.path.join(DEFAULT_TEST_DATA_PATH,"uncompress-log.csv")
        self.logdata = {
            "original_filename": "",
            "compressed_filename": "",
            "uncompressed_filename": "",
            "compression_method": "",
            "uncompressed_size": 0,
            "compressed_size": 0,
            "compression_time": "",
            "uncompression_time": "",
            "data_fetch_and_process_time": "",
            "data_write_and_process_time": "",
        }

        self.init_log_file()
        self.init_html_file()

    def init_log_file(self):
        
        if os.path.exists(self.filename):
            os.remove(self.filename)
        with open(self.filename, "a", encoding="utf-8") as file:
            file.close()

    def init_html_file(self):
        if os.path.exists(self.html_filename):
            os.remove(self.html_filename)
        with open(self.html_filename, "a", encoding="utf-8") as file:
            file.close()
        if os.path.exists(self.data_csv):
            self.archive_log_content(self.data_csv)
            os.remove(self.data_csv)
        with open(self.data_csv, "a", encoding="utf-8") as file:
            file.close()
            

    def archive_log_content(self, filename):
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

        if not os.path.exists(self.filename):
            with open(self.filename, "a", encoding="utf-8") as file:
                file.close()
        
        
        
        compression_ratio = int(logdata['compressed_size']) / \
                int(logdata['uncompressed_size']) * 100

        with open(self.filename, "a", encoding="utf-8") as file:
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
            analysis = f"""-<H2>EXTENSIVE TEST SUMMARY</H2><br>\n\
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
    
    def create_html_compression_table(self):
        compression_log = "\
<table border='1'>\n\
    <tr>\n\
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
            for row in data_as_rows:
                data = row.split(";")
                if data[15] == "0":
                    if float(data[6]) <= 0.6:
                        color = "green"
                    else:
                        color = "red"
                    compression_log += f"\
    <tr>\n\
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
            for row in data_as_rows:
                data = row.split(";")
                if data[15] == "1":
                    if float(data[6]) <= 0.6:
                        color = "green"
                    else:
                        color = "red"
                    uncompression_log += f"\
    <tr>\n\
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

        if not os.path.exists(self.filename):
            with open(self.filename, "a", encoding="utf-8") as file:
                file.close()

        with open(self.filename, "a", encoding="utf-8") as file:
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

default_loghandler = LogHandler()