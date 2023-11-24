import sys
import os
os.system('sudo apt-get install libxkbcommon-x11-0')

from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QFileDialog, QListView, QTreeView, QAbstractItemView
from MainWindow import Ui_MainWindow
import importlib
import dicom_deidentifier

class WorkerThread(QThread):
    finished = pyqtSignal(str)
    progress = pyqtSignal(int)

    def __init__(self, dicom_folder, subj):
        super().__init__()
        self.dicom_folder = dicom_folder
        self.subj = subj

    def run(self):
        try:
            for output in dicom_deidentifier.main(self.dicom_folder, self.subj):
                if isinstance(output, (int, float)):
                    self.progress.emit(int(output * 100))
                elif isinstance(output, str):
                    self.finished.emit(output)
                    return
        except Exception as e:
            self.finished.emit(f"Error: {e}")
        else:
            self.finished.emit("Unknown error occurred")

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.selectButton.clicked.connect(self.getDirectory)
        self.submitButton.clicked.connect(self.submitBtnclick)

        self.progressBar.hide()

        self.dicom_folder = ""

    def getDirectory(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.Directory)
        file_dialog.setOption(QFileDialog.Option.DontUseNativeDialog, True)
        file_view = file_dialog.findChild(QListView, 'listView')
        # to make it possible to select multiple directories:
        if file_view:
            file_view.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        f_tree_view = file_dialog.findChild(QTreeView)
        if f_tree_view:
            f_tree_view.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

        if file_dialog.exec():
            self.dicom_folder = file_dialog.selectedFiles()
            self.updateFolderPathDisplay()

    def updateFolderPathDisplay(self):
        folder_display_text = "<br>".join(f"📁 {folder}<br>" for folder in self.dicom_folder[:4])
        if len(self.dicom_folder) > 4:
            folder_display_text += "<br>..."
        self.folderPath.setText(folder_display_text)

    def submitBtnclick(self):
        if not self.dicom_folder:
            self.updateStatus(" 🔵 No DICOM directory selected.")
            return

        subj = self.subjInput.text()

        self.progressBar.show()
        self.progressBar.setValue(0)
        self.updateStatus(" 🔄 Processing...")

        self.worker = WorkerThread(self.dicom_folder, subj)
        self.worker.progress.connect(self.progressBar.setValue)
        self.worker.finished.connect(self.on_main_finished)
        self.worker.start()

    def on_main_finished(self, message):
        if "completed" in message.lower():
            self.progressBar.setValue(100)
        else:
            self.progressBar.hide()
        self.updateStatus(message)

    def updateStatus(self, message):
        self.statusLabel.setText(message)

app = QtWidgets.QApplication(sys.argv)
app.setStyle('Fusion')

window = MainWindow()
window.show()
app.exec()
