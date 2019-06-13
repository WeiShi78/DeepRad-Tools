from glob import glob
from skimage.io import imread
import tensorflow
from tensorflow.keras.utils import Sequence
from tensorflow.keras.callbacks import Callback
from PIL import Image
import numpy as np
import io
import os

# deeprad_keras_tools
# Copyright 2019 by Alan McMillan, University of Wisconsin
# All rights reserved.
# This file is part of DeepRad and is released under the "MIT License Agreement".
# Please see the LICENSE file that should have been included as part of this package

def read_images(fn_list):
    """
    Function to read images from a list of filenames

    Parameters
        fn_list: A list of input filenames
    
    Returns
        A batch of images
    """
    batch = np.array( [ imread(fn) for fn in fn_list ] )
    batch = np.expand_dims(batch,3)
    return batch

def wrap_model( model, data_input_shape, data_output_shape, model_input_shape, model_output_shape ):
    """
    A function to wrap an existing Keras model with input and output images from DeepRad

    Parameters
        model: The Keras model
        data_input_shape: The shape of the input data (from DeepRad). This is always a length two tuple [e.g., (M,N*C)]
        data_output_shape: The shape of the ground truth and output data (from DeepRad). This is always a length two tuple [e.g., (M,N*C)]
        model_input_shape: The shape of the Keras model input data. This is always a length three tuple [e.g., (M,N,C)]
        model_output_shape: The shape of the Keras model ground truth and output data. This is always a length three tuple [e.g., (M,N,C)]

    Returns
        A wrapped model that has input and output shapes matching the DeepRad data
    """
    new_input = tensorflow.keras.layers.Input(shape=(data_input_shape[0],data_input_shape[1],1))
    new_input_wrapped = tensorflow.keras.layers.Reshape(target_shape=(model_input_shape[0],model_input_shape[2],model_input_shape[1]))(new_input)
    new_input_wrapped = tensorflow.keras.layers.Permute((1,3,2))(new_input_wrapped)

    new_model_input = model(new_input_wrapped)

    new_output = tensorflow.keras.layers.Permute((1,3,2))(new_model_input)
    new_output_wrapped = tensorflow.keras.layers.Reshape(target_shape=(model_output_shape[0],model_output_shape[1],1))(new_output)

    return tensorflow.keras.models.Model(new_input,new_output_wrapped)


def get_keras_tiff_generator( X_folder, Y_folder, batch_size ):
    """
    A function to return a SimpleKerasGenerator from .tif or .tiff images found within specified folders

    Parameters:
        X_folder: A folder that contains the input data .tif or .tiff images with filenames that match Y_folder when sorted
        Y_folder: A folder that contains the ground truth data .tif or .tiff images with filenames that match X_folder when sorted
        batch_size: The batch size of the generator

    Returns:
        A Keras Generator that returns samples of batch_size
    """
    X_files = sorted(glob(os.path.join(X_folder,'*.tif'),recursive=True)) + sorted(glob(os.path.join(X_folder,'*.tiff'),recursive=True))
    Y_files = sorted(glob(os.path.join(Y_folder,'*.tif'),recursive=True)) + sorted(glob(os.path.join(Y_folder,'*.tiff'),recursive=True))

    print('keras tiff generator found {} files for X and {} files for Y'.format(len(X_files),len(Y_files)))

    return SimpleKerasGenerator( X_files, Y_files, batch_size )


class SimpleKerasGenerator(Sequence):
    """Keras Generator Class that returns batches of images read from disk """

    def __init__(self, X_filenames, Y_filenames, batch_size):
        """
        The constructor for the SimpleKerasGenerator class

        Parameters:
            X_filenames: A list of input data filenames matching the order of  Y_filenames
            Y_filenames: A list of ground truth data filenames matching the order of X_filenames
            batch_size: The batch size of the generator
        """
        self.X_filenames, self.Y_filenames = X_filenames, Y_filenames
        self.batch_size = batch_size

    def __len__(self):
        return len(self.X_filenames) // self.batch_size

    def __getitem__(self, idx):
        batch_x_fns = self.X_filenames[idx * self.batch_size:(idx + 1) * self.batch_size]
        batch_y_fns = self.Y_filenames[idx * self.batch_size:(idx + 1) * self.batch_size]

        batch_x = np.array( [ imread(fn) for fn in batch_x_fns ] )
        batch_x = np.expand_dims(batch_x,3)
        batch_y = np.array( [ imread(fn) for fn in batch_y_fns ] )
        batch_y = np.expand_dims(batch_y,3)

        return batch_x,batch_y

class TensorBoardIm2ImCallback(Callback):
    """Keras callback for TensorBoard that writes image examples at the end of every epoch"""

    def __init__(self, log_dir, X, Y):
        """
        The constructor for the TensorBoardIm2ImCallback class
        
        Parameters:
            log_dir: The TensorBoard log directory (should be the same as your TensorBoard Callback log_dir).
            X: The test input image. Should be the same size as the input to your model with batch_size=1.
            Y: The test ground truth output image. Should be the same size as the input to your model with batch_size=1.
        """
        super(TensorBoardIm2ImCallback, self).__init__()
        self.X = X
        self.Y = Y
        self.writer = tensorflow.summary.FileWriter(log_dir)

    def make_image(self, img_data):
        """
        A function to turn an array into a TensorBoard Summary Image (tensorflow.Summary.Image)

        Parameters:
            img_data: The input image data. Should be sized M x N or sized M x N x C, where M is the height, N is the width, and C is the number of channels.
        """
        if len(img_data.shape) == 2:
            height, width = img_data.shape
            channels = 1
        else:
            height, width, channels = img_data.shape
        
        # scale to 8-bit
        img_data = np.interp( img_data, (np.min(img_data), np.max(img_data)), (0, 255) ).astype(np.uint8)
        image = Image.fromarray(img_data)
          
        output = io.BytesIO()
        image.save(output, format='PNG')
        image_string = output.getvalue()
        output.close()
        return tensorflow.Summary.Image(height=height, width=width, colorspace= channels, encoded_image_string=image_string)

    def on_epoch_end(self, epoch, logs=None):
        """
        Function run at the end of the epoch. It will write the test images to the TensorBoard log
        """
        logs = logs or {}
        summary_str = []
        
        Y_ = self.model.predict( self.X )
        
        summary_str.append(tensorflow.Summary.Value(tag='Y_', image=self.make_image( np.squeeze(Y_) )))
        if epoch < 1: # these images do not change, so let's only write them once
            summary_str.append(tensorflow.Summary.Value(tag='Y', image=self.make_image( np.squeeze(self.Y) )))
            summary_str.append(tensorflow.Summary.Value(tag='X', image=self.make_image( np.squeeze(self.X) )))
        
        self.writer.add_summary( tensorflow.Summary(value = summary_str), epoch )
