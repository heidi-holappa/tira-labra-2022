from tkinter import Menu, messagebox
import webbrowser


class GuiMenu:
    """A class to configure and construct the menu for the GUI.
    """

    def __init__(self, root, main_view, compression_view, testing_view):
        """Constructor for initializing an object of the class.
        Args:
            root (Tk): root component for constructing views
        """

        self._root = root
        self._main_view = main_view
        self._compression_view = compression_view
        self._testing_view = testing_view

    def init_menu(self):
        menubar = Menu(self._root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Main view", command=self._main_view)
        filemenu.add_command(label="Compression view",
                             command=self._compression_view)
        filemenu.add_command(label="Extensive testing view",
                             command=self._testing_view)
        filemenu.add_command(label="Exit", command=self.exit)
        menubar.add_cascade(label="File", menu=filemenu)

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(
            label="How-to-use (opens browser)", command=self._open_help)
        helpmenu.add_command(
            label="Analysis-tests documentation (opens browser)", command=self._open_analysis_documentation)
        helpmenu.add_command(label="About", command=self._show_about)
        menubar.add_cascade(label="Help", menu=helpmenu)
        return menubar

    def exit(self):
        """Method that destroys the root component and exits the application.
        """
        self._root.quit()

    def _open_help(self):
        """A method that opens the requirements specification in the operating system's default browser.
        """
        webbrowser.open_new(
            "https://github.com/heidi-holappa/tira-labra-2022/blob/master/documentation/how-to-guide.md")

    def _open_analysis_documentation(self):
        """Opens the testing documentation in Github in the default browser window.
        """
        webbrowser.open_new(
            "https://github.com/heidi-holappa/tira-labra-2022/blob/master/documentation/testing-documentation.md#extensive-analysis-tests-view-in-gui")

    def _show_about(self):
        """A method that prompts a messabox with project information.
        """
        messagebox.showinfo(
            title="About the application",
            message="Version 0.1\n\nCreated as a University project in 2022",
            icon=messagebox.INFO
        )
