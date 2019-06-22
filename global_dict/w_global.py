#!/usr/bin/python
# -*- coding: UTF-8 -*-


global gbl_dict
gbl_dict = {}


def gbl_set_value(key, value):
    gbl_dict[key] = value


def gbl_get_value(key, defvalue=None):
    try:
        return gbl_dict[key]
    except KeyError:
        return defvalue


def gbl_all():
    return gbl_dict
