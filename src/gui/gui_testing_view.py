from tkinter import ttk, constants, Frame, IntVar, filedialog, messagebox, Text, simpledialog
from config import DEFAULT_DATA_PATH
from config import DEFAULT_TEST_DATA_PATH
from services.compressionmanagement import default_compression_management
from services.filemanagement import default_file_manager
from services.extensivetesthandler import default_test_handler
from services.extensivetesthandler import InvalidCharactersError

class TestingView:

    def __init__(self, root):
        self._root = root
        self._frame = None
        self.compression_management = default_compression_management
        self.filemanager = default_file_manager
        self.testhandler = default_test_handler

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

        self.construct_analysis_frame()
        self.construct_instruction_frame()
        self.construct_buttons_frame()

    def construct_instruction_frame(self):
        label_instruction = ttk.Label(
            master=self._label_and_instruction_frame,
            text="In this view you can generate extensive test data and run selected tests. Please note that running extensive tests can take a long time, especially with large content.",
            style="Centered.TLabel"
        )
        label_instruction.grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )

    def construct_analysis_frame(self):
        analysis_header = ttk.Label(
            master=self._analysis_frame,
            text="Extensive test log",
            style="Header1.TLabel"
        )

        textfield = Text(
            master=self._analysis_frame,
            wrap="word",
            bg="white"
        )
        textfield.grid(
            row=0,
            column=0
        )

        log_content = self.filemanager.get_log_content(DEFAULT_TEST_DATA_PATH)

        textfield.insert(1.0, log_content)
        textfield["state"] = "normal"

    def construct_buttons_frame(self):
        button_generate_english = ttk.Button(
            master=self._buttons_frame,
            text="Create paragraphs in English",
            command=self._generate_paragraphs_of_english,
            style="Custom.TButton"

        )

        button_generate_ascii = ttk.Button(
            master=self._buttons_frame,
            text="Create paragraphs of printable ASCII",
            command=self._generate_paragraphs_of_ascii,
            style="Custom.TButton"
        )

        button_run_extensive_tests = ttk.Button(
            master=self._buttons_frame,
            text="Run extensive tests",
            command=self._run_extensive_tests,
            style="Custom.TButton"
        )

        button_generate_english.grid(
            row=0,
            column=0,
            pady=20,
            padx=20
        )

        button_generate_ascii.grid(
            row=0,
            column=1,
            pady=20,
            padx=20
        )

        button_run_extensive_tests.grid(
            row=0,
            column=2,
            pady=20,
            padx=20
        )

    def _update_log(self):
        self.clear_frame(self._analysis_frame)
        self.construct_analysis_frame()

    # TODO: This could be moved to shared methods (compression view uses this as well)
    def clear_frame(self, frame: ttk.LabelFrame):
        """A general method for clearing a selected frame before repopulating it. 
        Can be used for multiple purposes. 
        Args:
            frame (ttk.LabelFrame): LabelFrame widget in which the buttons are to be embedded.
        """
        for widgets in frame.winfo_children():
            widgets.destroy()

    def _generate_paragraphs_of_ascii(self):
        """Handles calling the instance of ExtensiveTestHandler to create
        random ascii-content.
        """
        paragraphs = simpledialog.askinteger(
            'Paragraphs', "How many paragraphs do you want to create?")
        if not paragraphs or paragraphs < 0 or paragraphs > 10000:
            self._show_error("Please select a value between 0 and 10,000")
            return
        self.testhandler.create_document_with_random_printable_ascii(
            paragraphs)

    def _generate_paragraphs_of_english(self):
        """Handles calling the instance of ExtensiveTestHandler to create
        random natural English language content.
        """
        paragraphs = simpledialog.askinteger(
            'Paragraphs', "How many paragraphs do you want to create?")
        if not paragraphs or paragraphs < 0 or paragraphs > 10000:
            self._show_error("Please select a value between 0 and 10,000")
            return
        self.testhandler.create_document_with_natural_language(paragraphs)

    def _run_extensive_tests(self):
        """Handles calling the instance of ExtensiveTestHangler to initiate
        the extensive tests.
        """
        max_characters = simpledialog.askinteger(
            "Document length", "Max character length for documents to be included.")
        if not max_characters or max_characters < 0:
            self._show_error("Please type in a positive integer value.")
            return
        try: 
            self.testhandler.activate_extensive_tests(max_characters)
        except InvalidCharactersError as charerror:
            self._show_error(charerror.args[0])
        self._update_log()

    def _show_error(self, content=""):
        """A messagebox showing an error message.

        Args:
            content (str, optional): Content describing the error. Defaults to "".
        """
        messagebox.showinfo(
            title="Error!",
            message=content,
            icon=messagebox.ERROR)
