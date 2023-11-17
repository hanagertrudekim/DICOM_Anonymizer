# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt6 UI code generator 6.6.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1062, 674)
        MainWindow.setStyleSheet("background-color: #101010;")
        self.centralWidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.submitButton = QtWidgets.QPushButton(parent=self.centralWidget)
        self.submitButton.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.submitButton.sizePolicy().hasHeightForWidth())
        self.submitButton.setSizePolicy(sizePolicy)
        self.submitButton.setMinimumSize(QtCore.QSize(130, 40))
        font = QtGui.QFont()
        font.setFamily(".AppleSystemUIFont")
        font.setPointSize(-1)
        self.submitButton.setFont(font)
        self.submitButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.submitButton.setStyleSheet("background-color: #101010;\n"
"font-size: 15px;\n"
"color: #91C9F8;\n"
"\n"
"")
        self.submitButton.setObjectName("submitButton")
        self.gridLayout_2.addWidget(self.submitButton, 21, 4, 1, 1)
        self.label = QtWidgets.QLabel(parent=self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(150, 0))
        self.label.setText("")
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 21, 5, 1, 1)
        self.folderPath = QtWidgets.QLabel(parent=self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.folderPath.sizePolicy().hasHeightForWidth())
        self.folderPath.setSizePolicy(sizePolicy)
        self.folderPath.setMinimumSize(QtCore.QSize(0, 100))
        self.folderPath.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.folderPath.setFont(font)
        self.folderPath.setMouseTracking(False)
        self.folderPath.setStyleSheet("color: rgb(235, 235, 235);\n"
"font-size: 10px;\n"
"line-height: 1.6;\n"
"padding: 3px;\n"
"padding-top: 15px;")
        self.folderPath.setText("")
        self.folderPath.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.folderPath.setObjectName("folderPath")
        self.gridLayout_2.addWidget(self.folderPath, 14, 2, 1, 2)
        self.label_5 = QtWidgets.QLabel(parent=self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setMinimumSize(QtCore.QSize(0, 150))
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 22, 0, 1, 6)
        self.selectButton = QtWidgets.QPushButton(parent=self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selectButton.sizePolicy().hasHeightForWidth())
        self.selectButton.setSizePolicy(sizePolicy)
        self.selectButton.setMinimumSize(QtCore.QSize(160, 35))
        self.selectButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.selectButton.setStyleSheet("background-color: #101010;\n"
"font-size: 15px;\n"
"color: #91C9F8;")
        self.selectButton.setObjectName("selectButton")
        self.gridLayout_2.addWidget(self.selectButton, 8, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(parent=self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMinimumSize(QtCore.QSize(260, 0))
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 5, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(parent=self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(145, 145, 145);\n"
"font-size: 11px;\n"
"padding-left: 5px;")
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 12, 2, 1, 2)
        self.header = QtWidgets.QLabel(parent=self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.header.sizePolicy().hasHeightForWidth())
        self.header.setSizePolicy(sizePolicy)
        self.header.setMinimumSize(QtCore.QSize(200, 35))
        self.header.setMaximumSize(QtCore.QSize(16777215, 35))
        self.header.setAccessibleDescription("")
        self.header.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.header.setStyleSheet("font-size: 14px;\n"
"color: white;\n"
"border-bottom: 0.7px solid rgb(94, 94, 94);\n"
"letter-spacing: 0.2em;\n"
"padding-left: 3px;\n"
"padding-bottom: 2px;")
        self.header.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.header.setObjectName("header")
        self.gridLayout_2.addWidget(self.header, 4, 1, 1, 5)
        self.mrnInput = QtWidgets.QLineEdit(parent=self.centralWidget)
        self.mrnInput.setMinimumSize(QtCore.QSize(0, 35))
        self.mrnInput.setStyleSheet("border: none;\n"
"border-bottom: 0.5px solid rgb(214, 214, 214);\n"
"color: white;\n"
"margin: 0 50px 5px 10px;")
        self.mrnInput.setInputMask("")
        self.mrnInput.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.mrnInput.setObjectName("mrnInput")
        self.gridLayout_2.addWidget(self.mrnInput, 8, 3, 1, 1)
        self.Title = QtWidgets.QLabel(parent=self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Title.sizePolicy().hasHeightForWidth())
        self.Title.setSizePolicy(sizePolicy)
        self.Title.setMinimumSize(QtCore.QSize(200, 90))
        self.Title.setMaximumSize(QtCore.QSize(16777215, 100))
        font = QtGui.QFont()
        font.setFamily(".AppleSystemUIFont")
        font.setPointSize(-1)
        font.setBold(False)
        font.setUnderline(False)
        self.Title.setFont(font)
        self.Title.setStyleSheet("color: white;\n"
"font-size: 23px;")
        self.Title.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter|QtCore.Qt.AlignmentFlag.AlignTop)
        self.Title.setObjectName("Title")
        self.gridLayout_2.addWidget(self.Title, 6, 2, 1, 2)
        self.progressBar = QtWidgets.QProgressBar(parent=self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy)
        self.progressBar.setMinimumSize(QtCore.QSize(0, 0))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout_2.addWidget(self.progressBar, 15, 2, 1, 2)
        self.statusLabel = QtWidgets.QLabel(parent=self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statusLabel.sizePolicy().hasHeightForWidth())
        self.statusLabel.setSizePolicy(sizePolicy)
        self.statusLabel.setMinimumSize(QtCore.QSize(0, 0))
        self.statusLabel.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setFamily("AppleGothic")
        font.setItalic(True)
        self.statusLabel.setFont(font)
        self.statusLabel.setStyleSheet("color: rgb(235, 235, 235);")
        self.statusLabel.setText("")
        self.statusLabel.setObjectName("statusLabel")
        self.gridLayout_2.addWidget(self.statusLabel, 20, 2, 1, 2)
        self.label_2 = QtWidgets.QLabel(parent=self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(145, 145, 145);\n"
"font-size: 11px;\n"
"padding-left: 5px;")
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 10, 2, 1, 2)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.submitButton.setText(_translate("MainWindow", "SUBMIT"))
        self.selectButton.setText(_translate("MainWindow", "SELECT FOLDER"))
        self.label_3.setText(_translate("MainWindow", "(DICOM folder name should be SUBJ_CTDATE: ex) KU39009_20220921)"))
        self.header.setText(_translate("MainWindow", "LAMIS"))
        self.mrnInput.setPlaceholderText(_translate("MainWindow", "MRN number"))
        self.Title.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:23pt;\">DICOM Form</span></p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "Please select one or multiple Raw DICOM Folders."))
