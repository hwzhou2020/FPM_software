# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Main.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGraphicsView, QGridLayout, QHBoxLayout,
    QMainWindow, QMenu, QMenuBar, QPlainTextEdit,
    QPushButton, QSizePolicy, QSpacerItem, QStatusBar,
    QWidget)

class Ui_FPMSoftware(object):
    def setupUi(self, FPMSoftware):
        if not FPMSoftware.objectName():
            FPMSoftware.setObjectName(u"FPMSoftware")
        FPMSoftware.setEnabled(True)
        FPMSoftware.resize(1190, 720)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(FPMSoftware.sizePolicy().hasHeightForWidth())
        FPMSoftware.setSizePolicy(sizePolicy)
        FPMSoftware.setMinimumSize(QSize(1190, 720))
        self.actionLoad_Data = QAction(FPMSoftware)
        self.actionLoad_Data.setObjectName(u"actionLoad_Data")
        self.actionSystem_Spec = QAction(FPMSoftware)
        self.actionSystem_Spec.setObjectName(u"actionSystem_Spec")
        self.actionAlgorithm_Spec = QAction(FPMSoftware)
        self.actionAlgorithm_Spec.setObjectName(u"actionAlgorithm_Spec")
        self.actionSave_Reults = QAction(FPMSoftware)
        self.actionSave_Reults.setObjectName(u"actionSave_Reults")
        self.actionLoad_Results = QAction(FPMSoftware)
        self.actionLoad_Results.setObjectName(u"actionLoad_Results")
        self.actionShow_single_raw_frame = QAction(FPMSoftware)
        self.actionShow_single_raw_frame.setObjectName(u"actionShow_single_raw_frame")
        self.actionShow_all_raw_frames = QAction(FPMSoftware)
        self.actionShow_all_raw_frames.setObjectName(u"actionShow_all_raw_frames")
        self.actionSingle_raw_spectrum = QAction(FPMSoftware)
        self.actionSingle_raw_spectrum.setObjectName(u"actionSingle_raw_spectrum")
        self.actionAll_raw_spectrum = QAction(FPMSoftware)
        self.actionAll_raw_spectrum.setObjectName(u"actionAll_raw_spectrum")
        self.actionAmplitude_result = QAction(FPMSoftware)
        self.actionAmplitude_result.setObjectName(u"actionAmplitude_result")
        self.actionPhase_result = QAction(FPMSoftware)
        self.actionPhase_result.setObjectName(u"actionPhase_result")
        self.actionPupil_function = QAction(FPMSoftware)
        self.actionPupil_function.setObjectName(u"actionPupil_function")
        self.actionAll_results = QAction(FPMSoftware)
        self.actionAll_results.setObjectName(u"actionAll_results")
        self.actionCheck_systerm_specs = QAction(FPMSoftware)
        self.actionCheck_systerm_specs.setObjectName(u"actionCheck_systerm_specs")
        self.actionSystem_specs = QAction(FPMSoftware)
        self.actionSystem_specs.setObjectName(u"actionSystem_specs")
        self.actionGerchberg_Saxton = QAction(FPMSoftware)
        self.actionGerchberg_Saxton.setObjectName(u"actionGerchberg_Saxton")
        self.actionEPRY = QAction(FPMSoftware)
        self.actionEPRY.setObjectName(u"actionEPRY")
        self.actionGauss_Newton = QAction(FPMSoftware)
        self.actionGauss_Newton.setObjectName(u"actionGauss_Newton")
        self.actionKramers_Kronig = QAction(FPMSoftware)
        self.actionKramers_Kronig.setObjectName(u"actionKramers_Kronig")
        self.actionAPIC = QAction(FPMSoftware)
        self.actionAPIC.setObjectName(u"actionAPIC")
        self.actionSoftware_Guide = QAction(FPMSoftware)
        self.actionSoftware_Guide.setObjectName(u"actionSoftware_Guide")
        self.actionReferences = QAction(FPMSoftware)
        self.actionReferences.setObjectName(u"actionReferences")
        self.actionSave_Messgaes = QAction(FPMSoftware)
        self.actionSave_Messgaes.setObjectName(u"actionSave_Messgaes")
        self.actionClear_Messages = QAction(FPMSoftware)
        self.actionClear_Messages.setObjectName(u"actionClear_Messages")
        self.actionSave_Specs = QAction(FPMSoftware)
        self.actionSave_Specs.setObjectName(u"actionSave_Specs")
        self.actionSIngle_ROI = QAction(FPMSoftware)
        self.actionSIngle_ROI.setObjectName(u"actionSIngle_ROI")
        self.actionAll_ROI_images = QAction(FPMSoftware)
        self.actionAll_ROI_images.setObjectName(u"actionAll_ROI_images")
        self.centralwidget = QWidget(FPMSoftware)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy1)
        self.centralwidget.setMinimumSize(QSize(1100, 600))
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.load_butt = QPushButton(self.centralwidget)
        self.load_butt.setObjectName(u"load_butt")

        self.horizontalLayout_5.addWidget(self.load_butt)

        self.roi_butt = QPushButton(self.centralwidget)
        self.roi_butt.setObjectName(u"roi_butt")

        self.horizontalLayout_5.addWidget(self.roi_butt)

        self.run_butt = QPushButton(self.centralwidget)
        self.run_butt.setObjectName(u"run_butt")

        self.horizontalLayout_5.addWidget(self.run_butt)

        self.save_butt = QPushButton(self.centralwidget)
        self.save_butt.setObjectName(u"save_butt")

        self.horizontalLayout_5.addWidget(self.save_butt)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)

        self.acknowledge_text = QPlainTextEdit(self.centralwidget)
        self.acknowledge_text.setObjectName(u"acknowledge_text")

        self.horizontalLayout_5.addWidget(self.acknowledge_text)

        self.horizontalLayout_5.setStretch(0, 1)
        self.horizontalLayout_5.setStretch(1, 1)
        self.horizontalLayout_5.setStretch(2, 1)
        self.horizontalLayout_5.setStretch(3, 1)
        self.horizontalLayout_5.setStretch(4, 5)
        self.horizontalLayout_5.setStretch(5, 2)

        self.gridLayout_2.addLayout(self.horizontalLayout_5, 0, 0, 1, 1)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.Msg_window = QPlainTextEdit(self.centralwidget)
        self.Msg_window.setObjectName(u"Msg_window")

        self.gridLayout_3.addWidget(self.Msg_window, 0, 1, 1, 1)

        self.display_window = QGraphicsView(self.centralwidget)
        self.display_window.setObjectName(u"display_window")
        self.display_window.setAutoFillBackground(False)

        self.gridLayout_3.addWidget(self.display_window, 0, 0, 1, 1)

        self.gridLayout_3.setColumnStretch(0, 9)
        self.gridLayout_3.setColumnStretch(1, 7)

        self.gridLayout_2.addLayout(self.gridLayout_3, 1, 0, 1, 1)

        self.gridLayout_2.setRowStretch(0, 1)
        self.gridLayout_2.setRowStretch(1, 12)
        FPMSoftware.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(FPMSoftware)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1190, 33))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuDisplay = QMenu(self.menubar)
        self.menuDisplay.setObjectName(u"menuDisplay")
        self.menuSpecs = QMenu(self.menubar)
        self.menuSpecs.setObjectName(u"menuSpecs")
        self.menuAlgorithm_specs = QMenu(self.menuSpecs)
        self.menuAlgorithm_specs.setObjectName(u"menuAlgorithm_specs")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuMessageBox = QMenu(self.menubar)
        self.menuMessageBox.setObjectName(u"menuMessageBox")
        FPMSoftware.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(FPMSoftware)
        self.statusbar.setObjectName(u"statusbar")
        FPMSoftware.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSpecs.menuAction())
        self.menubar.addAction(self.menuDisplay.menuAction())
        self.menubar.addAction(self.menuMessageBox.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionLoad_Data)
        self.menuFile.addAction(self.actionSystem_Spec)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave_Reults)
        self.menuFile.addAction(self.actionLoad_Results)
        self.menuDisplay.addAction(self.actionShow_single_raw_frame)
        self.menuDisplay.addAction(self.actionShow_all_raw_frames)
        self.menuDisplay.addAction(self.actionSingle_raw_spectrum)
        self.menuDisplay.addAction(self.actionAll_raw_spectrum)
        self.menuDisplay.addSeparator()
        self.menuDisplay.addAction(self.actionSIngle_ROI)
        self.menuDisplay.addAction(self.actionAll_ROI_images)
        self.menuDisplay.addSeparator()
        self.menuDisplay.addAction(self.actionAmplitude_result)
        self.menuDisplay.addAction(self.actionPhase_result)
        self.menuDisplay.addAction(self.actionPupil_function)
        self.menuDisplay.addAction(self.actionAll_results)
        self.menuSpecs.addAction(self.actionCheck_systerm_specs)
        self.menuSpecs.addAction(self.actionSystem_specs)
        self.menuSpecs.addAction(self.menuAlgorithm_specs.menuAction())
        self.menuSpecs.addAction(self.actionSave_Specs)
        self.menuAlgorithm_specs.addAction(self.actionGerchberg_Saxton)
        self.menuAlgorithm_specs.addAction(self.actionEPRY)
        self.menuAlgorithm_specs.addAction(self.actionGauss_Newton)
        self.menuAlgorithm_specs.addAction(self.actionKramers_Kronig)
        self.menuAlgorithm_specs.addAction(self.actionAPIC)
        self.menuHelp.addAction(self.actionSoftware_Guide)
        self.menuHelp.addAction(self.actionReferences)
        self.menuMessageBox.addAction(self.actionSave_Messgaes)
        self.menuMessageBox.addAction(self.actionClear_Messages)

        self.retranslateUi(FPMSoftware)

        QMetaObject.connectSlotsByName(FPMSoftware)
    # setupUi

    def retranslateUi(self, FPMSoftware):
        FPMSoftware.setWindowTitle(QCoreApplication.translate("FPMSoftware", u"MainWindow", None))
        self.actionLoad_Data.setText(QCoreApplication.translate("FPMSoftware", u"Load Data", None))
        self.actionSystem_Spec.setText(QCoreApplication.translate("FPMSoftware", u"Load Data Batch", None))
        self.actionAlgorithm_Spec.setText(QCoreApplication.translate("FPMSoftware", u"Default Setting", None))
        self.actionSave_Reults.setText(QCoreApplication.translate("FPMSoftware", u"Save Reults", None))
        self.actionLoad_Results.setText(QCoreApplication.translate("FPMSoftware", u"Load Results", None))
        self.actionShow_single_raw_frame.setText(QCoreApplication.translate("FPMSoftware", u"Single raw frame", None))
        self.actionShow_all_raw_frames.setText(QCoreApplication.translate("FPMSoftware", u"All raw frames", None))
        self.actionSingle_raw_spectrum.setText(QCoreApplication.translate("FPMSoftware", u"Single raw spectrum", None))
        self.actionAll_raw_spectrum.setText(QCoreApplication.translate("FPMSoftware", u"All raw spectra", None))
        self.actionAmplitude_result.setText(QCoreApplication.translate("FPMSoftware", u"Amplitude result", None))
        self.actionPhase_result.setText(QCoreApplication.translate("FPMSoftware", u"Phase result", None))
        self.actionPupil_function.setText(QCoreApplication.translate("FPMSoftware", u"Pupil function", None))
        self.actionAll_results.setText(QCoreApplication.translate("FPMSoftware", u"All results", None))
        self.actionCheck_systerm_specs.setText(QCoreApplication.translate("FPMSoftware", u"Load Specs", None))
        self.actionSystem_specs.setText(QCoreApplication.translate("FPMSoftware", u"System specs", None))
        self.actionGerchberg_Saxton.setText(QCoreApplication.translate("FPMSoftware", u"Gerchberg-Saxton", None))
        self.actionEPRY.setText(QCoreApplication.translate("FPMSoftware", u"EPRY", None))
        self.actionGauss_Newton.setText(QCoreApplication.translate("FPMSoftware", u"Gauss-Newton", None))
        self.actionKramers_Kronig.setText(QCoreApplication.translate("FPMSoftware", u"Kramers-Kronig", None))
        self.actionAPIC.setText(QCoreApplication.translate("FPMSoftware", u"APIC", None))
        self.actionSoftware_Guide.setText(QCoreApplication.translate("FPMSoftware", u"Software Guide", None))
        self.actionReferences.setText(QCoreApplication.translate("FPMSoftware", u"References", None))
        self.actionSave_Messgaes.setText(QCoreApplication.translate("FPMSoftware", u"Export Messgaes", None))
        self.actionClear_Messages.setText(QCoreApplication.translate("FPMSoftware", u"Clear Messages", None))
        self.actionSave_Specs.setText(QCoreApplication.translate("FPMSoftware", u"Save Specs", None))
        self.actionSIngle_ROI.setText(QCoreApplication.translate("FPMSoftware", u"SIngle ROI image", None))
        self.actionAll_ROI_images.setText(QCoreApplication.translate("FPMSoftware", u"All ROI images", None))
        self.load_butt.setText(QCoreApplication.translate("FPMSoftware", u"Load", None))
        self.roi_butt.setText(QCoreApplication.translate("FPMSoftware", u"ROI", None))
        self.run_butt.setText(QCoreApplication.translate("FPMSoftware", u"Run", None))
        self.save_butt.setText(QCoreApplication.translate("FPMSoftware", u"Save", None))
        self.acknowledge_text.setPlainText(QCoreApplication.translate("FPMSoftware", u"Designed by Haowen Zhou.\n"
"https://hwzhou2020.github.io/\n"
"Caltech Biophotonics Lab", None))
        self.Msg_window.setPlainText(QCoreApplication.translate("FPMSoftware", u"Welcome to Fourier Ptychographic Microscopy reconstruction algorithm software!", None))
        self.menuFile.setTitle(QCoreApplication.translate("FPMSoftware", u"File", None))
        self.menuDisplay.setTitle(QCoreApplication.translate("FPMSoftware", u"Display", None))
        self.menuSpecs.setTitle(QCoreApplication.translate("FPMSoftware", u"Specs", None))
        self.menuAlgorithm_specs.setTitle(QCoreApplication.translate("FPMSoftware", u"Algorithm specs", None))
        self.menuHelp.setTitle(QCoreApplication.translate("FPMSoftware", u"Help", None))
        self.menuMessageBox.setTitle(QCoreApplication.translate("FPMSoftware", u"MessageBox", None))
    # retranslateUi

