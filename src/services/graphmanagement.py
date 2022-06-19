import os
import matplotlib.pyplot as pyplt
import numpy as np
from config import DEFAULT_TEST_GRAPH_FOLDER
from config import IMG_COMPRESS_RATIO
from config import IMG_HUFFMAN_FREQ
from config import IMG_LZ_MEAN_MATCH
from config import IMG_LZ_MEAN_OFFSET

class GraphManagement:

    def __init__(self):
        self.graph_folder = DEFAULT_TEST_GRAPH_FOLDER
        img_folder_split = DEFAULT_TEST_GRAPH_FOLDER.split("/")
        self.img_folder = img_folder_split[-1] + "/"

    def construct_huffman_frequency_variance_bar_chart(self, x_values):
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

    def construct_lempel_ziv_average_length_bar_chart(self, x_values):
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

    def construct_lempel_ziv_average_offset_bar_chart(self, x_values):
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

    def construct_compression_ratio_bar_chart(self, x_values, y_values, labels):
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
