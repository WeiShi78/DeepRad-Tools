"""
DeepRad Normalize (deeprad_normalize)

Calculates normalization information for folders full of NifTI images (.nii or .nii.gz files).
Specifically, this tool add normalization information as a JSON file (.deeprad) matching the 
NiFTI file so that other DeepRad tools can utilize these data as properly normalized inputs
into deep learning algorithms. Running this tool is most likely a pre-requisite before running
other DeepRad tools.
Note the NifTI file is not modified as a result of this tool. However, write permission in the
folders where the NiFTI files are stored is required.
"""

# deeprad_normalize
# Copyright 2019 by Alan McMillan, University of Wisconsin
# All rights reserved.
# This file is part of DeepRad and is released under the "MIT License Agreement".
# Please see the LICENSE file that should have been included as part of this package

from PIL import Image
from glob import glob
from tqdm import tqdm
# from dynamic_tqdm import setup_logging, setup_streams_redirection

import os
import sys
import time
import shutil
import logging
import nibabel
import argparse
import itertools
import json
import dynamic_tqdm
import tqdm.auto as t_AUTO

import numpy as np

class GuiLogger(logging.Handler):
    def emit(self, record):
        text = self.edit.toPlainText()+'\n'+self.format(record)
        self.edit.setPlainText(text)  # implementation of append_line omitted

def arg_parser():
    """
    Function to return the command line argument parse for deeprad_normalize
    """
    parser = argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter,add_help=True)
    parser.add_argument('--folder',type=str,nargs='+',required=True,help='path(s) to input data (can be multiple folders separated by spaces)')
    group1 = parser.add_mutually_exclusive_group(required=True)
    group1.add_argument('--volumenorm',action='store_true',help='normalize input data [0,1] in a volumewise manner')
    group1.add_argument('--globalnorm',action='store_true',help='normalize input data [0,1] in a global manner (caution: ranges are computed volumewise and applied globally. This requires two passes through the data)')
    group1.add_argument('--volumezscore',action='store_true',help='normalize input data into Z score (data-mean)/stdev in a volumewise manner')
    group1.add_argument('--globalzscore',action='store_true',help='normalize input data into Z score (data-mean)/stdev in a global manner (caution: ranges are computed volumewise and applied globally. This requires two passes through the data)')
    group1.add_argument('--customnorm',action='store_true',help='normalize with custom factors: (data-shift)/scale')
    group1.add_argument('--nonorm',action='store_true',)
    parser.add_argument('--shift',type=float,default=0.0,help='user-specified shift to apply')
    parser.add_argument('--scale',type=float,default=1.0,help='user-specified scale factor to apply')
    parser.add_argument('--cropabove',type=float,default=100.0,help='crop pixel values above (greater than) the specified percentile [e.g., 95]. Note: does not apply to Z score normalizations.')
    parser.add_argument('--cropbelow',type=float,default=0.0,help='crop pixel values below (greater than) the specified percentile [e.g., 5]. Note: does not apply to Z score normalizations.')
    return parser

def glob_nii(folder):
    """"
    Function to return a sorted list of .nii and/or .nii.gz filenames from the specified folder

    Parameters
        folder: The input folder with .nii and/or .nii.gz files

    Returns
        A sorted list of .nii and/or .nii.gz files in folder
    """
    return sorted(glob(os.path.join(folder,'*.nii.gz'),recursive=True)) + sorted(glob(os.path.join(folder,'*.nii'),recursive=True))

def main():
    args = arg_parser().parse_args()
    process_norm(args)

