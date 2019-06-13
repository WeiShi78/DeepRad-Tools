import os
os.environ['TF_ENABLE_AUTO_MIXED_PRECISION'] = '1'

import deeprad_keras_tools

import tensorflow
from tensorflow.keras.callbacks import History, ModelCheckpoint, TensorBoard
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import losses
import numpy
import Unet

tensorflow.keras.backend.set_image_data_format('channels_last')

def smooth_L1_loss(y_true, y_pred):
    return tensorflow.losses.huber_loss(y_true, y_pred)

def execute():
    data_in_chan = 1
    data_out_chan = 1
    data_x = 256
    data_y = 256*data_in_chan    
    model_x = 256
    model_y = 256
    batch_size = 10
    num_epochs = 25

    X_folder = 'C:\\Users\\axm3\\Documents\\data\\deepMRAC\\data\\bravo-tiff\\X'
    Y_folder = 'C:\\Users\\axm3\\Documents\\data\\deepMRAC\\data\\bravo-tiff\\Y'

    X_progress_file = 'C:\\Users\\axm3\\Documents\\data\\deepMRAC\\data\\bravo-tiff\\X\\train\\X_00001_00000001.tiff'
    Y_progress_file = 'C:\\Users\\axm3\\Documents\\data\\deepMRAC\\data\\bravo-tiff\\Y\\train\\Y_00001_00000001.tiff'

    print('creating model')
    model = Unet.UNetContinuous([model_x,model_y,data_in_chan],out_ch=data_out_chan,start_ch=16,depth=4,inc_rate=2.,activation='relu',dropout=0.5,batchnorm=True,maxpool=True,upconv=True,residual=False)
    model = deeprad_keras_tools.wrap_model( model, (data_x,data_y,1), (data_x,data_y,1), (model_x,model_y,1), (model_x,model_y,1) )    
    model.compile(optimizer=Adam(lr=1e-3), loss=smooth_L1_loss, metrics=[smooth_L1_loss,losses.mean_squared_error,losses.mean_absolute_error])
    model.summary()

    print('creating data generators')
    train_gen = deeprad_keras_tools.get_keras_tiff_generator( os.path.join(X_folder,'train'), os.path.join(Y_folder,'train'), batch_size )
    val_gen = deeprad_keras_tools.get_keras_tiff_generator( os.path.join(X_folder,'val'), os.path.join(Y_folder,'val'), batch_size )

    print('creating callbacks')
    history = History()
    modelCheckpoint = ModelCheckpoint('weights.h5', monitor='loss', save_best_only=True)
    tblogdir = 'tblogs/{}'.format(time())
    tensorboard = TensorBoard(log_dir=tblogdir)
    X_progress = deeprad_keras_tools.read_images( [X_progress_file] )
    Y_progress = deeprad_keras_tools.read_images( [Y_progress_file] )
    tensorboardimage = deeprad_keras_tools.TensorBoardIm2ImCallback(log_dir=tblogdir,X=X_progress,Y=Y_progress)

    print('fitting model')
    model.fit_generator( train_gen,
                        validation_data=val_gen,
                        epochs=num_epochs,
                        use_multiprocessing=True,
                        max_queue_size=20,
                        workers=3,
                        callbacks=[history, modelCheckpoint, tensorboard, tensorboardimage] )

if __name__ == "__main__": 
    execute()



