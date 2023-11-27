from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

import sys

import alex_editor.widgets as widgets
import alex_editor.syntax_highlighter as syntax_highlighter
import alex_editor.util as util
import alex_editor.command_palette as command_palette

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("ALEX IDE")

        # Infinite loop
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(0)

        # Current directory
        self.root_open_dir = "/home/alexandru/Documents"
        self.open_dir = self.root_open_dir + "/GitHub"
        self.opened_file = ""
        self.opened_file_type = "Plain text"

        # Main Widget and Layout
        self.mainw = QWidget(self)
        self.layout_ = QHBoxLayout()
        self.mainw.setLayout(self.layout_)

        # Menubar
        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        dir_open = QAction("Open Directory..", self)
        dir_open.triggered.connect(self.f_open_dir)
        file_menu.addAction(dir_open)
        file_menu.addSeparator()
        create_n_file = QAction("Create New File...", self)
        create_n_file.triggered.connect(self.f_create_new_file)
        save_c_file = QAction("Save Current File...", self)
        save_c_file.triggered.connect(self.f_save_c_file)
        file_menu.addAction(create_n_file)
        file_menu.addAction(save_c_file)

        # Tools
        tab_tools = QTabWidget(self)
        self.layout_.addWidget(tab_tools)

        # File Browser
        self.filebrowser = widgets.FileBrowser(self)
        self.filebrowser.dirupbt.clicked.connect(self.f_directory_up)
        self.filebrowser.listwidget.clicked.connect(self.f_lb_select)
        self.filebrowser.update(self.open_dir, self.root_open_dir)
        tab_tools.addTab(self.filebrowser, "File Browser")

        # Text Box
        self.textbox = widgets.TextBox(self)
        self.layout_.addWidget(self.textbox)

        # Indentation
        self.space = '    '
        self.indent_level = 0
        #self.textbox.textChanged.connect(self.tb_add_indent)

        # Command palette
        self.command_p = command_palette.CommandPalette()

        # Shortcuts
        QShortcut("Ctrl+O", self).activated.connect(self.f_open_dir)
        QShortcut("Ctrl+S", self).activated.connect(self.f_save_c_file)
        QShortcut("Ctrl+Shift+B", self).activated.connect(self.p_show)

        # Show
        self.setCentralWidget(self.mainw)
    
    def update(self):
        pass

    def tb_add_indent(self):
        if self.textbox.tb.toPlainText().endswith(':\n') or self.textbox.tb.toPlainText().endswith(self.space * (self.indent_level+1)):
            self.indent_level += 1
        elif self.textbox.tb.toPlainText().endswith(self.space * (self.indent_level-1)):
            self.indent_level -= 1
        if self.textbox.tb.toPlainText().endswith('\n'):
            self.textbox.tb.insertPlainText(self.space * self.indent_level)
    
    def f_open_dir(self):
        filedialog = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if not filedialog:
            return
        self.root_open_dir, self.open_dir = filedialog, filedialog
        self.filebrowser.update(self.open_dir, self.root_open_dir)
    
    def f_lb_select(self):
        if self.filebrowser.listwidget.selectedItems()[0].text().startswith("DIR"):
            self.f_next_dir()
        elif self.filebrowser.listwidget.selectedItems()[0].text().startswith("FILE"):
            self.f_next_file()
            if self.opened_file.endswith(".py"):
                self.textbox.highlighter = syntax_highlighter.Python(self.textbox.tb.document())
                self.opened_file_type = "Python"
            elif self.opened_file.endswith(".c") or self.opened_file.endswith(".cpp") or \
                self.opened_file.endswith(".h") or self.opened_file.endswith(".hpp"):
                self.textbox.highlighter = syntax_highlighter.Cpp(self.textbox.tb.document())
                self.opened_file_type = "C/C++"
            if self.opened_file.endswith(".sh"):
                self.textbox.highlighter = syntax_highlighter.Sh(self.textbox.tb.document())
                self.opened_file_type = "sh"
            else:
                self.textbox.highlighter = syntax_highlighter.Sh(self.textbox.tb.document())
                self.opened_file_type = "Plain text"
        self.textbox.update(self.opened_file)
        self.command_p.opened_file = self.opened_file
        self.command_p.opened_file_type = self.opened_file_type
    
    def f_next_dir(self):
        self.open_dir += self.filebrowser.listwidget.selectedItems()[0].text().split("DIR    ")[1]
        self.filebrowser.update(self.open_dir, self.root_open_dir)
    
    def f_next_file(self):
        fn = self.filebrowser.listwidget.selectedItems()[0].text().split("FILE    ")[1]
        ff = f"{self.open_dir}/{fn}"
        try:
            with open(ff, "r+") as f:
                self.textbox.tb.setPlainText(f.read())
                self.opened_file = ff
        except Exception as e:
            QMessageBox(self, text=str(e)).show()
    
    def f_save_c_file(self):
        err = util.run_py_code(f"""
with open("{self.opened_file}", "w") as f:
    f.truncate(0)
    f.write('''{self.textbox.tb.toPlainText()}''')
""")
        QMessageBox(self, text=err).show() if err else None
    
    def f_directory_up(self):
        self.open_dir = self.open_dir.rpartition("/")[0] if self.open_dir != self.root_open_dir else self.open_dir
        self.filebrowser.update(self.open_dir, self.root_open_dir)

    def f_create_new_file(self):
        ew = widgets.entry_window("Enter file name")
        if ew == "":
            return
        open(self.open_dir + "/" + ew, "w").close()
        self.filebrowser.update(self.open_dir, self.root_open_dir)

    def p_show(self):
        self.command_p.show()
        self.command_p.activateWindow()
        self.command_p.commands = self.command_p.actions[self.opened_file_type]
        self.command_p.update_commands()
        self.command_p.input_field.setPlaceholderText(f"Actions for {self.opened_file_type} file")

def main():
    app = QApplication(sys.argv)
    root = MainWindow()
    root.showMaximized()
    #root.show()
    sys.exit(app.exec())
