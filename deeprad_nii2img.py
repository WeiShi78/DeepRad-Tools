"""DeepRad Nii2Img (deeprad_nii2img)

This tool converts organized folders of NifTI images (.nii or .nii.gz files) to standard
TIFF files and optionally performs augmentation (random alterations) to input images.
The rationale for this tool is that image file formats that are often used in medical imaging
are not directly compatible with software frameworks that are most commonly used for deep
learning. This tool takes NifTI data, which is a convenient format for volumetric medical
imaging data because it maintains subject-specific spatial transformations of pixel data.
For more information about NifTI, go here: https://nifti.nimh.nih.gov

This tool takes folders containing NifTI data as input and writes a new folder structure
containing TIFF files that can be readily consumed by a variety of deep learning tools.
The advantage of using this strategy is that datasets that are larger than the physical
RAM of a system can be readily consumed. While there is likely an I/O performance loss
compared to other big data storage strategies such as HDF, there is a great deal of 
flexibility presented by the proposed approach. First, given that standard image files
are used, they are readily viewed and consumed by a wide range of existing software tools.
This is incredibly useful for performing visual checks of input and output data. Second,
because images are written as floating-point 32-bit floating point data, there is little
or no loss to dyanmic range as would occur with integer file formats. Finally, the tool
utilizes a reshaping strategy to enable multiple inputs and/or 3D inputs to be provided
by writing into 2D images. Because reshaping data is a common operation in all deep learning
toolkits, it is straightforward to reshape inputs and outputs to allow the use of TIFF
images as an intermediate format for deep learning.

Note that it is a pre-requisite to use DeepRad Normalize (deeprad_normalize) before using
this tool to calculate the proper scale factors for input and output data. This means there
should be .deeprad files matching your .nii/.nii.gz files in your input image data folders.

Input is expected as a list of one or more folders for input (--X) and target
output ground truth (--Y) data. Output is written into the specified folder (--outfolder)
in the following format if validation or testing fractions are specified:
    -OUTFOLDER
        -X
            -test
            -train
            -val
        -Y
            -test
            -train
            -val

Or if validiation or tesing fractions are not specified:
    -OUTFOLDER
        -X
        -Y

This folder structure will facilitate integration into a variety of deep learning frameworks

Current limitations of 06/2019:
    * only handles 2D slices, 3D patches coming soon
    * is optimized to image-to-image translations, segmentation needs to be validated.
        Classification and regression capability (mapped to a CSV file) are forthcoming
    * augmentation strategies are currently limited to affine transformations
    * 4D NifTI data is not properly handled and will likely break things

Try running deeprad_nii2img --help for specific help and command line options
"""

# deeprad_nii2img
# Copyright 2019 by Alan McMillan, University of Wisconsin
# All rights reserved.
# This file is part of DeepRad and is released under the "MIT License Agreement".
# Please see the LICENSE file that should have been included as part of this package

import argparse
import glob
import logging
import nibabel
import numpy as np
import os
import sys
import time
import copy
import warnings
import json
from glob import glob
from PIL import Image
from scipy.ndimage import rotate
from scipy.ndimage.interpolation import shift
from scipy.ndimage import zoom
from scipy.ndimage import affine_transform
from tqdm import tqdm
from random import random

# global variables
# logger = logging.getLogger()

class GuiLogger(logging.Handler):
    def emit(self, record):
        text = self.edit.toPlainText()+'\n'+self.format(record)
        self.edit.setPlainText(text)  # implementation of append_line omitted

