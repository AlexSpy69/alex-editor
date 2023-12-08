from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

import sys

import alex_editor.util as util

class CommandPalette(QWidget):
    def __init__(self):
        super().__init__()

        self.opened_file = ""
        self.opened_file_type = "Plain text"
        self.open_dir = ""
        self.root_open_dir = ""
        self.commands = {}
        self.actions = {"Plain text": {}, "Python": {"Run": "python3 !fp/!fn",
            "Compile": "python3 -m py_compile !fp/!fn"}, "C/C++": {"Compile": "",
            "Compile and run": "", "Make": "", "Make and run": ""},
            "sh": {"Gain execution permission": "chmod +x !fp/!fn", "Run": "!fp/!fn"}}

        self.hidden = False
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Create the input field
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Type a command...")
        self.input_field.textChanged.connect(self.filter_commands)

        # Create the list widget
        self.list_widget = QListWidget(self)
        self.list_widget.itemActivated.connect(self.execute_command)

        # Add commands to the list widget
        for command in self.commands:
            item = QListWidgetItem(command)
            self.list_widget.addItem(item)

        layout.addWidget(self.input_field)
        layout.addWidget(self.list_widget)

        self.setLayout(layout)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Command Palette')
        self.show()

    def update_commands(self):
        self.list_widget.clear()
        for command in self.commands:
            item = QListWidgetItem(command)
            self.list_widget.addItem(item)

    def filter_commands(self, text): 
        # Filter commands based on the input text
        self.list_widget.clear()
        for command in self.commands:
            if text.lower() in command.lower():
                item = QListWidgetItem(command)
                self.list_widget.addItem(item)

    def execute_command(self, item):
        command = self.actions[self.opened_file_type][item.text()]
        file_rp = self.opened_file.rpartition("/")
        repl_command = util.replace(command, {"!fp": file_rp[0], "!fn": file_rp[2]})
        util.execute_command(repl_command, file_rp[0])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    palette = CommandPalette()
    sys.exit(app.exec())
