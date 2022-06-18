from tkinter import ttk, constants, Frame, Menu, IntVar, filedialog, messagebox, Text
from config import DEFAULT_DATA_PATH
from gui.gui_menu import GuiMenu
from services.compressionmanagement import default_compression_management
from services.filemanagement import default_file_manager


class CompressionView:

    def __init__(self, root):
        self._root = root
        self._frame = None
        self._state = "enabled"
        self.file_to_compress = None
        self.file_to_uncompress = None
        self.compression_management = default_compression_management
        self.filemanager = default_file_manager

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

        self._compression_frame = ttk.LabelFrame(
            master=self._frame,
            text="Compress",
            style="Custom.TLabelframe"
        )

        self._uncompression_frame = ttk.LabelFrame(
            master=self._frame,
            text="Uncompress",
            style="Custom.TLabelframe"
        )

        self._label_and_instruction_frame.grid(
            row=0,
            columnspan=2,
            sticky=constants.EW)
        self._analysis_frame.grid(
            row=1,
            columnspan=2,
            sticky=constants.EW)
        self._compression_frame.grid(
            row=2,
            column=0,
            sticky=constants.EW)
        self._uncompression_frame.grid(
            row=2,
            column=1,
            sticky=constants.EW)

        label = ttk.Label(
            master=self._label_and_instruction_frame,
            text="Compress or uncompress data",
            style="Header1.TLabel"
        )

        label_description = ttk.Label(
            master=self._label_and_instruction_frame,
            text="In this view you can compress or uncompress data.\nUse radio button to choose compression algorithm. Compression log data is updated when file is compressed.",
            style="Centered.TLabel"
        )

        self.label_file_explorer_compress = ttk.Label(
            self._compression_frame,
            text="Select a file to compress",
            style="Custom.TLabel"
        )

        self.label_file_explorer_uncompress = ttk.Label(
            self._uncompression_frame,
            text="Select a file to uncompress",
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

        self.label_file_explorer_compress.grid(
            row=0,
            column=0,
            pady=10
        )

        self.label_file_explorer_uncompress.grid(
            row=0,
            column=0,
            pady=10
        )

        self._construct_log_frame()
        self._construct_buttons()

    def _construct_buttons(self):

        button_select_file_to_compress = ttk.Button(
            master=self._compression_frame,
            text="select file",
            command=self._handle_get_file_to_compress,
            style="Custom.TButton"

        )

        button_select_file_to_uncompress = ttk.Button(
            master=self._uncompression_frame,
            text="select file",
            command=self._handle_get_file_to_uncompress,
            style="Custom.TButton"

        )

        button_compress = ttk.Button(
            master=self._compression_frame,
            text="compress",
            command=self._handle_compression,
            style="Custom.TButton"
        )

        button_uncompress = ttk.Button(
            master=self._uncompression_frame,
            text="uncompress",
            command=self._handle_uncompression,
            style="Custom.TButton"
        )

        self._compression_var = IntVar()
        radiobutton_label = ttk.Label(
            master=self._compression_frame,
            text="Select compression method",
            style="Custom.TLabel"
        )

        radiobutton_huffman = ttk.Radiobutton(
            self._compression_frame,
            text="Huffman coding",
            variable=self._compression_var,
            value=1,
            style="Custom.TRadiobutton",
            state=self._state)

        radiobutton_lempelziv77 = ttk.Radiobutton(
            self._compression_frame,
            text="Lempel-Ziv 77",
            variable=self._compression_var,
            value=2,
            style="Custom.TRadiobutton",
            state=self._state)

        button_select_file_to_compress.grid(
            sticky=constants.NSEW
        )

        radiobutton_label.grid(
            pady=10,
            sticky=constants.W)

        radiobutton_huffman.grid(
            sticky=constants.W)

        radiobutton_lempelziv77.grid(
            sticky=constants.W)

        button_compress.grid(
            pady=20,
            sticky=constants.NSEW
        )

        button_select_file_to_uncompress.grid(
            sticky=constants.NSEW
        )

        button_uncompress.grid(
            pady=20,
            sticky=constants.NSEW
        )

    def _construct_log_frame(self):
        analysis_header = ttk.Label(
            master=self._analysis_frame,
            text="Compression log",
            style="Header1.TLabel"
        )

        textfield = Text(
            master=self._analysis_frame,
            wrap="word",
            bg="white"
        )
        analysis_header.grid(
            row=1,
            column=0
        )
        textfield.grid(
            row=1,
            column=0
        )

        log_content = self.filemanager.get_log_content()

        textfield.insert(1.0, log_content)
        textfield["state"] = "normal"

    # TODO: Consider improving validation
    def _handle_compression(self):
        """An initial method for handling compression.

        Only validations at the moment are that file is chosen and file extension matches.
        """
        if not self.file_to_compress:
            self._file_error("Select a file to compress")
            return
        if not self.compression_management.validate_file_extension(self.file_to_compress[-3:], "txt"):
            self._file_error("Can only compress txt-files currently")
            return
        compression_method = self._compression_var.get()
        if compression_method == 1:
            self.compression_management.initial_huffman_compression(
                self.file_to_compress)
        if compression_method == 2:
            self.compression_management.lempel_ziv_compress(
                self.file_to_compress)
        self._update_log()
        self._compression_status_notification("File compressed successfully!")

    def _update_log(self):
        self.clear_frame(self._analysis_frame)
        self._construct_log_frame()

    def clear_frame(self, frame: ttk.LabelFrame):
        """A general method for clearing a selected frame before repopulating it. 
        Can be used for multiple purposes. 
        Args:
            frame (ttk.LabelFrame): LabelFrame widget in which the buttons are to be embedded.
        """
        for widgets in frame.winfo_children():
            widgets.destroy()

    def _handle_uncompression(self):
        """An initial method for handling compression.

        Note to self: validation has duplicate code. Consider creating a method to
        handle validation.

        Currently only Huffman coding is available.
        Only validations at the moment are that file is chosen and file extension matches.
        """

        if not self.file_to_uncompress:
            self._file_error("Select a file to uncompress")
            return
        if not (self.file_to_uncompress[-3:] == "huf" or self.file_to_uncompress[-2:] == "lz"):
            self._file_error("Can only uncompress .huf and .lz - files.")
            return
        if self.file_to_uncompress[-3:] == "huf":
            self.compression_management.initial_huffman_uncompression(
                self.file_to_uncompress)
        if self.file_to_uncompress[-2:] == "lz":
            self.compression_management.lempel_ziv_uncompress(
                self.file_to_uncompress
            )
        self._update_log()
        self._compression_status_notification(
            "File uncompressed successfully!")

    def _handle_get_file_to_compress(self):
        """A method to handle filedialog opening.

        Default path can be configured in .env - file.
        """

        self.file_to_compress = filedialog.askopenfilename(initialdir=DEFAULT_DATA_PATH,
                                                           title="Select a File",
                                                           filetypes=(
                                                               ("Supported types",
                                                                ".txt"),
                                                               ("all files", ".*")
                                                           )
                                                           )
        filename_split = self.file_to_compress.split("/")
        filename = filename_split[-1]
        self.label_file_explorer_compress.configure(
            text=f"File Opened: {filename}")

    def _handle_get_file_to_uncompress(self):
        """A method to handle filedialog opening.

        Default path can be configured in .env - file.
        """

        self.file_to_uncompress = filedialog.askopenfilename(initialdir=DEFAULT_DATA_PATH,
                                                             title="Select a File",
                                                             filetypes=(
                                                                 ("Supported types",
                                                                  ".huf"),
                                                                 ("Supported types",
                                                                  ".lz"),
                                                                 ("all files", ".*")
                                                             )
                                                             )
        filename_split = self.file_to_uncompress.split("/")
        filename = filename_split[-1]
        self.label_file_explorer_uncompress.configure(
            text=f"File Opened: {filename}")

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
