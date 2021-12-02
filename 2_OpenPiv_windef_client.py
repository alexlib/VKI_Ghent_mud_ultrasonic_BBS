# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 16:42:13 2019

@author: Theo
"""

# add two directories that include the new files
# note that we need to import openpiv in a separate, original namespace
# so we can use everything from openpiv as openpiv.filters and whatever is 
# going to replace it will be just filteers (for example)

#DEFINE 3 VARIABLES FOR CORRECT NAMING 
Density= "145"#116, 145 or 172
Freq = "45" #two digit number without decimal --> fc x 10 (e.g. 7.5MHz becomes 75)
FR = "90" # frame rate

from OpenPIV_windef_func import PIV_windef
#import time

class Settings(object):
    pass  
#start_time = time.time()
settings = Settings()


Base_folder="C:/Scans UZL/tests at home_rev2_(raw_imgs)/new_images_35_phased_array/"
'Data related settings'
# Folder with the images to process
#settings.filepath_images = './Pre_Pro_PIV_IMAGES2/'
settings.filepath_images = Base_folder+"/Img_pairs/"

# Folder for the outputs
settings.save_path = Base_folder+'./Results_PIV/'
# Root name of the output Folder for Result Files
settings.save_folder_suffix = ''
# Format and Image Sequence
settings.frame_pattern_a = 'A*a.tif'#looks at every file of which the filename starts with "A" and ends with "a" and a random number in between 
settings.frame_pattern_b = 'A*b.tif'    

'Region of interest'
# (50,300,50,300) #Region of interest: (xmin,xmax,ymin,ymax) or 'full' for full image
# seems like X = vertical and Y is horizontal
settings.ROI = 'full'
#settings.ROI=(5*16,15*16,10*16,30*16)#middle region
#settings.ROI=(0,500,0,1000)#upper region

'Image preprocessing'
# 'None' for no masking, 'edges' for edges masking, 'intensity' for intensity masking
# WARNING: This part is under development so better not to use MASKS
settings.dynamic_masking_method = 'None'
settings.dynamic_masking_threshold = 0.005
settings.dynamic_masking_filter_size = 7 

'Processing Parameters'
settings.correlation_method = 'linear'  # 'circular' or 'linear'
settings.iterations = 2  # select the number of PIV passes
# add the interroagtion window size for each pass. 
# For the moment, it should be a power of 2 
settings.windowsizes = (80, 40, 20) # if longer than n iteration the rest is ignored
#settings.windowsizes = (48,24,12)#smaller window sizes --> overlap also needs to change
# The overlap of the interroagtion window for each pass.
settings.overlap = (40, 20, 10) # This is 50% overlap
#settings.overlap = (24, 12, 6) # This is 50% overlap for the smaller window size
# Has to be a value with base two. In general window size/2 is a good choice.
# methode used for subpixel interpolation: 'gaussian','centroid','parabolic'
settings.subpixel_method = 'gaussian'
# order of the image interpolation for the window deformation
settings.interpolation_order = 3
settings.scaling_factor = 10  # scaling factor pixel/millimeter !!!!!!!!!!!!!!! see TSC course video 01:00:05
settings.dt = 1/496.27791563272973  # time between to frames (in seconds)!!!!!!!!!!!!!!!!!!!!!!!! see TSC course video 01:00:05
'Signal to noise ratio options (only for the last pass)'
# It is possible to decide if the S/N should be computed (for the last pass) or not
settings.extract_sig2noise = True  # 'True' or 'False' (only for the last pass)
# method used to calculate the signal to noise ratio 'peak2peak' or 'peak2mean'
# The higher the better (ratio = always > 1). Value of 1.5 is minimum. 
# Too high values (> 3 or 4) are suspicious. Bad image results in lot of zero values in txt file (see TSC video 01:02:50) 
# S2N is influenced by windowsize. (too) large windowsizes will result in high S2N, but it has no meaning anymore 
settings.sig2noise_method = 'peak2peak'
# select the width of the masked to masked out pixels next to the main peak
# Adjust to higher value in case of large particle size, otherwise it will consider same particle multiple times (TSC video 01:01:40) 
settings.sig2noise_mask = 5
# If extract_sig2noise==False the values in the signal to noise ratio
# output column are set to NaN
'vector validation options' # 4 options to knock out obviously wrong results (e.g. too high displacements and thus velocities)
# choose if you want to do validation of the first pass: True or False
settings.validation_first_pass = True
# only effecting the first pass of the interrogation the following passes
# in the multipass will be validated
'Validation Parameters'
# The validation is done at each iteration based on three filters.
# The first filter is based on the min/max ranges. Observe that these values are defined in
# terms of minimum and maximum displacement in pixel/frames.
Max_disp = 100# maximum displacement (in pixels!!!!)
# Good practice is a movement of 8 - 10 pixels between 2 frames
settings.MinMax_U_disp = (-Max_disp, Max_disp)
settings.MinMax_V_disp = (-Max_disp, Max_disp)
# The second filter is based on the global STD threshold
# factor is the maximum factor between registered value and standard deviation. If above the factor chosen, the value is masked 
settings.std_threshold = 4  # threshold of the std validation
# The third filter is the median test (not normalized at the moment)
settings.median_threshold = 4  # threshold of the median validation
# On the last iteration, an additional validation can be done based on the S/N.
settings.median_size = 1 #defines the size of the local median
'Validation based on the signal to noise ratio'
# Note: only available when extract_sig2noise==True and only for the last
# pass of the interrogation
# Enable the signal to noise ratio validation. Options: True or False
settings.do_sig2noise_validation = True # This is time consuming
# minmum signal to noise ratio that is need for a valid vector
settings.sig2noise_threshold = 1.25
'Outlier replacement or Smoothing options'
# Replacment options for vectors which are masked as invalid by the validation
settings.replace_vectors = False # Enable the replacment. Chosse: True or False
settings.smoothn=False #Enables smoothing of the displacemenet field
settings.smoothn_p=0.1 # This is a smoothing parameter
# select a method to replace the outliers: 'localmean', 'disk', 'distance'
settings.filter_method = 'localmean'
# maximum iterations performed to replace the outliers
settings.max_filter_iteration = 4
settings.filter_kernel_size = 2  # kernel size for the localmean method
'Output options'
# Select if you want to save the plotted vectorfield: True or False
settings.save_plot = True
# Choose wether you want to see the vectorfield or not :True or False
settings.show_plot = False
settings.scale_plot = 200 # select a value to scale the quiver plot of the vectorfield
# run the script with the given settings
settings.counter = 0

'''
i = 1
for i in range(1, 11):
    settings.frame_pattern_a = 'A%03da.tif' % i
    settings.frame_pattern_b = 'A%03db.tif' % i 
    settings.counter = i
    PIV_windef(settings)
'''

PIV_windef(settings)


# # Test for Manuel
# import numpy as np
# import matplotlib.pyplot as plt
# filename='Results_PIV\\Open_PIV_results_Test_RAW\\field_02.txt'
# a = np.loadtxt(filename)
# SN_Data=a[:,4]
# plt.hist(SN_Data,200)
# print('Mean SN_Ratio ' +str(np.mean(SN_Data)))
# plt.xlim([1,5])
# #end_time = time.time()
# #print('Calculationtime: %.3f' % (end_time-start_time))