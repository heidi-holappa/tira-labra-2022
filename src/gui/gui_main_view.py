from tkinter import ttk, constants, Frame, Menu
from gui.gui_menu import GuiMenu
from services.compressionmanagement import default_compression_management


class MainView:
    """Creates the main view of the application.
    Attributes:
        root: root component of the GUI
        login: a reference to a method that handles creating the login view
        create account: a reference to a method that handles the creation of create account view
        frame: a variable for creating the Frame object
    """

    def __init__(self, root, compression_view, testing_view):
        self._root = root
        self._compression_view = compression_view
        self._testing_view = testing_view
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
        self._create_menubar()
        label = ttk.Label(
            master=self._frame,
            text="Datastructures and Algorithms laboratory project application",
            style="Header1.TLabel")

        label_description = ttk.Label(
            master=self._frame,
            text="The purpose of this application is to demonstrate the functionality and efficiency of two well establised lossless data compression algorithms. Before starting out please read through the project documentation found through help menu.",
            style="Centered.TLabel")

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

        self.construct_buttons()

    def construct_buttons(self):

        button_compression_view = ttk.Button(
            master=self._frame,
            text="compress / uncompress data",
            command=self._compression_view,
            style="Custom.TButton"
        )

        button_testing_view = ttk.Button(
            master=self._frame,
            text="Run extensive tests",
            command=self._testing_view,
            style="Custom.TButton"

        )

        button_compression_view.grid(
            row=3,
            column=0
        )

        button_testing_view.grid(
            row=4,
            column=0,
            padx=10,
            pady=10
        )

    def compress_all(self):
        self.compression_management.compress_all_txt_files_in_directory()

    def _create_menubar(self):
        """A method that calls for the construction of default menu bar.
        """
        create_menu = GuiMenu(self._root)
        menubar = create_menu.init_menu()
        self._root.config(menu=menubar)
