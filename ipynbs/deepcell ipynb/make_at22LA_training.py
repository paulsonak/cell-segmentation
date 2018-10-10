'''
Make 20170420-AT22LAclones training data
'''
from __future__ import print_function
from trainingData import *
import os
direc_name = '/home/amandap/data/deepCellData/training'
imgs_dir = os.path.join(direc_name, 'imgs')
masks_dir = os.path.join(direc_name, 'masks')
feature_names = ['seg']
channel_names = ['img']
window_x = 30
window_y = 30
max_direcs = 250
max_training_examples = 1*10**6
file_name_save = os.path.join(direc_name, 'imgs.npz')

print("Loading channel data...")
channels = load_channel_imgs(imgs_dir, channel_names, window_x, window_y, max_direcs)
print("Loading feature masks...")
feature_mask = load_feature_masks(masks_dir, feature_names, window_x, window_y, max_direcs, invert=False)

def feature_mask_clean(feature_mask):
    pos_planes = np.array([batch.sum() for batch in feature_mask[:,0,:,:]])
    idx = pos_planes > 0
    return feature_mask[idx,:,:,:].astype('bool'), idx

feature_mask, idx = feature_mask_clean(feature_mask)
channels = channels[idx,:,:,:]

print("Identifying training pixels...")
min_num = determine_min_examples(feature_mask, window_x, window_y)

feature_matrix = identify_training_pixels(feature_mask, min_num, window_x, window_y, max_training_examples)
print("Saving training data to :" + file_name_save)
save_training_data(file_name_save, channels, feature_matrix, window_x, window_y)
