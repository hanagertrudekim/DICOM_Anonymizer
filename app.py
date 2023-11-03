import sys
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QFileDialog, QListView, QTreeView, QAbstractItemView
from MainWindow import Ui_MainWindow
import importlib


class WorkerThread(QThread):
    finished = pyqtSignal()
    progress = pyqtSignal(int)  # int is sufficient for progress as a percentage

    def __init__(self, dicom_folder, function):
        super().__init__()
        self.dicom_folder = dicom_folder
        self.function = function

    def run(self):
        for progress in self.function(self.dicom_folder):
            self.progress.emit(int(progress * 100))  # Emit the progress signal as a percentage
        self.finished.emit()



class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.selectButton.clicked.connect(self.getDirectory)
        self.submitButton.clicked.connect(self.submitBtnclick)
        self.progressBar.hide() # progressbar 감추기

        # 인스턴스 변수로 dicom_folder를 선언
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
            dicom_deidentifier = importlib.import_module("dicom_deidentifier")
            self.progressBar.show()  # Show the progress bar
            self.progressBar.setValue(0)  # Reset the progress bar to 0%

            self.worker = WorkerThread(self.dicom_folder, dicom_deidentifier.main)
            self.worker.progress.connect(self.update_progress_bar)  # 진행 상태 시그널을 연결합니다.
            self.worker.finished.connect(self.on_main_finished)  # 완료 시그널을 연결합니다.
            self.worker.start()
            self.statusLabel.setText(" 🔄 Processing...")
        else:
            print("🔵 No DICOM directory selected.")
            self.statusLabel.setText(" 🔵 No DICOM directory selected.")

    def update_progress_bar(self, value):
        self.progressBar.setValue(value)  # 프로그레스바 값 업데이트

    def on_main_finished(self):
        self.progressBar.setValue(100)  # 작업 완료 시 프로그레스바를 100%로 설정
        print("submit dicom path")
        self.statusLabel.setText(" ✅ complete DICOM de-Identifier")


app = QtWidgets.QApplication(sys.argv)
app.setStyle('Fusion')

window = MainWindow()
window.show()
app.exec()