def arg_parser():
    """
    Function to return the command line argument parse for deeprad_nii2img
    """
    parser = argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter,add_help=True)
    parser.add_argument('--outfolder', type=str, required=True,
                        help='path to output folder where images will be written')
    parser.add_argument('--X', type=str, nargs='+', required=True,
                        help='path to nifti image directory containing input data (X)')
    parser.add_argument('--Y', type=str, nargs='+', required=True,
                        help='path to nifti image directory containing target ground truth data (Y)')
    parser.add_argument('--axes', type=int, default=2, nargs='+', required=True, choices=[0,1,2],
                        help='Axes of the 3d image array on which to sample the slices (can be 0 or 1 or 2 or any multiple combination)')
    parser.add_argument('--imsize', type=int, nargs=2,
                        help='force size of input images to be X by Y in size. This is useful if you are using multiple --axes for non-isotropic data. If not specified, data will be resized to the size of the first dataset.')
    parser.add_argument('--force',action='store_true',help='Force writing into existing folder')                        
    parser.add_argument('--Xslices', type=int, default=1, choices=range(1,6,2),
                        help='Number of adjacent slices to store from input data (X)')
    parser.add_argument('--Yslices', type=int, default=1, choices=range(1,6,2),
                        help='Number of adjacent slices to store from input data (Y)')
    parser.add_argument('--shuffle', action='store_true', help='Shuffle the order of input data. Use with --augseed to produce different samplings')
    parser.add_argument('--testfraction', type=int, default=0.0, choices=range(0,100,5), help='Fraction of data as an integer percentage that will be used as testing')
    parser.add_argument('--valfraction', type=int, default=0.0, choices=range(0,100,5), help='Fraction of data as an integer percentage that will be used as validation')
    auggroup = parser.add_argument_group('Augmentation options')
    auggroup.add_argument('--augfactor', type=int, default=5, nargs=1, help='The augmentation factor applied. This is how many passes through the data augmentation will perform.')
    auggroup.add_argument('--augmode', type=str, default='reflect', choices=['mirror','nearest','reflect','wrap'],
                        help='Determines how the augmented data is extended beyond its boundaries. See scipy.ndimage documentation for more information')
    auggroup.add_argument('--augseed',type=int,nargs=1,default=813,help='Random seed to set for reproducible augmentation')
    auggroup.add_argument('--addnoise',type=float,nargs=1,default=0,help='Add Gaussian noise by this factor')
    auggroup.add_argument('--hflips',action='store_true',help='Perform random horizontal flips')
    auggroup.add_argument('--vflips',action='store_true',help='Perform random horizontal flips')
    auggroup.add_argument('--rotations',type=float,nargs=1,default=0,help='Perform random rotations up to this angle (in degrees)')
    auggroup.add_argument('--scalings',type=float,nargs=1,default=0,help='Perform random scalings between the range [(1-scale),(1+scale)]')
    auggroup.add_argument('--shears',type=float,nargs=1,default=0,help='Add random shears by up to this angle (in degrees)')
    auggroup.add_argument('--translations',type=float,nargs=1,default=0,help='Perform random translations by up to this number of pixels')
    return parser

def glob_nii(folder):
    """
    Function to return a sorted list of .nii and/or .nii.gz filenames from the specified folder

    Parameters
        folder: The input folder with .nii and/or .nii.gz files

    Returns
        A sorted list of .nii and/or .nii.gz files in folder
    """
    return sorted(glob(os.path.join(folder,'*.nii.gz'),recursive=True)) + sorted(glob(os.path.join(folder,'*.nii'),recursive=True))

def main():
    # parse args
    args = arg_parser().parse_args()
    if args.logger is None:
        args()['logger'] = logging.getLogger()
    process_n2i(args)


