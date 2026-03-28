import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, 
    QFileDialog, QLabel, QComboBox, QCheckBox, QProgressBar, 
    QMessageBox, QFrame, QHeaderView
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon, QColor

from renamer_logic import RenamerLogic
from ai_engine import AIEngine

class BulkRenamerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bulk File Renamer")
        self.setMinimumSize(1000, 700)
        
        # Logic instances
        self.logic = RenamerLogic(".")
        self.ai = AIEngine()
        
        # State
        self.selected_directory = ""
        self.preview_data = [] # List of (original, new, status)
        
        self.init_ui()
        
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Sidebar
        sidebar = QFrame()
        sidebar.setFixedWidth(300)
        sidebar.setFrameShape(QFrame.Shape.StyledPanel)
        sidebar.setStyleSheet("background-color: #f8f9fa;")
        sidebar_layout = QVBoxLayout(sidebar)
        
        # Folder Selection
        sidebar_layout.addWidget(QLabel("1. Select Folder"))
        self.btn_select_folder = QPushButton("Choose Directory...")
        self.btn_select_folder.clicked.connect(self.select_folder)
        sidebar_layout.addWidget(self.btn_select_folder)
        self.lbl_folder_path = QLabel("No folder selected")
        self.lbl_folder_path.setWordWrap(True)
        sidebar_layout.addWidget(self.lbl_folder_path)
        
        sidebar_layout.addSpacing(20)
        
        # Rename Method Tabs (Pattern or AI)
        sidebar_layout.addWidget(QLabel("2. Renaming Method"))
        
        self.method_tabs = QComboBox()
        self.method_tabs.addItems(["Pattern Rename", "AI Rename"])
        self.method_tabs.currentIndexChanged.connect(self.update_method_view)
        sidebar_layout.addWidget(self.method_tabs)
        
        # Container for method-specific inputs
        self.method_container = QFrame()
        self.method_layout = QVBoxLayout(self.method_container)
        
        # Pattern Section
        self.pattern_frame = QWidget()
        pattern_vbox = QVBoxLayout(self.pattern_frame)
        self.input_pattern = QLineEdit()
        self.input_pattern.setPlaceholderText("photo_{date}_{index}{ext}")
        self.input_pattern.textChanged.connect(self.generate_preview)
        pattern_vbox.addWidget(QLabel("Pattern:"))
        pattern_vbox.addWidget(self.input_pattern)
        pattern_vbox.addWidget(QLabel("Variables: {index}, {date}, {time}, {original}, {ext}"))
        
        # AI Section
        self.ai_frame = QWidget()
        ai_vbox = QVBoxLayout(self.ai_frame)
        self.input_prompt = QLineEdit()
        self.input_prompt.setPlaceholderText("Rename these images based on their context...")
        ai_vbox.addWidget(QLabel("AI Prompt:"))
        ai_vbox.addWidget(self.input_prompt)
        self.btn_generate_ai = QPushButton("Generate AI Suggestions")
        self.btn_generate_ai.clicked.connect(self.generate_ai_preview)
        ai_vbox.addWidget(self.btn_generate_ai)
        
        self.method_layout.addWidget(self.pattern_frame)
        self.method_layout.addWidget(self.ai_frame)
        self.ai_frame.hide() # Default to pattern
        
        sidebar_layout.addWidget(self.method_container)
        
        sidebar_layout.addStretch()
        
        # Apply Section
        self.btn_apply = QPushButton("Apply Changes")
        self.btn_apply.setFixedHeight(50)
        self.btn_apply.setStyleSheet("background-color: #007bff; color: white; font-weight: bold;")
        self.btn_apply.clicked.connect(self.apply_changes)
        sidebar_layout.addWidget(self.btn_apply)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.hide()
        sidebar_layout.addWidget(self.progress_bar)
        
        # Main Area
        main_area = QVBoxLayout()
        
        # File Table
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Original Name", "New Name", "Status"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        main_area.addWidget(self.table)
        
        main_layout.addWidget(sidebar)
        main_layout.addLayout(main_area)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Directory")
        if folder:
            self.selected_directory = folder
            self.lbl_folder_path.setText(folder)
            self.logic.directory = folder
            self.logic.refresh_files()
            self.generate_preview()

    def update_method_view(self, index):
        if index == 0: # Pattern
            self.pattern_frame.show()
            self.ai_frame.hide()
            self.generate_preview()
        else: # AI
            self.pattern_frame.hide()
            self.ai_frame.show()

    def generate_preview(self):
        if not self.selected_directory or self.method_tabs.currentIndex() != 0:
            return
            
        pattern = self.input_pattern.text()
        if not pattern:
            return
            
        self.preview_data = self.logic.generate_preview(pattern)
        self.update_table()

    def generate_ai_preview(self):
        if not self.selected_directory:
            QMessageBox.warning(self, "Error", "Please select a folder first.")
            return
        
        prompt = self.input_prompt.text()
        if not prompt:
            QMessageBox.warning(self, "Error", "Please enter an AI prompt.")
            return

        self.btn_generate_ai.setEnabled(False)
        self.btn_generate_ai.setText("Generating...")
        
        # Use AI Engine
        original_names = self.logic.files
        suggested_names = self.ai.generate_names(original_names, prompt)
        
        self.preview_data = []
        for old, new in zip(original_names, suggested_names):
            status = "ready" if old != new else "no_change"
            self.preview_data.append((old, new, status))
            
        self.update_table()
        self.btn_generate_ai.setEnabled(True)
        self.btn_generate_ai.setText("Generate AI Suggestions")

    def update_table(self):
        self.table.setRowCount(0)
        for old, new, status in self.preview_data:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            self.table.setItem(row, 0, QTableWidgetItem(old))
            self.table.setItem(row, 1, QTableWidgetItem(new))
            
            status_item = QTableWidgetItem(status)
            if "error" in status.lower():
                status_item.setForeground(QColor("red"))
            elif status == "success":
                status_item.setForeground(QColor("green"))
            
            self.table.setItem(row, 2, status_item)

    def apply_changes(self):
        if not self.preview_data:
            QMessageBox.warning(self, "Error", "Nothing to rename.")
            return
            
        reply = QMessageBox.question(self, 'Confirmation', 
                                    f"Are you sure you want to rename {len(self.preview_data)} files?", 
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                    QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self.progress_bar.show()
            self.progress_bar.setMaximum(len(self.preview_data))
            
            rename_map = [(old, new) for old, new, s in self.preview_data if s != "no_change"]
            results = self.logic.apply_renaming(rename_map)
            
            # Map results back to preview data for UI update
            result_dict = dict(results)
            new_preview = []
            for old, new, s in self.preview_data:
                res_status = result_dict.get(old, s)
                new_preview.append((old, new, res_status))
            
            self.preview_data = new_preview
            self.update_table()
            self.progress_bar.hide()
            
            QMessageBox.information(self, "Done", "Renaming completed.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BulkRenamerApp()
    window.show()
    sys.exit(app.exec())
