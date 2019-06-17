# -*- coding: utf-8 -*-
import deeprad_normalize as dr_norm
import deeprad_nii2img as nr_n2i
from PyQt5 import QtCore, QtGui, QtWidgets
from types import SimpleNamespace


def deeprad_backend_norm(ui):

	# QtWidgets.QMessageBox.information(ui.button_start, "test", "I am in the glue!")

	value_folder = [ui.norm_folder.toPlainText()]
	value_vn = ui.norm_radio_vn.isChecked()
	value_gn = ui.norm_radio_gn.isChecked()
	value_vz = ui.norm_radio_vz.isChecked()
	value_gz = ui.norm_radio_gz.isChecked()
	value_cn = ui.norm_radio_cn.isChecked()
	value_nn = ui.norm_radio_nn.isChecked()

	if ui.norm_radio_cn.isChecked():
		value_shift = float(ui.norm_text_shift.text())
		value_scale = float(ui.norm_text_scale.text())
		value_cropa = float(ui.norm_text_cropa.text())
		value_cropb = float(ui.norm_text_cropb.text())
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
						   cropbelow=value_cropb,
						   log_output=ui.norm_logger)
	dr_norm.process(args)


def deeprad_backend_n2i(ui):

	value_outfolder = [ui.n2i_outfolder.toPlainText()]
	value_X = [ui.n2i_folder_X.toPlainText()]
	value_Y = [ui.n2i_folder_Y.toPlainText()]
	value_axes = int(ui.n2i_text_axes.text())
	value_imsize = int(ui.n2i_text_imsize.text())
	value_force = ui.n2i_check_force.isChecked()
	value_shuffle = ui.n2i_check_shuffle.isChecked()

	# to be done

	# dr_n2i.process(args)