def process_norm(args):
    #
    # logger = logging.getLogger()
    # # set up logging
    # logger.setLevel(logging.DEBUG)
    # # create console handler and set level to info
    # handler = logging.StreamHandler()
    # handler.setLevel(logging.INFO)
    # formatter = logging.Formatter('%(message)s')
    # handler.setFormatter(formatter)
    # logger.addHandler(handler)
    # # create error file handler and set level to info
    # logfile = os.path.join(args.folder[0],'deeprad.log')
    # handler = logging.FileHandler(logfile,'w', encoding=None, delay='true')
    # handler.setLevel(logging.INFO)
    # formatter = logging.Formatter(fmt='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    # handler.setFormatter(formatter)
    # logger.addHandler(handler)

    # # output log to QT GUI
    # h = GuiLogger()
    # h.edit = args.log_output  # this should be done in __init__
    # logger.addHandler(h)

    # dynamic tqdm setting
    dynamic_tqdm.setup_logging('DR_norm')
    _logger = logging.getLogger('DR_norm')
    _logger.setLevel(logging.DEBUG)

    tabs = ''
    indata = list( itertools.chain.from_iterable( [ glob_nii(f) for f in args.folder ] ) )
    # logger.info(args.folder)

    _logger.info(tabs+'deeprad_normalize -- a tool to write applicaiton-specific normalization information to Nifti headers')
    _logger.info(tabs+'{} files were found in {} folder(s)'.format(len(indata),len(args.folder)))

    # for global normalization we need to keep track data ranges
    globaldata_norm1 = np.zeros(len(indata))
    globaldata_norm2 = np.zeros(len(indata))

    if args.customnorm:
        _logger.info(tabs+'Applying custom normalization (shift={}, scale={})...'.format(args.shift,args.scale))
    elif args.volumenorm:
        _logger.info(tabs+'Computing volume-wise normalization...')
    elif args.globalnorm or args.globalzscore:
        _logger.info(tabs+'Computing global normalization...')
        # loop through all of the files
        #for curr_file in indata:
        for i in tqdm(range(len(indata)),desc='Determining global scaling factors'):
            curr_file = indata[i]
            curr_nii = nibabel.load(curr_file)
            curr_data = curr_nii.get_fdata()

            if args.globalnorm:
                globaldata_norm1[i] = np.percentile(curr_data,args.cropbelow)
                globaldata_norm2[i] = np.percentile(curr_data,args.cropabove)
            elif args.globalzscore:
                globaldata_norm1[i] = np.mean(curr_data)
                globaldata_norm2[i] = np.std(curr_data)

        if args.globalnorm:
            global_min = np.min(globaldata_norm1)
            global_max = np.max(globaldata_norm2)
            _logger.info(tabs+' Global min = {} (@ {}%-ile)'.format(global_min,args.cropbelow))
            _logger.info(tabs+' Global max = {} (@ {}%-ile)'.format(global_max,args.cropabove))
        elif args.globalzscore:
            global_mean = np.mean(globaldata_norm1)
            global_std = np.std(globaldata_norm2)
            _logger.info(tabs+' Global mean= {}'.format(global_mean))
            _logger.info(tabs+' Global std= {}'.format(global_std))

    # loop through all of the files
    tqdm_obect = t_AUTO.tqdm(range(len(indata)), unit_scale=True, dynamic_ncols=True)
    tqdm_obect.set_description("Writing normalization to header")
    # for i in tqdm(range(len(indata)),desc='Writing normalization to header'):
    for i in tqdm_obect:
        curr_file = indata[i]

        json_file = curr_file + '.deeprad'

        deepraddata = {}
        
        # calculate normalization
        if args.volumenorm: # volumewise normalization
            curr_nii = nibabel.load(curr_file)
            curr_data = curr_nii.get_fdata()

            curr_min = np.percentile(curr_data,args.cropbelow)
            curr_max = np.percentile(curr_data,args.cropabove)

            deepraddata['normtype'] = 'volume'
            deepraddata['norm1'] = curr_min
            deepraddata['norm2'] = curr_max

        elif args.volumezscore: # volumewise Z score
            curr_nii = nibabel.load(curr_file)
            curr_data = curr_nii.get_fdata()

            curr_mean = np.mean(curr_data)
            curr_std = np.std(curr_data)

            deepraddata['normtype'] = 'volumezscore'
            deepraddata['norm1'] = curr_mean
            deepraddata['norm2'] = curr_std            

        elif args.globalnorm: # global normalization
            deepraddata['normtype'] = 'global'
            deepraddata['norm1'] = global_min
            deepraddata['norm2'] = global_max   

        elif args.globalnorm: # global Z score
            deepraddata['normtype'] = 'globalzscore'
            deepraddata['norm1'] = global_mean
            deepraddata['norm2'] = global_std  

        elif args.customnorm: # custom normalization
            deepraddata['normtype'] = 'custom'
            deepraddata['norm1'] = args.shift
            deepraddata['norm2'] = args.scale

        # write to deeprad json file
        with open(json_file, 'w') as outfile:  
            json.dump(deepraddata, outfile)

        _logger.info('Processing {}/{}: {}'.format(i,len(indata),curr_file))

    _logger.info(tabs+"Normalization completed!")


if __name__ == "__main__":
    sys.exit(main())
