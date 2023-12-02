from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

import alex_editor.syntax_highlighter as syntax_highlighter
import alex_editor.util as util
import os

class FileBrowser(QFrame):
    def __init__(self, parent):
        super().__init__()
        layout = QVBoxLayout()
        self.rootlb = QLabel(parent)
        self.currentlb = QLabel(parent)
        self.dirupbt = QPushButton(parent, text="One Directory up")
        self.listwidget = QListWidget(parent)
        layout.addWidget(self.rootlb)
        layout.addWidget(self.currentlb)
        layout.addWidget(self.dirupbt)
        layout.addWidget(self.listwidget)
        self.setLayout(layout)
    
    def update(self, folder:str, root:str) -> None:
        # root label
        self.rootlb.setText(f"Root directory: {root}")
        self.currentlb.setText(f"Current directory: {folder.split(root)[1]}")

        # list widget
        dirlist = []
        for root, dirs, files in os.walk(folder):
            root_item = root.split(folder)[1]
            dirlist.append("DIR    " + root_item) if root_item.count("/") == 1 else None
        dirlist.sort()

        filelist = []
        for path in os.listdir(folder):
            if os.path.isfile(os.path.join(folder, path)):
                filelist.append("FILE    " + path)
        filelist.sort()

        self.listwidget.clear()
        for count, item in enumerate(filelist):
            self.listwidget.insertItem(count, item)
        for count, item in enumerate(dirlist):
            self.listwidget.insertItem(count, item)

    def selected_item(self) -> str:
        return self.listwidget.selectedItems()[0].text().split("    ")[1]


class TextBox(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.ofile_lb = QLabel(self)
        layout.addWidget(self.ofile_lb)
        self.tb = QPlainTextEdit(self)
        self.tb.setFont(QFont("Monospace"))
        self.highlighter = syntax_highlighter.Nothing(self.tb.document())
        layout.addWidget(self.tb)

    def update(self, opened_file_name) -> None:
        if opened_file_name:
            self.ofile_lb.setText(f"Opened file: {opened_file_name}")
        else:
            self.ofile_lb.setText(f"No file opened")


def entry_window(caption) -> str:
    text, ok = QInputDialog.getText(QWidget(), "Entry window",
        caption)

    if ok:
        return text
    else:
        return ""
