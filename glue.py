# -*- coding: utf-8 -*-
import deeprad_normalize as dr_norm
import deeprad_nii2img as dr_n2i
from types import SimpleNamespace


def deeprad_backend_norm(ui):

    # QtWidgets.QMessageBox.information(ui.button_start, "test", "I am in the glue!")

    value_folder = ui.norm_folder.toPlainText().split('\n')
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
    dr_norm.process_norm(args)


def deeprad_backend_n2i(ui):

    value_outfolder = ui.n2i_folder_output.toPlainText()
    value_X = [ui.n2i_folder_X.toPlainText()]
    value_Y = [ui.n2i_folder_Y.toPlainText()]

    try:
        value_axes = int(ui.n2i_text_axes.text())
    except ValueError:
        value_axes = None

    try:
        value_imsize_w = int(ui.n2i_text_imsize_w.text())
    except ValueError:
        value_imsize_w = None

    try:
        value_imsize_h = int(ui.n2i_text_imsize_h.text())
    except ValueError:
        value_imsize_h = None

    try:
        value_testfraction = int(ui.n2i_text_testfraction.text())
    except ValueError:
        value_testfraction = None

    try:
        value_valfraction = int(ui.n2i_text_valfraction.text())
    except ValueError:
        value_valfraction = None

    try:
        value_Xslices = int(ui.n2i_text_xslices.text())
    except ValueError:
        value_Xslices = None

    try:
        value_Yslices = int(ui.n2i_text_yslices.text())
    except ValueError:
        value_Yslices = None

    value_force = ui.n2i_check_force.isChecked()
    value_shuffle = ui.n2i_check_shuffle.isChecked()
    
    if value_imsize_w is None and value_imsize_h is None:
    	value_imsize = None
    else:
    	value_imsize = [value_imsize_w, value_imsize_h]

    # augmentation part
    if ui.n2i_check_aug.isChecked():
        value_augfactor = int(ui.n2i_text_augfactor.text())
        value_augseed = int(ui.n2i_text_augseed.text())
        value_addnoise = float(ui.n2i_text_addnoise.text())
        value_rotations = float(ui.n2i_text_rotations.text())
        value_scalings = float(ui.n2i_text_scalings.text())
        value_shears = float(ui.n2i_text_shears.text())
        value_translations = float(ui.n2i_text_translations.text())
        value_hflips = ui.n2i_check_hflips.isChecked()
        value_vflips = ui.n2i_check_vflips.isChecked()
        
        value_augmode = None
        if ui.n2i_radio_augmode_reflect.isChecked():
            value_augmode = 'reflect'
        if ui.n2i_radio_augmode_nearest.isChecked():
            value_augmode = 'nearest'
        if ui.n2i_radio_augmode_mirror.isChecked():
            value_augmode = 'mirror'
        if ui.n2i_radio_augmode_warp.isChecked():
            value_augmode = 'warp'

    else:
        value_augfactor = 1
        value_augseed = 0
        value_addnoise = 0
        value_rotations = 0
        value_scalings = 0
        value_shears = 0
        value_translations = 0
        value_hflips = False
        value_vflips = False
        value_augmode = None

    args = SimpleNamespace(outfolder=value_outfolder,
                           X=value_X,
                           Y=value_Y,
                           axes=value_axes,
                           imsize=value_imsize,
                           Xslices=value_Xslices,
                           Yslices=value_Yslices,
                           force=value_force,
                           shuffle=value_shuffle,
                           testfraction=value_testfraction,
                           valfraction=value_valfraction,
                           augfactor=value_augfactor,
                           augseed=value_augseed,
                           addnoise=value_addnoise,
                           rotations=value_rotations,
                           scalings=value_scalings,
                           shears=value_shears,
                           translations=value_translations,
                           hflips=value_hflips,
                           vflips=value_vflips,
                           augmode=value_augmode,
                           log_output=ui.n2i_logger)

    dr_n2i.process_n2i(args)