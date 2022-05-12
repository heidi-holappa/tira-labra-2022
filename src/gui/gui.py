from tkinter import Tk
from gui.gui_theme import setTheme
from gui.gui_main_view import MainView

class GUI:

    """Creates a hub-object to coordinate application logic for other GUI-objects.
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
        """A method that call to construct the main view.
        If a user is logged in, they are logged out when entering main view.
        """

        self._hide_current_view()

        self._current_view = MainView(
                        self._root
                        )

        self._current_view.pack()

def main():
    """A method that launch the application.
    """

    window = Tk()
    window.title("Laboratory project: Lossless compression")

    gui = GUI(window)
    gui.start()

    window.mainloop()