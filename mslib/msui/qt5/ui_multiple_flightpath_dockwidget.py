# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mslib/msui/ui/ui_multiple_flightpath_dockwidget.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MultipleViewWidget(object):
    def setupUi(self, MultipleViewWidget):
        MultipleViewWidget.setObjectName("MultipleViewWidget")
        MultipleViewWidget.resize(544, 235)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MultipleViewWidget.sizePolicy().hasHeightForWidth())
        MultipleViewWidget.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(MultipleViewWidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.list_flighttrack = QtWidgets.QListWidget(MultipleViewWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.list_flighttrack.sizePolicy().hasHeightForWidth())
        self.list_flighttrack.setSizePolicy(sizePolicy)
        self.list_flighttrack.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.list_flighttrack.setObjectName("list_flighttrack")
        self.horizontalLayout_2.addWidget(self.list_flighttrack)
        self.list_operation_track = QtWidgets.QListWidget(MultipleViewWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.list_operation_track.sizePolicy().hasHeightForWidth())
        self.list_operation_track.setSizePolicy(sizePolicy)
        self.list_operation_track.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.list_operation_track.setObjectName("list_operation_track")
        self.horizontalLayout_2.addWidget(self.list_operation_track)
        self.frame = QtWidgets.QFrame(MultipleViewWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_color = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_color.sizePolicy().hasHeightForWidth())
        self.pushButton_color.setSizePolicy(sizePolicy)
        self.pushButton_color.setObjectName("pushButton_color")
        self.verticalLayout.addWidget(self.pushButton_color)
        self.dsbx_linewidth = QtWidgets.QDoubleSpinBox(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dsbx_linewidth.sizePolicy().hasHeightForWidth())
        self.dsbx_linewidth.setSizePolicy(sizePolicy)
        self.dsbx_linewidth.setAlignment(QtCore.Qt.AlignCenter)
        self.dsbx_linewidth.setObjectName("dsbx_linewidth")
        self.verticalLayout.addWidget(self.dsbx_linewidth)
        self.horizontalLayout_2.addWidget(self.frame)
        self.horizontalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.labelStatus = QtWidgets.QLabel(MultipleViewWidget)
        self.labelStatus.setObjectName("labelStatus")
        self.verticalLayout_2.addWidget(self.labelStatus)

        self.retranslateUi(MultipleViewWidget)
        QtCore.QMetaObject.connectSlotsByName(MultipleViewWidget)

    def retranslateUi(self, MultipleViewWidget):
        _translate = QtCore.QCoreApplication.translate
        MultipleViewWidget.setWindowTitle(_translate("MultipleViewWidget", "Form"))
        self.list_flighttrack.setToolTip(_translate("MultipleViewWidget", "List of Open Flighttracks.\n"
"Check box to activate and display track on topview."))
        self.list_operation_track.setToolTip(_translate("MultipleViewWidget", "List of Mscolab Operations.\n"
"Check box to activate and display track on topview."))
        self.pushButton_color.setText(_translate("MultipleViewWidget", "Change Color"))
        self.labelStatus.setText(_translate("MultipleViewWidget", "Status: "))
