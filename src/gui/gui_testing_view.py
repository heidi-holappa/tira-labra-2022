from tkinter import ttk, constants, Frame, IntVar, filedialog, messagebox
from config import DEFAULT_DATA_PATH
from config import DEFAULT_TEST_DATA_PATH
from services.compressionmanagement import default_compression_management


class TestingView:

    def __init__(self, root):
        self._root = root
        self._frame = None
        self.compression_management = default_compression_management

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
