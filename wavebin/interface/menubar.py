"""
wavebin
https://github.com/sam210723/wavebin

Oscilloscope waveform capture viewer
"""

from PyQt5.QtWidgets import QAction, QApplication, QMenuBar, QMenu


class MainMenuBar(QMenuBar):
    """
    Main window menu bar
    """

    def __init__(self, app: QApplication):
        # Initialise base class
        super(MainMenuBar, self).__init__()

        # Hide menubar by default
        self.setHidden(True)

        # Parent application instance
        self.app = app

        # Menu actions
        self.menu_actions = {
            "file": {
                "open":   QAction("Open waveform..."),
                "cap":    QAction("Capture waveform..."),
                "export": QAction("Export waveform..."),
                "----":   None,
                "exit":   QAction("Exit")
            },
            "view": {

            },
            "help": {
                "docs":   QAction("Documentation"),
                "bug":    QAction("Report a bug"),
                "----":   None,
                "about":  QAction("About")
            }
        }

        # Build menubar
        self.menus = {}
        for root in self.menu_actions:
            # Add root menus
            self.menus[root] = QMenu(root.title())
            self.addMenu(self.menus[root])

            # Add actions to root menus
            for action in self.menu_actions[root]:
                # Insert separator
                if action == "----":
                    self.menus[root].addSeparator()
                    continue

                # Attach mouse click event
                self.menu_actions[root][action].triggered.connect(eval(f"self.menu_{root}_{action}"))
                self.menus[root].addAction(self.menu_actions[root][action])


    def menu_file_open(self):   self.app.button_open()
    def menu_file_cap(self):    self.app.button_capture()
    def menu_file_export(self): self.app.tool_bar.button_export()
    def menu_file_exit(self):   self.app.safe_exit(self.app.config)
    def menu_help_docs(self):   self.app.button_docs()
    def menu_help_bug(self):    self.app.tool_bar.button_bug()
    def menu_help_about(self):  print("ABOUT")


    def log(self, msg: str):
        """
        Print message to console if verbose mode enabled

        Args:
            msg (str): Message to print to console
        """

        if self.app.config['verbose']: print(msg)
