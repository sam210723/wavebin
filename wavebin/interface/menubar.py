"""
wavebin
https://github.com/sam210723/wavebin

Oscilloscope waveform capture viewer
"""

import logging
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenuBar, QMenu, QToolBar
import qtawesome as qta

from wavebin import __main__ as main

class MainMenuBar(QMenuBar):
    """
    Main window menu bar
    """

    def __init__(self, tool_bar: QToolBar) -> None:
        # Initialise base class
        super(MainMenuBar, self).__init__()
        self.tool_bar: QToolBar = tool_bar

        # Hide menubar by default
        self.setHidden(True)

        # Menu actions
        self.menu_actions = {
            "file": {
                "open":   ["Open waveform", "folder-open"],
                "cap":    ["Capture waveform", "wave-square"],
                "export": ["Export waveform", "file-export"],
                "sep0":   None,
                "exit":   ["Exit", "power-off"]
            },
            "view": {
                "props":  ["Waveform properties", "list"]
            },
            "help": {
                "docs":   ["Documentation", "bookmark"],
                "bug":    ["Report a bug", "bug"],
                "update": ["Update wavebin", "sync-alt"],
                "sep0":   None,
                "about":  ["About", "question"]
            }
        }

        # Build menubar
        self.menus = {}
        for m in self.menu_actions:
            # Add root menus
            self.menus[m] = QMenu(m.title())
            self.addMenu(self.menus[m])

            # Add actions to root menus
            for a in self.menu_actions[m]:
                # Insert separator
                if self.menu_actions[m][a] == None:
                    self.menus[m].addSeparator()
                    continue

                # Get icon from Font Awesome
                icon = qta.icon(
                    f"fa5s.{self.menu_actions[m][a][1]}",
                    color="#000",
                    color_active="#444"
                )

                # Build action object
                action = QAction(self)
                action.setIcon(icon)
                action.setText(self.menu_actions[m][a][0])
                action.triggered.connect(eval(f"self.menu_{m}_{a}"))
                self.menus[m].addAction(action)

                # Replace list in dict with QAction instance
                self.menu_actions[m][a] = action

        # Set default action states
        self.menu_actions['file']['export'].setEnabled(False)
        self.menu_actions['view']['props'].setEnabled(False)


    # Reuse functions from tool bar in menu bar
    def menu_file_open(self) -> bool:   return self.tool_bar.button_open()
    def menu_file_cap(self) -> None:    self.tool_bar.button_capture()
    def menu_file_export(self) -> None: self.tool_bar.button_export()
    def menu_file_exit(self) -> None:   main.safe_exit()
    def menu_view_props(self) -> int:   return self.tool_bar.props_dialog.exec()
    def menu_help_docs(self) -> bool:   return self.tool_bar.button_docs()
    def menu_help_bug(self) -> bool:    return self.tool_bar.button_bug()
    def menu_help_update(self) -> bool: return self.tool_bar.button_update()
    def menu_help_about(self) -> None:  self.tool_bar.button_about()
