from tkinter import ttk, constants, Frame, Menu, IntVar, filedialog, messagebox
from config import DEFAULT_DATA_PATH
from gui.gui_menu import GuiMenu
from services.compressionmanagement import defaul_compression_management


class CompressionView:

    def __init__(self, root):
        self._root = root
        self._frame = None
        self._state = "disabled"
        self.filename = None
        self.compression_management = defaul_compression_management

        self._initialize()

    def pack(self):
        """A method to add the widgets to the GUI and make them visible to the user.
        """
        if self._frame:
            self._frame.pack(fill=constants.X)

    def destroy(self):
        """A method to destroy the Frame-object and all it's children. 
        """
        if self._frame:
            self._frame.destroy()

    def _initialize(self):
        """Initializes the widgets in the main view. 
        """
        self._frame = Frame(self._root,
                            padx=50,
                            pady=50,
                            bg="grey95")

        self._label_and_instruction_frame = ttk.LabelFrame(
            master=self._frame,
            text="Info",
            style="Custom.TLabelframe"
        )

        self._analysis_frame = ttk.LabelFrame(
            master=self._frame,
            text="Compression analysis",
            style="Custom.TLabelframe"
        )

        self._buttons_frame = ttk.LabelFrame(
            master=self._frame,
            text="Select action",
            style="Custom.TLabelframe"
        )

        self._label_and_instruction_frame.grid(sticky=constants.EW)
        self._analysis_frame.grid(sticky=constants.EW)
        self._buttons_frame.grid(sticky=constants.EW)
        
        label = ttk.Label(
            master=self._label_and_instruction_frame,
            text="Compress or uncompress data",
            style="Header1.TLabel"
        )

        label_description = ttk.Label(
            master=self._label_and_instruction_frame,
            text="In this view you can compress or uncompress data. Note: radiobutton is currently disabled as only an initial version of Huffman coding is available.",
            style="Centered.TLabel"
        )

        self.label_file_explorer = ttk.Label(
            self._buttons_frame,
            text = "Start by selecting a file to compress / uncompress",
            style="Custom.TLabel"
        )

        label.grid(
            row=0,
            column=0,
            padx=10,
            pady=0
        )

        label_description.grid(
            row=1,
            column=0,
            pady=10
        )

        self.label_file_explorer.grid(
            row=0,
            column=0,
            pady=10
        )
        

        self._construct_radio_buttons()
        self._construct_analysis_frame()
        self._construct_buttons()

    def _construct_radio_buttons(self):
        
        self._compression_var = IntVar()
        radiobutton_label = ttk.Label(
            master=self._buttons_frame,
            text="Select compression method",
            style="Custom.TLabel"
        )

        radiobutton_huffman = ttk.Radiobutton(
            self._buttons_frame,
            text="Huffman coding",
            variable=self._compression_var,
            value=1,
            style="Custom.TRadiobutton",
            state=self._state)

        radiobutton_lempelziv77 = ttk.Radiobutton(
            self._buttons_frame,
            text="Lempel-Ziv 77",
            variable=self._compression_var,
            value=2,
            style="Custom.TRadiobutton",
            state=self._state)

        radiobutton_label.grid(row=2, column=0, pady=10, sticky=constants.W)
        radiobutton_huffman.grid(row=3, column=0, sticky=constants.W)
        radiobutton_lempelziv77.grid(row=4, column=0, sticky=constants.W)

    def _construct_buttons(self):

        button_select_file = ttk.Button(
            master=self._buttons_frame,
            text="select file",
            command=self._handle_get_file,
            style="Custom.TButton"

        )

        button_compress = ttk.Button(
            master=self._buttons_frame,
            text="compress",
            command=self._handle_compression,
            style="Custom.TButton"
        )
        
        button_uncompress = ttk.Button(
            master=self._buttons_frame,
            text="uncompress",
            command=self._handle_uncompression,
            style="Custom.TButton"
        )
        
        button_select_file.grid(
            row=1,
            column=0,
            sticky=constants.W
        )
        
        button_compress.grid(
            row=5,
            column=0,
            pady=20
        )
        
        button_uncompress.grid(
            row=5,
            column=1,
            pady=20
        )

    def _construct_analysis_frame(self):
        analysis_header = ttk.Label(
            master=self._analysis_frame,
            text="Compression analysis",
            style="Header1.TLabel"
        )

        analysis_algorithm_used_label = ttk.Label(
            master=self._analysis_frame,
            text="Selected algorithm:",
            style="Custom.TLabel"
        )
        
        self.analysis_algorithm_used_value = ttk.Label(
            master=self._analysis_frame,
            text="no action selected",
            style="Custom.TLabel",
            state="disabled"
        )
        
        analysis_original_size_label = ttk.Label(
            master=self._analysis_frame,
            text="Original size (bits):",
            style="Custom.TLabel"
        )

        self.analysis_original_size_value = ttk.Label(
            master=self._analysis_frame,
            text="no action selected",
            style="Custom.TLabel",
            state="disabled"
        )
    
        analysis_compressed_content_size_label = ttk.Label(
            master=self._analysis_frame,
            text="Compressed content (bits):",
            style="Custom.TLabel"
        )

        self.analysis_compressed_content_size_value = ttk.Label(
            master=self._analysis_frame,
            text="no action selected",
            style="Custom.TLabel",
            state="disabled"
        )

        analysis_compressed_header_label = ttk.Label(
            master=self._analysis_frame,
            text="Compressed file header (bits):",
            style="Custom.TLabel"
        )

        self.analysis_compressed_header_value = ttk.Label(
            master=self._analysis_frame,
            text="no action selected",
            style="Custom.TLabel",
            state="disabled"
        )

        analysis_compressed_total_size_label = ttk.Label(
            master=self._analysis_frame,
            text="Total compressed (bits):",
            style="Custom.TLabel"
        )

        self.analysis_compressed_total_size_value = ttk.Label(
            master=self._analysis_frame,
            text="no action selected",
            style="Custom.TLabel",
            state="disabled"
        )

        analysis_content_ratio_label = ttk.Label(
            master=self._analysis_frame,
            text="Compression ratio (content):",
            style="Custom.TLabel"
        )

        self.analysis_content_ratio_value = ttk.Label(
            master=self._analysis_frame,
            text="no action selected",
            style="Custom.TLabel",
            state="disabled"
        )

        analysis_total_ratio_label = ttk.Label(
            master=self._analysis_frame,
            text="Compression ratio (total):",
            style="Custom.TLabel"
        )

        self.analysis_total_ratio_value = ttk.Label(
            master=self._analysis_frame,
            text="no action selected",
            style="Custom.TLabel",
            state="disabled"
        )

        analysis_header.grid(
            row=0,
            column=0,
            sticky=constants.W
        )

        analysis_algorithm_used_label.grid(
            row=1,
            column=0,
            sticky=constants.W
        )

        self.analysis_algorithm_used_value.grid(
            row=1,
            column=1,
            sticky=constants.W
        )

        analysis_original_size_label.grid(
            row=2,
            column=0,
            sticky=constants.W
        )

        self.analysis_original_size_value.grid(
            row=2,
            column=1,
            sticky=constants.W
        )

        analysis_compressed_content_size_label.grid(
            row=3,
            column=0,
            sticky=constants.W
        )

        self.analysis_compressed_content_size_value.grid(
            row=3,
            column=1,
            sticky=constants.W
        )

        analysis_compressed_header_label.grid(
            row=4,
            column=0,
            sticky=constants.W
        )

        self.analysis_compressed_header_value.grid(
            row=4,
            column=1,
            sticky=constants.W
        )

        analysis_compressed_total_size_label.grid(
            row=5,
            column=0,
            sticky=constants.W
        )

        self.analysis_compressed_total_size_value.grid(
            row=5,
            column=1,
            sticky=constants.W
        )

        analysis_total_ratio_label.grid(
            row=6,
            column=0,
            sticky=constants.W
        )

        self.analysis_total_ratio_value.grid(
            row=6,
            column=1,
            sticky=constants.W
        )

        analysis_content_ratio_label.grid(
            row=7,
            column=0,
            sticky=constants.W
        )

        self.analysis_content_ratio_value.grid(
            row=7,
            column=1,
            sticky=constants.W
        )

    def _handle_compression(self):
        """An initial method for handling compression. 

        Currently only Huffman coding is available. 
        Only validations at the moment are that file is chosen and file extension matches. 
        """
        if not self.filename:
            self._file_error("Select a file to compress")
            return
        if not self.compression_management.validate_file_extension(self.filename[-3:], "txt"):
            self._file_error("Can only compress txt-files currently")
            return
        self.compression_management.initial_huffman_compression(self.filename)
        self._compression_status_notification("File compressed successfully!")

        self.configure_analysis_labels()

    def configure_analysis_labels(self):
        self.analysis_algorithm_used_value.configure(
            text=self.compression_management.last_analysis["algorithm_used"],
            state="enabled"
        )
        self.analysis_original_size_value.configure(
            text=str(self.compression_management.last_analysis["uncompressed_size"]) + " bits",
            state="enabled"
        )
        self.analysis_compressed_content_size_value.configure(
            text=str(self.compression_management.last_analysis["compressed_content"]) + " bits",
            state="enabled"
        )
        self.analysis_compressed_header_value.configure(
            text=str(self.compression_management.last_analysis["compressed_header"]) + " bits",
            state="enabled"
        )
        self.analysis_compressed_total_size_value.configure(
            text=str(self.compression_management.last_analysis["compressed_total"]) + " bits",
            state="enabled"
        )
        self.analysis_content_ratio_value.configure(
            text=str(self.compression_management.last_analysis["content_ratio"]) + " percent",
            state="enabled"
        )
        self.analysis_total_ratio_value.configure(
            text=str(self.compression_management.last_analysis["total_ratio"]) + " percent",
            state="enabled"
        )


    def _handle_uncompression(self):
        """An initial method for handling compression. 

        Note to self: validation has duplicate code. Consider creating a method to 
        handle validation.

        Currently only Huffman coding is available. 
        Only validations at the moment are that file is chosen and file extension matches. 
        """
        if not self.filename:
            self._file_error("Select a file to uncompress")
            return
        if not self.compression_management.validate_file_extension(self.filename[-3:], "huf"):
            self._file_error("Can only uncompress huf-files currently")
            return
        self.compression_management.initial_huffman_uncompression(self.filename)
        self._compression_status_notification("File uncompressed successfully!")

    def _handle_get_file(self):
        """A method to handle filedialog opening. 

        Default path can be configured in .env - file. 

        """

        self.filename = filedialog.askopenfilename(initialdir = DEFAULT_DATA_PATH,
                                        title = "Select a File",
                                        filetypes = (
                                            ("Supported types",".txt"),
                                            ("Supported types", ".huf"),
                                            ("all files",".*")
                                            )
                                        )
        self.label_file_explorer.configure(text="File Opened: "+self.filename)

    def _file_error(self, content: str):
        """A general method to handle showing messageboxes with an error

        Args:
            content (str): a custom error message to be shown
        """
        messagebox.showinfo(
            title="Error!",
            message=content,
            icon=messagebox.ERROR)
    
    def _compression_status_notification(self, content: str):
        """A method for handling information messageboxes

        Args:
            content (str): a custom informational message to be shown. 
        """
        messagebox.showinfo(
            title="Success!",
            message=content,
            icon=messagebox.INFO
        )

