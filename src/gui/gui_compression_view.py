from distutils.log import INFO
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
        label = ttk.Label(
            master=self._frame,
            text="Compress or uncompress data",
            style="Header1.TLabel")

        label_description = ttk.Label(
            master=self._frame,
            text="In this view you can compress or uncompress data. Note: radiobutton is currently disabled as only an initial version of Huffman coding is available.",
            style="Centered.TLabel")

        self.label_file_explorer = ttk.Label(self._frame,
                            text = "File Explorer using Tkinter",
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
            row=2,
            column=0,
            pady=10
        )
        

        self._construct_radio_buttons()
        self._construct_buttons()

    def _construct_radio_buttons(self):
        
        self._compression_var = IntVar()
        radiobutton_label = ttk.Label(
            master=self._frame,
            text="Select compression method",
            style="Custom.TLabel"
        )

        radiobutton_huffman = ttk.Radiobutton(
            self._frame,
            text="Huffman coding",
            variable=self._compression_var,
            value=1,
            style="Custom.TRadiobutton",
            state=self._state)

        radiobutton_lempelziv77 = ttk.Radiobutton(
            self._frame,
            text="Lempel-Ziv 77",
            variable=self._compression_var,
            value=2,
            style="Custom.TRadiobutton",
            state=self._state)

        radiobutton_label.grid(row=4, column=1, sticky=constants.W)
        radiobutton_huffman.grid(row=5, column=1, sticky=constants.W)
        radiobutton_lempelziv77.grid(row=6, column=1, sticky=constants.W)

    def _construct_buttons(self):

        button_select_file = ttk.Button(
            master=self._frame,
            text="select file",
            command=self._handle_get_file,
            style="Custom.TButton"

        )

        button_compress = ttk.Button(
            master=self._frame,
            text="compress",
            command=self._handle_compression,
            style="Custom.TButton"
        )
        
        button_uncompress = ttk.Button(
            master=self._frame,
            text="uncompress",
            command=self._handle_uncompression,
            style="Custom.TButton"
        )
        
        button_select_file.grid(
            row=3,
            column=1
        )
        
        button_compress.grid(
            row=7,
            column=1
        )
        
        button_uncompress.grid(
            row=7,
            column=2
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

    def _file_error(self, content):
        messagebox.showinfo(
            title="Error!",
            message=content,
            icon=messagebox.ERROR)
    
    def _compression_status_notification(self, content):
        messagebox.showinfo(
            title="Success!",
            message=content,
            icon=messagebox.INFO
        )

