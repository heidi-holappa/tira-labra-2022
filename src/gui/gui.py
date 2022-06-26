from tkinter import Tk
from gui.gui_compression_view import CompressionView
from gui.gui_theme import setTheme
from gui.gui_main_view import MainView
from gui.gui_testing_view import TestingView


class GUI:

    """Creates a hub-object to coordinate application logic for other GUI-objects.

    Application theme can be re-configured in the file gui_theme.py. The protocol
    configuration sets a handler for closing the application. 

    Attributes:
        root: root component of the GUI
        current_view: the current view to be constructed
        style: currently selected graphical style
    """

    def __init__(self, root):
        self._root = root
        self._current_view = None
        self.style = "default"
        setTheme(self._root)
        self._root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        """When user presses the "X" icon, this method is called.

        If at some point some tasks would need to be handled when exiting, 
        these could be addressed here. Do note that Menu also includes 
        an option for exiting the app. If additional activities are included
        here, refactor the exit-feature from Menu to here.
        """
        self._root.quit()

    def start(self):
        """Calls a method that initiates the building of the main view
        """
        self._show_main_view()

    def _hide_current_view(self):
        """A method that destroys all widgets from the root component. 
        """
        if self._current_view:
            self._current_view.destroy()

        self._current_view = None

    def _show_main_view(self):
        """A method that calls to construct the main view.
        If a user is logged in, they are logged out when entering main view.
        """

        self._hide_current_view()

        self._current_view = MainView(
            self._root,
            self._handle_compression_view,
            self._handle_testing_view,
            self.start
        )

        self._current_view.pack()

    def _show_compression_view(self):
        """Handles calling the construction of the compression view.
        """
        self._hide_current_view()
        self._current_view = CompressionView(
            self._root,
        )
        self._current_view.pack()

    def _handle_compression_view(self):
        """Calls the method that handles the construction of
        compression view"""
        self._show_compression_view()

    def _show_testing_view(self):
        """Handles calling for the construction of testing view"""
        self._hide_current_view()
        self._current_view = TestingView(
            self._root,
        )
        self._current_view.pack()

    def _handle_testing_view(self):
        """Calls the method that handles changing the view to testing_view"""
        self._show_testing_view()


def main():
    """A method that launch the application.
    """

    window = Tk()
    window.title("Laboratory project: Lossless compression")

    gui = GUI(window)
    gui.start()

    window.mainloop()
