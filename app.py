import sys
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QFileDialog, QListView, QTreeView, QAbstractItemView
from MainWindow import Ui_MainWindow
import importlib


class WorkerThread(QThread):
    finished = pyqtSignal()

    def __init__(self, dicom_folder, function):
        super().__init__()
        self.dicom_folder = dicom_folder
        self.function = function

    def run(self):
        self.function(self.dicom_folder)
        self.finished.emit()


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.selectButton.clicked.connect(self.getDirectory)
        self.submitButton.clicked.connect(self.submitBtnclick)

        # 인스턴스 변수로 dicom_folder를 선언
        self.dicom_folder = ""

    def getDirectory(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.Directory)
        file_dialog.setOption(QFileDialog.Option.DontUseNativeDialog, True)
        file_view = file_dialog.findChild(QListView, 'listView')

        # to make it possible to select multiple directories:
        if file_view:
            file_view.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        f_tree_view = file_dialog.findChild(QTreeView)
        if f_tree_view:
            f_tree_view.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)

        if file_dialog.exec():
            self.dicom_folder = file_dialog.selectedFiles()
            # Update the folder display here
            folder_display_text = ""
            for i, folder in enumerate(self.dicom_folder):
                if i < 4:  # Only show the first four directories
                    folder_display_text += f"📁 {folder}\n"
                else:
                    folder_display_text += "...\n"
                    break  # Stop after adding the ellipsis
            
            self.folderPath.setText(folder_display_text)
            print("선택된 DICOM 디렉토리:", self.dicom_folder)


    def submitBtnclick(self):
        if self.dicom_folder:
            self.statusLabel.setText(" 🔄 Processing...")

            dicom_deidentifier = importlib.import_module("dicom_deidentifier")
            self.worker_thread = WorkerThread(self.dicom_folder, dicom_deidentifier.main)
            self.worker_thread.finished.connect(self.on_main_finished)
            self.worker_thread.start()
        else:
            print("DICOM 디렉토리가 선택되지 않았습니다.")
            self.statusLabel.setText(" 🔵 DICOM 디렉토리가 선택되지 않았습니다.")

    def on_main_finished(self):
        print("submit dicom path")
        self.statusLabel.setText(" ✅ complete DICOM de-Identifier")


app = QtWidgets.QApplication(sys.argv)
app.setStyle('Fusion')

window = MainWindow()
window.show()
app.exec()