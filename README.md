# DeepRad-Tools

Commandline tools to facilitate the use of Medical Images (from NifTI files) to standard image files (TIFF files) so that these datasets can be readily consumed by deep learning frameworks as used for computer vision.

It currently consists of two tools: [deeprad_nii2img](#deeprad_nii2img) and [deeprad_normalize](#deeprad_normalize)

# deeprad_nii2img

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
by writing into 2D images. Because reshaping is a common operation, it is straightforward
to reshape inputs and outputs to use TIFF images as an intermediate format.

Note that it is a pre-requisite to use DeepRad Normalize (deeprad_normalize) before using
this tool to calculate the proper scale factors for input and output data.

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

# deeprad_normalize

Calculates normalization information for folders full of NifTI images (.nii or .nii.gz files).
Specifically, this tool add normalization information as metadata to the NifTI header so that
other DeepRad tools can utilize these data as properly normalized inputs into deep learning
algorithms. Running this tool is likely a pre-requisite before running other DeepRad tools.
Note the NifTI file is modified as a result of this tool. However, the image pixel data are not
modified and only DeepRad-specific information is placed into the header. This should have no
effect on the use of the modified NifTI images in any other tool. 

Try running deeprad_normalize --help for specific help and command line options