def setup_logger(args):
    logger = logging.getLogger(str(random()))

    # set up logging
    logger.setLevel(logging.DEBUG)
    # create console handler and set level to info
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    # create error file handler and set level to info
    logfile = os.path.join(args.outfolder, 'deeprad.log')
    handler = logging.FileHandler(logfile, 'w', encoding=None, delay='true')
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(fmt='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def process_n2i(args):

    # fix random seet for reproducibility
    np.random.seed(args.augseed)

    # check output folder
    os.makedirs(args.outfolder,exist_ok=True)

    logger = setup_logger(args)

    # # output log to QT GUI
    # h = GuiLogger()
    # h.edit = args.log_output  # this should be done in __init__
    # logger.addHandler(h)
    tabs = '---'

    logger.info(tabs+'Started {}'.format(sys.argv[0]))

    # for clarity, repeat the command line options
    cmd_line_options = ' '.join(sys.argv[1:])
    logger.info(tabs+'Command line options were: {}'.format(cmd_line_options))

    # get file names and check that we have a similar count
    X_files = [glob_nii(f) for f in args.X]
    num_files = len(X_files[0])
    for i in range(len(X_files)):
        if len(X_files[i]) != num_files:
            err_msg = 'The number of files in folder {} is {}. I expected to see {}.'.format(args.X[i],len(X_files[i]),num_files)
            logger.error(err_msg)
            raise ValueError(err_msg)
    Y_files = [glob_nii(f) for f in args.Y]
    for i in range(len(Y_files)):
        if len(Y_files[i]) != num_files:
            err_msg = 'The number of files in folder {} is {}. I expected to see {}.'.format(args.Y[i],len(Y_files[i]),num_files)
            logger.error(err_msg)
            raise ValueError(err_msg)

    logger.info(tabs+'{} inputs (X) will be matched to {} outputs (Y) across {} observations (subjects)'.format(len(X_files),len(Y_files),num_files))

    do_testdata = True if (args.testfraction>0) else False
    do_valdata = True if (args.valfraction>0) else False

    num_test = int( num_files*args.testfraction/100 )
    num_val = int( num_files*args.valfraction/100 )
    num_train = num_files - num_val - num_test
    logger.info(tabs+'{} observations will be used for training, {} for validation, and {} for testing'.format(num_train,num_val,num_test))

    # check output folders
    X_folder = os.path.join(args.outfolder,'X')
    Y_folder = os.path.join(args.outfolder,'Y')
    if not args.force:
        if os.path.isdir(X_folder):
            err_msg = 'Output folder {} is not empty. Cannot continue.'.format(X_folder)
            logger.error(err_msg)
            raise ValueError(err_msg)
        if os.path.isdir(Y_folder):
            err_msg = 'Output folder {} is not empty. Cannot continue.'.format(Y_folder)
            logger.error(err_msg)            
            raise ValueError(err_msg)
    else:
        logger.info(tabs+'CAUTION: The option --force was specified. Existing images WILL NOT be overwritten, but performance will be degraded')

    os.makedirs(X_folder,exist_ok=True)
    if do_testdata or do_valdata:
        os.makedirs(os.path.join(X_folder,'train'),exist_ok=True)
        if do_testdata:
            os.makedirs(os.path.join(X_folder,'test'),exist_ok=True)
        if do_valdata:
            os.makedirs(os.path.join(X_folder,'val'),exist_ok=True)

    os.makedirs(Y_folder,exist_ok=True)
    if do_testdata or do_valdata:
        os.makedirs(os.path.join(Y_folder,'train'),exist_ok=True)
        if do_testdata:
            os.makedirs(os.path.join(Y_folder,'test'),exist_ok=True)
        if do_valdata:
            os.makedirs(os.path.join(Y_folder,'val'),exist_ok=True)

    logger.info(tabs+'Generating {}x samples per observation with augmentation'.format(args.augfactor))
    
    # shuffle input data if requested
    file_order = np.random.permutation(num_files) if args.shuffle else range(num_files)

    check_first_file = True # we want to check the size of the first file to make sure all inputs are consistently sized
    force_count = 0 # for --force option, keep track of existing files that were skipped to speed up
    subject_count = 0 # count for file writing
    for i in range(num_files):
        for axis in args.axes:

            # read in data
            curr_X_files = [f[file_order[i]] for f in X_files]
            curr_Y_files = [f[file_order[i]] for f in Y_files]
            X_vol = np.stack([get_nii_data(f, logger) for f in curr_X_files])
            Y_vol = np.stack([get_nii_data(f, logger) for f in curr_Y_files])

            # transpose so that the sampled slice is the last dimension
            if axis == 0:
                X_vol = np.transpose( X_vol, (0,2,3,1))
                Y_vol = np.transpose( Y_vol, (0,2,3,1))
            elif axis == 1:
                X_vol = np.transpose( X_vol, (0,1,3,2))
                Y_vol = np.transpose( Y_vol, (0,1,3,2))

            # fix the output size to the specified value or to that of the first file
            if check_first_file:
                if args.imsize is not None:
                    output_shape = args.imsize
                else:
                    output_shape = X_vol.shape[1:3]
                check_first_file = False
             
            logger.info(tabs+'X[{}] => Y[{}]'.format(' '.join(curr_X_files),' '.join(curr_Y_files)))

            # check to make sure the data is matching in size, otherwise skip this data
            if X_vol.shape[1:4] != Y_vol.shape[1:4]:
                warn_msg = 'Specified X and Y are not identically sized in x,y,z. They must be skipped.'
                logger.warning(warn_msg)
                warnings.warn(warn_msg)
                continue # skip this file

            # the number of samples could vary if there are a different number of slices
            num_samples = args.augfactor * X_vol.shape[3]

            # keep track of subject count (might not map 1:1 if multiple axes are supplied)
            subject_count += 1

            for j in tqdm(range(num_samples),desc='{} of {}'.format(i+1,num_files)):

                # get random slice location
                max_slices = np.max( args.Xslices + args.Yslices )
                z_loc = np.random.randint( (0+max_slices//2), (X_vol.shape[3]-max_slices//2)-1 )
                X = get_slice_chunks( X_vol, z_loc, args.Xslices )
                Y = get_slice_chunks( Y_vol, z_loc, args.Yslices )

                # now flatten so that repeated volumes are in 3rd dimension
                if np.ndim(X) == 4:
                    X = np.transpose( X, (1,2,3,0) )
                X = np.reshape( X, (X.shape[0],X.shape[1],-1), order='F' )

                if np.ndim(Y) == 4:
                    Y = np.transpose( Y, (1,2,3,0) )
                Y = np.reshape( Y, (Y.shape[0],Y.shape[1],-1), order='F' )

                # use affine transformations as augmentation
                M = np.eye(3)
                # horizontal flips
                if args.hflips:
                    M_ = np.eye(3)
                    M_[1][1] = 1 if np.random.random()<0.5 else -1
                    M = np.matmul(M,M_)
                # vertical flips
                if args.vflips:
                    M_ = np.eye(3)
                    M_[0][0] = 1 if np.random.random()<0.5 else -1
                    M = np.matmul(M,M_)
                # rotations
                if np.abs( args.rotations ) > 1e-2:
                    rot_angle = np.pi/180.0 * np.random.randint(-np.abs(args.rotations),np.abs(args.rotations))
                    M_ = np.eye(3)
                    M_[0][0] = np.cos(rot_angle)
                    M_[0][1] = np.sin(rot_angle)
                    M_[1][0] = -np.sin(rot_angle)
                    M_[1][1] = np.cos(rot_angle)
                    M = np.matmul(M,M_)
                # shears
                if np.abs( args.shears ) > 1e-2:
                    rot_angle_x = np.pi/180.0 * np.random.randint(-np.abs(args.rotations),np.abs(args.rotations))
                    rot_angle_y = np.pi/180.0 * np.random.randint(-np.abs(args.rotations),np.abs(args.rotations))
                    M_ = np.eye(3)
                    M_[0][1] = np.tan(rot_angle_x)
                    M_[1][0] = np.tan(rot_angle_y)
                    M = np.matmul(M,M_)                    
                # scaling (also apply specified resizing [--imsize] here)
                if np.abs( args.scalings ) > 1e-4 or args.imsize is not None:
                    if args.imsize is not None:
                        init_factor_x = X.shape[0] / args.imsize[0]
                        init_factor_y = X.shape[1] / args.imsize[1]
                    else:
                        init_factor_x = 1
                        init_factor_y = 1
                    if np.abs( args.scalings ) > 1e-4:
                        random_factor_x = np.random.randint(-np.abs(args.scalings)*10000,np.abs(args.scalings)*10000)/10000
                        random_factor_y = np.random.randint(-np.abs(args.scalings)*10000,np.abs(args.scalings)*10000)/10000
                    else:
                        random_factor_x = 0
                        random_factor_y = 0
                    scale_factor_x = init_factor_x + random_factor_x
                    scale_factor_y = init_factor_y + random_factor_y
                    M_ = np.eye(3)
                    M_[0][0] = scale_factor_x
                    M_[1][1] = scale_factor_y
                    M = np.matmul(M,M_)
                # translations
                if np.abs( args.translations ) > 0:
                    translate_x = np.random.randint( -np.abs( args.translations ), np.abs( args.translations ) )
                    translate_y = np.random.randint( -np.abs( args.translations ), np.abs( args.translations ) )
                    M_ = np.eye(3)
                    M_[0][2] = translate_x
                    M_[1][2] = translate_y
                    M = np.matmul(M,M_)

                # now apply the transform
                X_ = np.zeros( (output_shape[0],output_shape[1],X.shape[2]), dtype=X.dtype )
                Y_ = np.zeros( (output_shape[0],output_shape[1],Y.shape[2]), dtype=Y.dtype )
                for k in range(X.shape[2]):
                    X_[:,:,k] = affine_transform( X[:,:,k], M, output_shape=output_shape, mode=args.augmode )
                for k in range(Y.shape[2]):
                    Y_[:,:,k] = affine_transform( Y[:,:,k], M, output_shape=output_shape, mode=args.augmode )
                X = X_
                Y = Y_

                # optionally add noise
                if np.abs( args.addnoise ) > 1e-10:
                    noise_mean = 0
                    noise_sigma = args.addnoise
                    noise = np.random.normal( noise_mean, noise_sigma, output_shape )
                    for k in range(X.shape[2]):
                        X[:,:,k] = X[:,:,k] + noise
                    for k in range(Y.shape[2]):
                        Y[:,:,k] = Y[:,:,k] + noise

                # flatten samples into 2d data
                X = np.reshape( X, (X.shape[0],-1), order='F' )
                Y = np.reshape( Y, (X.shape[0],-1), order='F' )

                # transform the images to 32-bit float
                X = np.array(X, dtype=np.float32)
                Y = np.array(Y, dtype=np.float32)                

                # create PIL images and write to disk
                Ximage = Image.fromarray(X,mode='F')
                Yimage = Image.fromarray(Y,mode='F')

                # # save as a npy to see the result
                # Ximage = copy.deepcopy(X)
                # Yimage = copy.deepcopy(Y)

                # determine full output image path
                if not do_testdata and not do_valdata:
                    curr_X_folder = X_folder
                    curr_Y_folder = Y_folder
                elif do_testdata and (100*i/num_files > (100-args.testfraction)):
                    curr_X_folder = os.path.join(X_folder,'test')
                    curr_Y_folder = os.path.join(Y_folder,'test')
                elif do_valdata and (100*i/num_files > (100-args.valfraction-args.testfraction)):
                    curr_X_folder = os.path.join(X_folder,'val')
                    curr_Y_folder = os.path.join(Y_folder,'val')
                else:
                    curr_X_folder = os.path.join(X_folder,'train')
                    curr_Y_folder = os.path.join(Y_folder,'train')

                Ximage_path = os.path.join(curr_X_folder,'X_{:05d}_{:08d}.tiff'.format(subject_count,j+1))
                Yimage_path = os.path.join(curr_Y_folder,'Y_{:05d}_{:08d}.tiff'.format(subject_count,j+1))
                if args.force:
                    # user specified force, now we will have to check if the file exists before writing to it                    
                    while os.path.exists(Ximage_path) or os.path.exists(Yimage_path):
                        force_count += 1 
                        Ximage_path = os.path.join(curr_X_folder,'X_{:05d}_{:08d}.tiff'.format(subject_count+force_count,j+1))
                        Yimage_path = os.path.join(curr_Y_folder,'Y_{:05d}_{:08d}.tiff'.format(subject_count+force_count,j+1))                          
                
                # write image file to disk 
                Ximage.save(Ximage_path)
                Yimage.save(Yimage_path)

                # # save as npy
                # np.save(Ximage_path, Ximage)
                # np.save(Yimage_path, Yimage)


    logger.info(tabs+'Completed!\n\n\n')


def get_slice_chunks( img, z_loc, num_slices ):
    """
    Function to sample one or more slices from the image data format used internall

    Parameters
        img: The 4D image format used internally for image data 
        z_loc: The slice location to sample
        num_slices: The number of slices to sample. This should be an odd number

    Returns
        A chunk of 1 or more slices from the passed input
    """
    if num_slices == 1:
        out = img[:,:,:,z_loc]
        out = np.expand_dims(out,3)
    else:
        out = img[:,:,:,(z_loc-num_slices//2-1):(z_loc+num_slices//2)]

    return out


def get_nii_data(fn, logger):
    """
    Function to load NifTI data from the passed filename and apply DeepRad normalization (from deeprad_normalize)

    Parameters
        fn: The input file name of the NifTI image (.nii or .nii.gz file)

    Returns
        The image pixel data with DeepRad normalization applied (as calculated using deeprad_normalize)
    """
    nii = nibabel.load(fn)

    # read image data from file
    data = nii.get_fdata().astype(np.float32)

    # read normalization
    json_file = fn + '.deeprad'

    if os.path.isfile(json_file):
        with open(json_file) as infile:  
            deepraddata = json.load(infile)

            # apply normalization 
            if deepraddata['normtype']=='custom' or deepraddata['normtype']=='globalzscore' or deepraddata['normtype']=='volumezscore':
                data = (data-deepraddata['norm1'])/deepraddata['norm2']
            elif deepraddata['normtype']=='global' or deepraddata['normtype']=='volume':
                data = (data-deepraddata['norm1'])/(deepraddata['norm2']-deepraddata['norm1'])
            else:
                raise ValueError('Internal error. Invalid normtype in .deeprad file')

    else:
        warn_msg = 'No normalization info found for {}, assuming data is pre-normalized. Otherwise run deeprad_normalize'.format(fn)
        logger.warning(warn_msg)
        warnings.warn(warn_msg)

    return data


if __name__ == "__main__":
    sys.exit(main())