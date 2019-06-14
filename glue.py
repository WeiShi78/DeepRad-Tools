# -*- coding: utf-8 -*-
import deeprad_normalize as dr_n
from PyQt5 import QtCore, QtGui, QtWidgets
from types import SimpleNamespace


def backend(ui):

	# QtWidgets.QMessageBox.information(ui.button_start, "test", "I am in the glue!")

	value_folder = [ui.folder.toPlainText()]
	print("Folder:", value_folder)
	value_vn = ui.radio_vn.isChecked()
	value_gn = ui.radio_gn.isChecked()
	value_vz = ui.radio_vz.isChecked()
	value_gz = ui.radio_gz.isChecked()
	value_cn = ui.radio_cn.isChecked()
	value_nn = ui.radio_nn.isChecked()

	if ui.radio_cn.isChecked():
		value_shift = float(ui.text_shift.text())
		value_scale = float(ui.text_scale.text())
		value_cropa = float(ui.text_cropa.text())
		value_cropb = float(ui.text_cropb.text())
	else:
		value_shift = 0
		value_scale = 0
		value_cropa = 0
		value_cropb = 0


	args = SimpleNamespace(folder=value_folder,
						   volumenorm=value_vn,
						   globalnorm=value_gn,
						   volumezscore=value_vz,
						   globalzscore=value_gz,
						   customnorm=value_cn,
						   nonorm=value_nn,
						   shift=value_shift,
						   scale=value_scale,
						   cropabove=value_cropa,
						   cropbelow=value_cropb)
	dr_n.process(args)
