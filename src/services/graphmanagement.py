import os
import matplotlib.pyplot as pyplt
import numpy as np
from config import DEFAULT_TEST_GRAPH_FOLDER

class GraphManagement:

    def __init__(self):        
        self.graph_folder = DEFAULT_TEST_GRAPH_FOLDER

    def construct_huffman_frequency_variance_bar_chart(self, x_values):
        pyplt.figure(1)
        freq_index = np.arange(len(x_values))
        numbered_labels = list(np.arange(1, len(x_values) + 1))
        freq_bar_labels = numbered_labels
        pyplt.bar(
            freq_index,
            x_values,
            width=0.2,
            tick_label= freq_bar_labels,
            color = ["#e50053"]
            )
        pyplt.xlabel("File number")
        pyplt.ylabel("Variance")
        pyplt.title("Frequency variance for Huffman compression")
        filename = os.path.join(self.graph_folder, "huffman-frequency-variance.png")
        pyplt.savefig(filename)
        return "images/huffman-frequency-variance.png"

    def construct_lempel_ziv_average_length_bar_chart(self, x_values):
        pyplt.figure(3)
        freq_index = np.arange(len(x_values))
        numbered_labels = list(np.arange(1, len(x_values) + 1))
        freq_bar_labels = numbered_labels
        pyplt.bar(
            freq_index,
            x_values,
            width=0.2,
            tick_label= freq_bar_labels,
            color = ["#255cae"]
            )
        pyplt.xlabel("File number")
        pyplt.ylabel("Average length")
        pyplt.title("Average match length for Lempel-Ziv 77")
        filename = os.path.join(self.graph_folder, "lempel-ziv-avg-match.png")
        pyplt.savefig(filename)
        return "images/lempel-ziv-avg-match.png"

    def construct_lempel_ziv_average_offset_bar_chart(self, x_values):
        pyplt.figure(4)
        freq_index = np.arange(len(x_values))
        numbered_labels = list(np.arange(1, len(x_values) + 1))
        freq_bar_labels = numbered_labels
        pyplt.bar(
            freq_index,
            x_values,
            width=0.2,
            tick_label= freq_bar_labels,
            color = ["#255cae"]
            )
        pyplt.xlabel("File number")
        pyplt.ylabel("Average offset")
        pyplt.title("Average offset for Lempel-Ziv 77")
        filename = os.path.join(self.graph_folder, "lempel-ziv-avg-offset.png")
        pyplt.savefig(filename)
        return "images/lempel-ziv-avg-offset.png"

    
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
            tick_label= bar_labels,
            color = ["#e50053"]
            )
        pyplt.bar(
            x_index + 0.2,
            y_values,
            width=0.2,
            tick_label= bar_labels,
            color = ["#255cae"]
            )
        pyplt.xlabel("File number")
        pyplt.ylabel("Compression ratio")
        pyplt.title("Compression ratio comparison")
        pyplt.legend(legend_labels, loc=2)
        filename = os.path.join(self.graph_folder, "compression-ratio-comparison.png")
        pyplt.savefig(filename)
        return "images/compression-ratio-comparison.png"


default_graph_manager = GraphManagement()