import sys
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QThread, pyqtSignal
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
        folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Select DICOM Directory")
        if folder:  # 사용자가 디렉토리를 선택했다면
            self.dicom_folder = folder
            self.folderPath.setText(self.dicom_folder)
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