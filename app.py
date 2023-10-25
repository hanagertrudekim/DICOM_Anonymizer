import sys
from PyQt5 import QtWidgets, uic

from MainWindow import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.pushButton.clicked.connect(self.getDirectory)
        self.submitButton.clicked.connect(self.submitBtnclick)

        # 인스턴스 변수로 dicom_folder를 선언
        self.dicom_folder = ""

    def getDirectory(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Select DICOM Directory")
        if folder:  # 사용자가 디렉토리를 선택했다면
            self.dicom_folder = folder
            print("선택된 DICOM 디렉토리:", self.dicom_folder)

    def submitBtnclick(self):
        if self.dicom_folder:
            print("submit dicom path")
            
        else:
            print("DICOM 디렉토리가 선택되지 않았습니다.")



app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()