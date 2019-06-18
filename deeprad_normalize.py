"""
DeepRad Normalize (deeprad_normalize)

Calculates normalization information for folders full of NifTI images (.nii or .nii.gz files).
Specifically, this tool add normalization information as metadata to the NifTI header so that
other DeepRad tools can utilize these data as properly normalized inputs into deep learning
algorithms. Running this tool is likely a pre-requisite before running other DeepRad tools.
Note the NifTI file is modified as a result of this tool. However, the image pixel data are not
modified and only DeepRad-specific information is placed into the header. This should have no
effect on the use of the modified NifTI images in any other tool. 
"""

# deeprad_normalize
# Copyright 2019 by Alan McMillan, University of Wisconsin
# All rights reserved.
# This file is part of DeepRad and is released under the "MIT License Agreement".
# Please see the LICENSE file that should have been included as part of this package

from PIL import Image
from glob import glob
from tqdm import tqdm

import os
import sys
import shutil
import logging
import nibabel
import argparse
import itertools

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

    logger = logging.getLogger()
    # set up logging    
    logger.setLevel(logging.DEBUG)     
    # create console handler and set level to info
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    # create error file handler and set level to info
    logfile = os.path.join(args.folder[0],'deeprad.log')
    handler = logging.FileHandler(logfile,'w', encoding=None, delay='true')
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(fmt='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # output log to QT GUI
    h = GuiLogger()
    h.edit = args.log_output  # this should be done in __init__
    logger.addHandler(h)

    tabs = '---'
    indata = list( itertools.chain.from_iterable( [ glob_nii(f) for f in args.folder ] ) )
    # logger.info(args.folder)

    logger.info(tabs+'deeprad_normalize -- a tool to write applicaiton-specific normalization information to Nifti headers')
    logger.info(tabs+'{} files were found in {} folder(s)'.format(len(indata),len(args.folder)))

    # for global normalization we need to keep track data ranges
    globaldata_norm1 = np.zeros(len(indata))
    globaldata_norm2 = np.zeros(len(indata))

    if args.customnorm:
        logger.info(tabs+'Applying custom normalization (shift={}, scale={})...'.format(args.shift,args.scale))
    elif args.volumenorm:
        logger.info(tabs+'Computing volume-wise normalization...')
    elif args.globalnorm or args.globalzscore:
        logger.info(tabs+'Computing global normalization...')
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
            logger.info(tabs+' Global min = {} (@ {}%-ile)'.format(global_min,args.cropbelow))
            logger.info(tabs+' Global max = {} (@ {}%-ile)'.format(global_max,args.cropabove))
        elif args.globalzscore:
            global_mean = np.mean(globaldata_norm1)
            global_std = np.std(globaldata_norm2)
            logger.info(tabs+' Global mean= {}'.format(global_mean))
            logger.info(tabs+' Global std= {}'.format(global_std))

    # loop through all of the files
    for i in tqdm(range(len(indata)),desc='Writing normalization to header'):
        curr_file = indata[i]
        curr_nii = nibabel.load(curr_file)

        # search for a previous normalization header information and remove it
        for curr_headerext in curr_nii.header.extensions:
            curr_headerstring = curr_headerext.get_content().decode()
            # check for the previous normalization string and remove it
            if curr_headerstring.startswith('@DeepRad'):
                curr_nii.header.extensions.remove(curr_headerext)
        
        # prepare new header string
        if args.volumenorm: # volumewise normalization
            curr_data = curr_nii.get_fdata()

            curr_min = np.percentile(curr_data,args.cropbelow)
            curr_max = np.percentile(curr_data,args.cropabove)

            curr_normstring = '@DeepRad/vmin/{}/vmax/{}'.format(curr_min,curr_max)

        elif args.volumezscore: # volumewise Z score
            curr_data = curr_nii.get_fdata()

            curr_mean = np.mean(curr_data)
            curr_std = np.std(curr_data)

            curr_normstring = '@DeepRad/vmean/{}/vstd/{}'.format(curr_mean,curr_std)

        elif args.globalnorm: # global normalization
            curr_normstring = '@DeepRad/gmin/{}/gmax/{}'.format(global_min,global_max)

        elif args.globalnorm: # global Z score
            curr_normstring = '@DeepRad/gmean/{}/gstd/{}'.format(global_mean,global_std)

        elif args.customnorm: # custom normalization
            curr_normstring = '@DeepRad/cshift/{}/cscale/{}'.format(args.shift,args.scale)

        # extract directory and file names from path
        old_path = curr_nii.get_filename()
        curr_nii_path = os.path.dirname(old_path)
        curr_nii_name = os.path.basename(old_path)
        temp_path = os.path.join(curr_nii_path, "temp_"+curr_nii_name)

        # update nifti header and save
        curr_ext = nibabel.nifti1.Nifti1Extension('afni',str.encode(curr_normstring))
        curr_nii.header.extensions.append(curr_ext)
        curr_nii.to_filename( temp_path )

        # move original files to "orignal" folder
        original_folder = os.path.join(curr_nii_path, 'original')
        if not os.path.exists(original_folder):
            os.mkdir(original_folder)

        new_path = os.path.join(original_folder, curr_nii_name)
        os.rename(old_path, new_path)
        os.rename(temp_path, old_path)

        # delete 
        # shutil.rmtree('/path/to/your/dir/')

    logger.info(tabs+"Normalization completed!")



if __name__ == "__main__":
    sys.exit(main())