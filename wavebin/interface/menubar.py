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
        
        # Root menu bar items
        self.menus = {
            "file": QMenu("File"),
            "view": QMenu("View"),
            "help": QMenu("Help")
        }

        # Add root items to menu bar
        for m in self.menus: self.addMenu(self.menus[m])

        # Menu actions
        self.menu_actions = {
            "help": {
                "docs":  QAction("Documentation"),
                "bug":   QAction("Report a bug"),
                "----":  None,
                "about": QAction("About")
            }
        }

        # Add actions to root items
        for root in self.menu_actions:
            for action in self.menu_actions[root]:
                # Insert separator
                if action == "----":
                    self.menus[root].addSeparator()
                    continue
            
                self.menu_actions[root][action].triggered.connect(eval(f"self.menu_{root}_{action}"))
                self.menus[root].addAction(self.menu_actions[root][action])


    def menu_help_docs(self): print("docs")
    def menu_help_bug(self): print("bug")
    def menu_help_about(self): print("about")


    def log(self, msg: str):
        """
        Print message to console if verbose mode enabled

        Args:
            msg (str): Message to print to console
        """

        if self.app.config['verbose']: print(msg)
