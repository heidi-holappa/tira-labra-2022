import os
import matplotlib.pyplot as pyplt
import numpy as np
from config import DEFAULT_TEST_GRAPH_FOLDER
from config import IMG_COMPRESS_RATIO
from config import IMG_HUFFMAN_FREQ
from config import IMG_HUFFMAN_CHAR_COUNT
from config import IMG_LZ_MEAN_MATCH
from config import IMG_LZ_MEAN_OFFSET


class GraphManagement:
    """A class that handles constructing graphs for the HTML-log.
    """

    def __init__(self):
        """Constructor for the class.
        """
        self.graph_folder = DEFAULT_TEST_GRAPH_FOLDER
        img_folder_split = DEFAULT_TEST_GRAPH_FOLDER.split("/")
        self.img_folder = img_folder_split[-1] + "/"
        self.graph_explanations = {
            "compression-ratio": "<p>Compression ratio is the <b>size ratio</b> between the \
uncompressed and compressed content. For instance a ratio of 0.5 would mean that the compressed \
file's size is 50 percent of the file size of the uncompressed file. For both Huffman Coding and \
Lempel-Ziv 77 the compression ratio is worse for files with random content. You can read more \
about the reasons for this in the 'Implementation documentation'. Link can be found in the \
README.md.</p>\n",
            "huffman-character-count": "<p>With a high character count the role of \
higher frequency variance is more visible. With a small character count (for instance \
files with just few different characters) a very high compression ratio can be achieved, \
even with low frequency variance.</p>\n",
            "huffman-frequency-variance": "<p>The graph above describes the variance \
in the Huffman frequencies. As can be seen with the test content, the compression ratio \
is generally better with content that has a higher variance in the frequencies, but there \
are exceptions. You can read more about the reasons for this in the 'Implementation \
documentation'. Link can be found in the README.md.</p>\n",
            "lempel-ziv-mean-length": "<p>The average length describes the length \
of the match found in the sliding window. When the average length is higher, the \
compression ratio is generally better. Note that the mean value is only calculated for \
found matches. Indexes for which no match was found are not included in the mean value. </p>\n",
            "lempel-ziv-mean-offset": "The offset is the difference in indexes \
between the matches. For the included test material the offset is generally around \
1200-1400 characters. Currently 12 bits (0-4096) are reserved for storing the offset, \
but perhaps two bits less would suffice in most cases? \
This could possibly improve the compression ratio.</p>\n"
        }

    def construct_huffman_frequency_variance_bar_chart(self, x_values: list) -> str:
        """Constructs a frequency variance bar chart for Huffman coding

        Args:
            x_values (list): a list of float values

        Returns:
            str: relative path of the created file
        """
        pyplt.figure(1)
        freq_index = np.arange(len(x_values))
        numbered_labels = list(np.arange(1, len(x_values) + 1))
        freq_bar_labels = numbered_labels
        pyplt.bar(
            freq_index,
            x_values,
            width=0.2,
            tick_label=freq_bar_labels,
            color=["#e50053"]
        )
        pyplt.xlabel("File number")
        pyplt.ylabel("Variance")
        pyplt.title("Frequency variance for Huffman compression")
        filename = os.path.join(
            self.graph_folder, IMG_HUFFMAN_FREQ)
        pyplt.savefig(filename)
        html_path = self.img_folder + IMG_HUFFMAN_FREQ
        return html_path

    def construct_huffman_character_count_bar_chart(self, x_values: list) -> str:
        """Constructs a character count bar chart for Huffman coding.

        Args:
            x_values (list): a list of int values.

        Returns:
            str: relative path of the created file
        """
        pyplt.figure(5)
        freq_index = np.arange(len(x_values))
        numbered_labels = list(np.arange(1, len(x_values) + 1))
        freq_bar_labels = numbered_labels
        pyplt.bar(
            freq_index,
            x_values,
            width=0.2,
            tick_label=freq_bar_labels,
            color=["#e50053"]
        )
        pyplt.xlabel("File number")
        pyplt.ylabel("Character count")
        pyplt.title("Number of different characters in original content")
        filename = os.path.join(
            self.graph_folder, IMG_HUFFMAN_CHAR_COUNT)
        pyplt.savefig(filename)
        html_path = self.img_folder + IMG_HUFFMAN_CHAR_COUNT
        return html_path

    def construct_lempel_ziv_average_length_bar_chart(self, x_values: list) -> str:
        """Constructs a bar chart of LZ77  mean length data

        Args:
            x_values (list): a list of float values

        Returns:
            str: relative path for the file
        """
        pyplt.figure(3)
        freq_index = np.arange(len(x_values))
        numbered_labels = list(np.arange(1, len(x_values) + 1))
        freq_bar_labels = numbered_labels
        pyplt.bar(
            freq_index,
            x_values,
            width=0.2,
            tick_label=freq_bar_labels,
            color=["#255cae"]
        )
        pyplt.xlabel("File number")
        pyplt.ylabel("Average length")
        pyplt.title("Average match length for Lempel-Ziv 77")
        filename = os.path.join(self.graph_folder, IMG_LZ_MEAN_MATCH)
        pyplt.savefig(filename)
        html_path = self.img_folder + IMG_LZ_MEAN_MATCH
        return html_path

    def construct_lempel_ziv_average_offset_bar_chart(self, x_values: list) -> str:
        """Constructs a bar chart of LZ77 mean offsets

        Args:
            x_values (list): list of float values

        Returns:
            str: relative path for the graph created
        """
        pyplt.figure(4)
        freq_index = np.arange(len(x_values))
        numbered_labels = list(np.arange(1, len(x_values) + 1))
        freq_bar_labels = numbered_labels
        pyplt.bar(
            freq_index,
            x_values,
            width=0.2,
            tick_label=freq_bar_labels,
            color=["#255cae"]
        )
        pyplt.xlabel("File number")
        pyplt.ylabel("Average offset")
        pyplt.title("Average offset for Lempel-Ziv 77")
        filename = os.path.join(self.graph_folder, IMG_LZ_MEAN_OFFSET)
        pyplt.savefig(filename)
        html_path = self.img_folder + IMG_LZ_MEAN_OFFSET
        return html_path

    def construct_compression_ratio_bar_chart(
        self,
        x_values: list,
        y_values: list,
        labels: list
    ) -> str:
        """Constructs a bar char of compression ratio comparison
        between Huffman coding and LZ77.

        Args:
            x_values (list): list of float values containing Huffman ratios
            y_values (list): list of float values containing LZ77 ratios
            labels (list): list of string values for file numbers

        Returns:
            str: relative path to graph created
        """
        pyplt.figure(2)
        x_index = np.arange(len(labels))
        numbered_labels = list(np.arange(1, len(labels) + 1))
        bar_labels = numbered_labels
        legend_labels = ["Huffman coding", "Lempel-Ziv 77"]
        pyplt.bar(
            x_index,
            x_values,
            width=0.2,
            tick_label=bar_labels,
            color=["#e50053"]
        )
        pyplt.bar(
            x_index + 0.2,
            y_values,
            width=0.2,
            tick_label=bar_labels,
            color=["#255cae"]
        )
        pyplt.xlabel("File number")
        pyplt.ylabel("Compression ratio")
        pyplt.title("Compression ratio comparison")
        pyplt.legend(legend_labels, loc=2)
        filename = os.path.join(
            self.graph_folder, IMG_COMPRESS_RATIO)
        pyplt.savefig(filename)
        html_path = self.img_folder + IMG_COMPRESS_RATIO
        return html_path


default_graph_manager = GraphManagement()
