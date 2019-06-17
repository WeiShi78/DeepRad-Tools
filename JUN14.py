# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'JUN14.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from glue import backend

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(837, 855)
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 811, 831))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.textBrowser = QtWidgets.QTextBrowser(self.tab)
        self.textBrowser.setGeometry(QtCore.QRect(20, 20, 761, 761))
        self.textBrowser.setObjectName("textBrowser")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.frame = QtWidgets.QFrame(self.tab_2)
        self.frame.setGeometry(QtCore.QRect(10, 10, 781, 111))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.groupBox = QtWidgets.QGroupBox(self.frame)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 761, 91))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setCheckable(False)
        self.groupBox.setObjectName("groupBox")
        self.folder = QtWidgets.QPlainTextEdit(self.groupBox)
        self.folder.setGeometry(QtCore.QRect(10, 30, 741, 51))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.folder.setFont(font)
        self.folder.setObjectName("folder")
        self.frame_2 = QtWidgets.QFrame(self.tab_2)
        self.frame_2.setGeometry(QtCore.QRect(10, 130, 781, 571))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.groupBox_2 = QtWidgets.QGroupBox(self.frame_2)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 10, 761, 541))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setCheckable(False)
        self.groupBox_2.setObjectName("groupBox_2")
        self.radio_vn = QtWidgets.QRadioButton(self.groupBox_2)
        self.radio_vn.setGeometry(QtCore.QRect(20, 60, 121, 21))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.radio_vn.setFont(font)
        self.radio_vn.setObjectName("radio_vn")
        self.radio_gn = QtWidgets.QRadioButton(self.groupBox_2)
        self.radio_gn.setGeometry(QtCore.QRect(20, 90, 121, 21))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.radio_gn.setFont(font)
        self.radio_gn.setObjectName("radio_gn")
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setGeometry(QtCore.QRect(160, 60, 561, 21))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setGeometry(QtCore.QRect(160, 30, 91, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setGeometry(QtCore.QRect(20, 30, 91, 21))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setGeometry(QtCore.QRect(160, 90, 561, 21))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setGeometry(QtCore.QRect(160, 110, 561, 21))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setGeometry(QtCore.QRect(160, 130, 561, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.radio_vz = QtWidgets.QRadioButton(self.groupBox_2)
        self.radio_vz.setGeometry(QtCore.QRect(20, 160, 121, 21))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.radio_vz.setFont(font)
        self.radio_vz.setObjectName("radio_vz")
        self.label_7 = QtWidgets.QLabel(self.groupBox_2)
        self.label_7.setGeometry(QtCore.QRect(160, 160, 561, 21))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.radio_gz = QtWidgets.QRadioButton(self.groupBox_2)
        self.radio_gz.setGeometry(QtCore.QRect(20, 190, 121, 21))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.radio_gz.setFont(font)
        self.radio_gz.setObjectName("radio_gz")
        self.label_8 = QtWidgets.QLabel(self.groupBox_2)
        self.label_8.setGeometry(QtCore.QRect(160, 190, 561, 21))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.groupBox_2)
        self.label_9.setGeometry(QtCore.QRect(160, 210, 561, 21))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.groupBox_2)
        self.label_10.setGeometry(QtCore.QRect(160, 230, 561, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.radio_cn = QtWidgets.QRadioButton(self.groupBox_2)
        self.radio_cn.setGeometry(QtCore.QRect(20, 260, 121, 21))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.radio_cn.setFont(font)
        self.radio_cn.setObjectName("radio_cn")
        self.label_11 = QtWidgets.QLabel(self.groupBox_2)
        self.label_11.setGeometry(QtCore.QRect(160, 260, 561, 21))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.radio_nn = QtWidgets.QRadioButton(self.groupBox_2)
        self.radio_nn.setGeometry(QtCore.QRect(20, 290, 121, 21))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.radio_nn.setFont(font)
        self.radio_nn.setObjectName("radio_nn")
        self.label_12 = QtWidgets.QLabel(self.groupBox_2)
        self.label_12.setGeometry(QtCore.QRect(160, 290, 561, 21))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.frame_3 = QtWidgets.QFrame(self.groupBox_2)
        self.frame_3.setGeometry(QtCore.QRect(20, 320, 731, 201))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.label_13 = QtWidgets.QLabel(self.frame_3)
        self.label_13.setGeometry(QtCore.QRect(20, 10, 211, 21))
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self.frame_3)
        self.label_14.setGeometry(QtCore.QRect(40, 40, 71, 21))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.text_shift = QtWidgets.QLineEdit(self.frame_3)
        self.text_shift.setGeometry(QtCore.QRect(130, 40, 61, 23))
        self.text_shift.setObjectName("text_shift")
        self.label_15 = QtWidgets.QLabel(self.frame_3)
        self.label_15.setGeometry(QtCore.QRect(40, 70, 71, 21))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(self.frame_3)
        self.label_16.setGeometry(QtCore.QRect(40, 100, 71, 21))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_16.setFont(font)
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(self.frame_3)
        self.label_17.setGeometry(QtCore.QRect(40, 150, 71, 21))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_17.setFont(font)
        self.label_17.setObjectName("label_17")
        self.text_scale = QtWidgets.QLineEdit(self.frame_3)
        self.text_scale.setGeometry(QtCore.QRect(130, 70, 61, 23))
        self.text_scale.setText("")
        self.text_scale.setObjectName("text_scale")
        self.text_cropa = QtWidgets.QLineEdit(self.frame_3)
        self.text_cropa.setGeometry(QtCore.QRect(130, 100, 61, 23))
        self.text_cropa.setObjectName("text_cropa")
        self.text_cropb = QtWidgets.QLineEdit(self.frame_3)
        self.text_cropb.setGeometry(QtCore.QRect(130, 150, 61, 23))
        self.text_cropb.setObjectName("text_cropb")
        self.label_18 = QtWidgets.QLabel(self.frame_3)
        self.label_18.setGeometry(QtCore.QRect(220, 40, 481, 21))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")
        self.label_19 = QtWidgets.QLabel(self.frame_3)
        self.label_19.setGeometry(QtCore.QRect(220, 70, 481, 21))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_19.setFont(font)
        self.label_19.setObjectName("label_19")
        self.label_20 = QtWidgets.QLabel(self.frame_3)
        self.label_20.setGeometry(QtCore.QRect(220, 100, 481, 21))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_20.setFont(font)
        self.label_20.setObjectName("label_20")
        self.label_21 = QtWidgets.QLabel(self.frame_3)
        self.label_21.setGeometry(QtCore.QRect(220, 120, 481, 21))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_21.setFont(font)
        self.label_21.setObjectName("label_21")
        self.label_22 = QtWidgets.QLabel(self.frame_3)
        self.label_22.setGeometry(QtCore.QRect(220, 150, 481, 21))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_22.setFont(font)
        self.label_22.setObjectName("label_22")
        self.label_23 = QtWidgets.QLabel(self.frame_3)
        self.label_23.setGeometry(QtCore.QRect(220, 170, 481, 21))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_23.setFont(font)
        self.label_23.setObjectName("label_23")
        self.button_start = QtWidgets.QPushButton(self.tab_2)
        self.button_start.setGeometry(QtCore.QRect(10, 710, 80, 23))
        self.button_start.setObjectName("button_start")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tabWidget.addTab(self.tab_3, "")

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.button_start.clicked.connect(self.connect_to_backend)


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.textBrowser.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">DeepRad-Tools</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Commandline tools to facilitate the use of Medical Images (from NifTI files) to standard image files (TIFF files) so that these datasets can be readily consumed by deep learning frameworks as used for computer vision.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">It currently consists of three tools: <span style=\" font-weight:600; font-style:italic;\">deeprad_keras_tools</span><span style=\" font-style:italic;\">, </span><span style=\" font-weight:600; font-style:italic;\">deeprad_nii2img</span>, and <span style=\" font-weight:600; font-style:italic;\">deeprad_normalize.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-weight:600; font-style:italic;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">DeepRad-Tools</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">This tool converts organized folders of NifTI images (.nii or .nii.gz files) to standard</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">TIFF files and optionally performs augmentation (random alterations) to input images.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The rationale for this tool is that image file formats that are often used in medical imaging</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">are not directly compatible with software frameworks that are most commonly used for deep</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">learning. This tool takes NifTI data, which is a convenient format for volumetric medical</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">imaging data because it maintains subject-specific spatial transformations of pixel data.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">For more information about NifTI, go here: https://nifti.nimh.nih.gov</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">This tool takes folders containing NifTI data as input and writes a new folder structure</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">containing TIFF files that can be readily consumed by a variety of deep learning tools.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The advantage of using this strategy is that datasets that are larger than the physical</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">RAM of a system can be readily consumed. While there is likely an I/O performance loss</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">compared to other big data storage strategies such as HDF, there is a great deal of </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">flexibility presented by the proposed approach. First, given that standard image files</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">are used, they are readily viewed and consumed by a wide range of existing software tools.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">This is incredibly useful for performing visual checks of input and output data. Second,</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">because images are written as floating-point 32-bit floating point data, there is little</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">or no loss to dyanmic range as would occur with integer file formats. Finally, the tool</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">utilizes a reshaping strategy to enable multiple inputs and/or 3D inputs to be provided</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">by writing into 2D images. Because reshaping is a common operation, it is straightforward</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">to reshape inputs and outputs to use TIFF images as an intermediate format.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Note that it is a pre-requisite to use DeepRad Normalize (deeprad_normalize) before using</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">this tool to calculate the proper scale factors for input and output data.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Input is expected as a list of one or more folders for input (--X) and target</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">output ground truth (--Y) data. Output is written into the specified folder (--outfolder)</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">in the following format if validation or testing fractions are specified:</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">```</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    -OUTFOLDER</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">        -X</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">            -test</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">            -train</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">            -val</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">        -Y</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">            -test</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">            -train</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">            -val</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">```</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Or if validiation or tesing fractions are not specified:</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">```</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    -OUTFOLDER</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">        -X</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">        -Y</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">```</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">This folder structure will facilitate integration into a variety of deep learning frameworks</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Current limitations of 06/2019:</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"> - only handles 2D slices, 3D patches coming soon</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"> - is optimized to image-to-image translations, segmentation needs to be validated. Classification and regression capability (mapped to a CSV file) are forthcoming</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"> - augmentation strategies are currently limited to affine transformations</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"> - 4D NifTI data is not properly handled and will likely break things</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Try running deeprad_nii2img --help for specific help and command line options</p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "Introduction"))
        self.groupBox.setTitle(_translate("Dialog", "Image Folder"))
        self.folder.setPlainText(_translate("Dialog", "./data/"))
        self.groupBox_2.setTitle(_translate("Dialog", "Normalization Options"))
        self.radio_vn.setText(_translate("Dialog", "Volume Norm"))
        self.radio_gn.setText(_translate("Dialog", "Global Norm"))
        self.label.setText(_translate("Dialog", "Normalize input data [0,1] in a volumewise manner"))
        self.label_2.setText(_translate("Dialog", "Description"))
        self.label_3.setText(_translate("Dialog", "Methods"))
        self.label_4.setText(_translate("Dialog", "Normalize input data [0,1] in a global manner"))
        self.label_5.setText(_translate("Dialog", "Caution: ranges are computed volumewise and applied globally. "))
        self.label_6.setText(_translate("Dialog", "This requires two passes through the data"))
        self.radio_vz.setText(_translate("Dialog", "Volume Zscore"))
        self.label_7.setText(_translate("Dialog", "Normalize input data into Z score (data-mean)/stdev in a volumewise manner"))
        self.radio_gz.setText(_translate("Dialog", "Global Zscore"))
        self.label_8.setText(_translate("Dialog", "Normalize input data into Z score (data-mean)/stdev in a global manner"))
        self.label_9.setText(_translate("Dialog", "Caution: ranges are computed volumewise and applied globally. "))
        self.label_10.setText(_translate("Dialog", "This requires two passes through the data"))
        self.radio_cn.setText(_translate("Dialog", "Custom Norm"))
        self.label_11.setText(_translate("Dialog", "Normalize with custom factors: (data-shift)/scale"))
        self.radio_nn.setText(_translate("Dialog", "No Norm"))
        self.label_12.setText(_translate("Dialog", "No normalization is applied."))
        self.label_13.setText(_translate("Dialog", "Parameters for Custom Norm"))
        self.label_14.setText(_translate("Dialog", "Shift"))
        self.label_15.setText(_translate("Dialog", "Scale"))
        self.label_16.setText(_translate("Dialog", "Crop-above"))
        self.label_17.setText(_translate("Dialog", "Crop-below"))
        self.label_18.setText(_translate("Dialog", "User-specified shift to apply"))
        self.label_19.setText(_translate("Dialog", "User-specified scale factor to apply"))
        self.label_20.setText(_translate("Dialog", "Crop pixel values above (greater than) the specified percentile [e.g., 95]."))
        self.label_21.setText(_translate("Dialog", "Note: does not apply to Z score normalizations."))
        self.label_22.setText(_translate("Dialog", "Crop pixel values below (less than) the specified percentile [e.g., 5]."))
        self.label_23.setText(_translate("Dialog", "Note: does not apply to Z score normalizations."))
        self.button_start.setText(_translate("Dialog", "Start"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "Normalize"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Dialog", "nii2img"))

    def connect_to_backend(self):
        deeprad_backend(self)

