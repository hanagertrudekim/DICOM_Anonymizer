import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QThread, pyqtSignal, QRunnable, QThreadPool, QObject
from MainWindow import Ui_MainWindow
from dicom_deidentifier import main

class WorkerSignals(QObject):
    finished = pyqtSignal()

class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    def run(self):
        self.fn(*self.args, **self.kwargs)
        self.signals.finished.emit()

def long_running_task(dicom_folder):
    # 여기에 CPU 집약적인 작업을 추가
    main(dicom_folder)


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

            # 작업을 스레드 풀에 추가
            worker = Worker(long_running_task, self.dicom_folder)
            worker.signals.finished.connect(self.on_main_finished)
            QThreadPool.globalInstance().start(worker)
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