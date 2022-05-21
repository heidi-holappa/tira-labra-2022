from tkinter import Menu, messagebox
import webbrowser


class GuiMenu:
    """A class to configure and construct the menu for the GUI.
    """

    def __init__(self, root):
        """Constructor for initializing an object of the class.
        Args:
            root (Tk): root component for constructing views
        """

        self._root = root

    def init_menu(self):
        menubar = Menu(self._root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=self.exit)
        menubar.add_cascade(label="File", menu=filemenu)

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(
            label="Documenation (opens browser)", command=self._open_help)
        helpmenu.add_command(label="About", command=self._show_about)
        menubar.add_cascade(label="Help", menu=helpmenu)
        return menubar

    def exit(self):
        """Method that destroys the root component and exits the application.
        """
        self._root.destroy()

    def _open_help(self):
        """A method that opens the requirements specification in the operating system's default browser.
        """
        webbrowser.open_new(
            "https://github.com/heidi-holappa/tira-labra-2022/blob/master/documentation/requirements-specification.md")

    def _show_about(self):
        """A method that prompts a messabox with project information.
        """
        messagebox.showinfo(
            title="About the application",
            message="Version 0.1\n\nCreated as a University project in 2022",
            icon=messagebox.INFO
        )
