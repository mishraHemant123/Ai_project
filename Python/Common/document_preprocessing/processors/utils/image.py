import subprocess
import os
import numpy as np
import cv2
import re
import traceback
from. import ocr as tess_utils
from. import image_utils as image_utils
from multiprocessing.dummy import Pool as ThreadP
from joblib import Parallel, delayed
import time
import glob
import pandas as pd
import logging
import sys
import pdf2image
logger = logging.getLogger()

def convert_image(infile, outfile, overwrite, dpi = 300):
    if os.path.exists(outfile) and not overwrite:
        return outfile
    cmd = "convert -density %d -units PixelsPerInch %s -background white %s" % (dpi, infile, outfile)
    try:
        subprocess.call(cmd, shell = True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        raise Exception ("Image Conversion Error, File: %s" % infile)
    return outfile


# def convert_page_to_image(page_id, infile, outfile, overwrite, resample=True, dpi =300):
#     num=int(page_id)
#     if os.path.exists(outfile) and not overwrite:
#         logger.info('convert_page_to_image' - 'File exists : {0}'.format(outfile))
#     return outfile
    
#     if resample:
#         cmd = "convert -density %d -units PixelsPerInch %s[%d] %s" % (dpi, infile, num-1, outfile)
#     else:
#         cmd = "convert -units PixelsPerInch %s [%d] %s" % (infile, num - 1, outfile)
#     try:
#         subprocess.call(cmd, shell = True, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
#     except subprocess.CalledProcessError:
#         raise Exception("Image Conversion Error, Page: %s" % page_id)
#     return outfile

#image.py
def convert_page_to_image(page_id, infile, outfile, overwrite, resample=True, dpi =300):
    num=int(page_id)
    if os. path.exists (outfile) and not overwrite:
    # 		logger.info
        print('convert_page_to_image',format(outfile))
    # PART 2: NOW GET PAGE TO IMAGE -------------------------------------
    page_image = pdf2image.convert_from_path(os.path.join('fileDir',infile)) # without 'size=...'
    #show first page with the right size (at least the one that pdfminer says)
    # firstpage_image.show()
    outfile_file=page_image[num-1]

    outfile_file.save(outfile)

    return outfile
#image.py
def ocr_convert_page_to_image(infile, outfile, overwrite, resample=True, dpi =300):
    print('ocr_convert_page_to_image',format(outfile),infile)

    image_list=[]
    if os. path.exists (outfile) and not overwrite:
    # 		logger.info
        print('ocr_convert_page_to_image1',format(outfile))
        print('page_image',format(page_image))

    print('ocr_convert_page_to_image0',format(outfile))
    # PART 2: NOW GET PAGE TO IMAGE -------------------------------------
    page_image = pdf2image.convert_from_path(os.path.join('fileDir',infile))
    print('ocr_convert_page_to_image2',format(outfile))# without 'size=...'
    #show first page with the right size (at least the one that pdfminer says)
    # firstpage_image.show()
    for index,img in enumerate (page_image):
        out_file=outfile.replace('.png','_'+str(index)+'.png')
        img.save(out_file)
        image_list.append(out_file)
        print('ocr_convert_page_to_image3',format(outfile))
    return image_list

# def convert_pdf_to_image(infile, outfile, overwrite):
# def tryint(s):
#     try:
#         return int(s)
#     except:
#         return s


# def alphanum_key (s):
#      """
#     1. Turn a string into a list of string and number chunks.
#     "Z23a" -> ["z", 23, "a"]
#     """
#     return [tryint(c) for c in re.split([0-9]+), s)]

# def sort_nicely(l):
#     """
#     10 Sort the given list in the way that humans expect.
#     """
#     l.sort(key=alphanum_key)
#     images_dir,_=os.path.split(outfile)
#     if os.path.exists(images_dir) and len(os.listdir(images_dir)) > 0 and not overwrite:
#         files = os.listdir(images_dir)
#         files = [os. path.join(images_dir, f) for f in files]
#         sort_nicely(files)
#         return files

#     cmd = "convert -scene 1 -density 300 -units PixelsPerInch %s %s" % (infile, outfile)

#     try:
#         subprocess.call(cmd, shell = True, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
#     except subprocess.CalledProcessError:
#         raise Exception ("PDF to PNG Conversion Error")
#     files = os.listdir(images_dir)
#     sort_nicely(files)
#     files = [os.path.join(images_dir, f) for f in files]
#     return files

# def convert_tiff_to_image (infile, outfile, overwrite, dpi=300):
# def tryint(s):
#     try:
#         return int(s)
#     except:
#         return s

# def alphanum_key (s):
#     """
#     Turn a string into a list of string and number chunks.
#     "223a" -> ["z", 23, "a"]
#     """
#     return [tryint(c) for c in re.split('([0-9]+), s)]

# def sort_nicely (l):
#     """
#     sort the given list in the way that humans expect.
#     """
#     l.sort(key=alphanum_key)
#     images_dir,_ = os.path.split(outfile)
#     if os. path. exists(images_dir) and len(os.listdir(images_dir)) > 0:
#         files = os.listdir(images_dir)
#         files = [os. path.join(images_dir, f) for f in files]
#         sort_nicely(files)
#         return files

#     cmd = "convert -density " + str(dpi)+ scene 1 -units PixelsPerInch % %$" % (infile, outfile)
#     try:
#         subprocess.call(cmd, shell = True, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
#     except subprocess. Called ProcessError:
#         raise Exception (PDF to PNG Conversion Error)
#     files = os.listdir(images_dir)
#     sort_nicely(files)
#     return files

                                            
                                            
                                            
# def crop_image (infile, box, overwrite, page_width,page_height, padding=0):
# 	pad = padding // 2
# 	new_box = list (box)
# 	new_box[0] = np.clip(box[0] - pad, 0, page_width)
# 	new_box[1] = np.clip(box[1] - pad, 0, page_height)
# 	new_box[2] = np.clip(box [2] - pad, 0, page_width)
# 	new_box[3] = np.clip(box [3] - pad, 0, page_height)
# 	offsets = [box[0] - new_box[0], box[1] - new_box[1],box [2] - new_box [2], box[3] -new_box [3]]
# 	bbox = [300 * float(b) / 72 for b in new_box]
# 	width = int(bbox[2] - bbox[0])
# 	height = int(bbox[3] - bbox[1])
# 	x0 = int(bbox[0])
# 	y0 = int(bbox[1])
# 	crop_params = str(width)+ 'x' + str(height) +  '+' + str(x0) + '+' + str(y0)
# 	img=cv2.imread(infile)
# 	crop_image=img[y0:y0+height,x:x0+width]
# 	outfile = infile[0:-4] + '-'
# 	outfile += crop_params + '.png'
# 	cv2.imwrite(outfile,crop_image)
# 	if os.path.exists(outfile) and not overwrite:
# 		return outfile, offsets
# 	cmd = 'convert -crop' + crop_params +' '+ infile  + ' '+ outfile
# 	try:
# 		subprocess.call(cmd, shell = True, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
# 	except subprocess.CalledProcessError:
# 		raise Exception ("Image Conversion Error during Cropping.")
# 	return outfile, offsets


#image.py
def crop_image (infile, box, overwrite, page_width,page_height, padding=0):
    pad = padding // 2
    new_box = list (box)
    new_box[0] = np.clip (box[0] - pad, 0, page_width)
    new_box[1] = np.clip (box[1] - pad, 0, page_height)
    new_box[2] = np.clip (box [2] - pad, 0, page_width)
    new_box[3] = np.clip (box [3] - pad, 0, page_height)
    offsets = [box[0] - new_box[0], box[1] - new_box[1],box [2] - new_box [2], box[3] -new_box [3]]
    bbox = [300 * float(b) / 72 for b in new_box]
    width = int(bbox[2] - bbox[0])
    height = int(bbox[3] - bbox[1])
    x0 = int(bbox[0])
    y0 = int(bbox[1])
    crop_params = str(width)+ 'x' + str(height) +  '+' + str(x0) + '+' + str(y0)
    img=cv2.imread(infile)

    crop_image=img[y0:y0+height,x0:x0+width]
    outfile = infile [0:-4] + '-'
    outfile += crop_params + '.png'
    cv2.imwrite(outfile,crop_image)
    print('box',box,'new_box',new_box,'offsets',offsets,'y,:y0+height,x0,x0+width,',y0,y0+height,x0,x0+width)   
    if os. path.exists(outfile) and not overwrite:
        return outfile, offsets
    cmd = 'convert -crop' + crop_params +' '+ infile  + ' '+ outfile
    try:
        subprocess.call(cmd, shell = True, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        raise Exception ("Image Conversion Error during Cropping.")
    return outfile, offsets
                                            
                                            
def rotate_image(image_file, rotation):
    cmd = "convert -density 300 -units PixelsPerInch -rotate %d %s %s" % (rotation, image_file, image_file)
    try:
        subprocess.call(cmd, shell = True, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        raise Exception("Image Conversion Error during Rotation.")
    return image_file


def get_page_content_angle(image):
    _, binary_img = CV2. threshold (image, 150, 255, CV2. THRESH_BINARY_INV)
    indices = np. where (binary_img > 0)
    coords = np.column_stack((indices[1], indices[0]))
    angle = cv2.minAreaRect(coords) [-1]
    orig_angle = angle
    if angle <-45:
        angle = -(90 + angle)
    return angle, orig_angle


def fix_page_orientation (image):
    h, w, c = (0, 0, 0)
    try:
        h, w, c = image.shape
    except:
        h, w = image.shape
    margin_w = int(w / 10)
    sub_img = image[margin_h: h - margin_h, margin_w : w - margin_w]
    rot_anglel, orig_anglel = get_page_content_angle (sub_img)
    img1= image.copy ()
    M = cv2.getRotationMatrix2D((w/2,h/2), rot_anglel, 1)
    image = CV2.warpaffine (image, M, (w,h), bordervalue=(255, 255, 255))
    if abs(rot_anglel)==abs(orig_anglel) or abs(orig_anglel)>89.7:
        return image
    else:
        MCV2.getRotationMatrix2D((w/2,h/2), Erot_anglel, 1)
        img1 = CV2.warpAffine (img1, M, (w,h), borderValue = (255, 255,255))
        return img1


def fix_rotation(image_file, tessdata):
    osd = tess_utils.OSD (image_file, tessdata)
    rotation = osd.perform_osd()
    if rotation != 0 :
        orientation = rotation
        image_file = rotate_image(image_file, orientation)
    return rotation



def fix_image_rotation(image_file, tessdata, ocr_language):
    try:
        rotation = fix_rotation(image_file, tessdata, ocr_language)
        return rotation
    except:
        return 0


# def fix_page_image (args):
#     image_file = args["image_file"]
#     tessdata = args["tessdata"]
#     image_directory = args["image_directory"]
#     rotation = fix_image_rotation (image_file, tessdata)
#     page_no = int(os.path.splitext(os.path.split(image_file) (-1]) [0].split("")[-1])
#     img = cv2.imread (image_file)
#     image_file_original = os.path.join(image_directory, "original_" + str(page_no) +".png")
#     cv2.imwrite(image_file_original, img)
#     img = image_utils.normalize_image(img.copy())
#     cv2.imwrite(image_file, img)
#     return page_no,rotation

# def convert_page_image (args) :
# page_no = str(args['page_no/l)
# source_file = args['source_file')
# image_directory = args['image directory']

# tessdata = args["tessdata"]
# dpi = str(args['dpi'])
# ocr_language = args['ocr_language']
# outfile = os.path.join(image_directory, 'page_' + page_no + '.png")
# try:
# convert_page_to_image(int(page_no), source_file, outfile, False, True,
# int(dpi)).
# except subprocess. CalledProcessError:
# if source_file.endswith(".tiff') :
# convert_tiff_to_image (infile = source_file, outfile = outfile, overwrite =
# True ,dpi = int(dpi))
# else:
# raise Exception("Image Conversion Error, Page: %s" % page_no)
# image_file = os. path.join(image_directory, 'page_' + page_no + ".png')
# rotation = fix_image_rotation(image_file, tessdata, ocr_language)
# page_no = int(os.path.splitext(os.path, split(image_file) [-1])[0].split("_")[-1])
# img = cv2.imread (image_file)
# image_file_original = os.path.join(image_directory, "original_" + str(page_no) +
# ".png")
# CV2.imwrite(image_file_original, img)
# img = image_utils. normalize_image (img.copy())
# CV2.imwrite(image_file, img)
# return page_no, rotation


# def convert_pdf_image(source_file, tessdata, num_pages, dpi, ocr_language):
# target_directory, = os. path.split(source_file)
# image_directory = os.path.join(target_directory, 'png')
# page_wise_rotation_info = os. path.join(target_directory,
# page_wise_rotation_info.csv')
# if not os. path.exists(image_directory):
# os.mkdir (image_directory)
# Ist_page_wise_rotation_info = []
# Ist_args = [{'page_no' : page_no, 'source_file' : source_file,
# "image_directory' : image_directory,
# "tessdata"
# : tessdata, "dpi": dpi, "ocr_language" : ocr_language}
# for page_no in list(range (1, num_pages+1))]
# Ist_page_wise_rotation_info.extend (Parallel (n_jobs = 8)
# (delayed (convert_page_image) (lst_args[idx]) for idx in range (num_pages)))
# df_page_wise_rotation_info = pd.DataFrame (lst_page_wise_rotation_info, columns
# = ["page_no", "rotation"])
# df_page_wise_rotation_info. to_csv (page_wise_rotation_info)
# .
# else:
# df_page_wise_rotation_info pd.read_csv (page_wise_rotation_info)
# return df_page_wise_rotation_info


# def get_image_using_page_no(page_id, source_file, prefix = "page_", file = False):
# ""get Page Image using Page Number and sourcefile
# Arguments:
# page_id : Page Number
# source_file : location of the source file
# Returns:
# img : Page Image as a numpy array
# path, _ = os. path.split(source_file)
# image_file = os. path.join(path, "images" , prefix + str(page_id) + ".png")
# img = cv2.imread (image_file, 1)
# if file :
# return image_file
# else:
# return img

def get_image_using_page_no(page_id, source_file, prefix = "page_", file = False):
    """get Page Image using Page Number and sourcefile
    Arguments:
    page_id : Page Number
    source_file : location of the source file
    Returns:
    img : page image as a numpy array
        """

    path, _ = os.path.split(source_file)
    image_file = os. path.join( "./tmp" , prefix + str(page_id) + ".png")
    img = cv2.imread (image_file, 1)
    if file :
        return image_file
    else:
        return img
                                        

# def resize_with_aspect(img, final_h, final_w, fill_color=255, pix_type=np.uint8):
# h, w, c = None, None, None
# if len (img.shape) > 2: # channel present
# h, W, c = img.shape
# else: # no channel
# h, w = img.shape
# C = 1
# img = img.reshape(h, w, c)
# THIS
# mmg I wropy wy
# new_img = np.zeros((final_h, final_w, c), dtype=pix_type)
# new_img[:, :, :] = fill_color
# new_w, new_h = final_w, final_h
# img_aspect = w / h
# resize = True
# if (new_ht img_aspect > new_w):
# new_W = final_w
# new_h = new_w / img_aspect
# elif (new_w_1 img_aspect > new_h):
# new_h = final_h
# new_w = new_h * img_aspect
# I
# new_w, new_h = int(new_w), int(new_h)
# if (new_w <= 0):
# new_w = 1
# if (new_h = 0):
# new.h = 1
# if resize:
# img = CV2.resize (img, (new_w, new_h), CV2.INTER_CUBIC)
# if len(img.shape) < 3:
# img = img.reshape (new_h, new_w, c)
# cx, cY = final_h / 2, final_w / 2
# row_start = cx - new_h / 2
# row_end = cx + new_h / 2
# col_start = cY - new_w / 2
# row_end = cx + new_h / 2
# col_start = cY - new_w / 2
# col_end = cY + new_W / 2
# if row_start - int (row_start) > 0.0:
# row_start = int(row_start) + 1
# else:
# row_start = int(row_start)
# if row_end - int (row_end) > 0.0:
# row_end = int(row_end) + 1
# else:
# row_end = int(row_end)
# if col_start - int(col_start) > 0.0:
# col_start = int(col_start) + 1
# else:
# col_start = int(col_start)
# if col_end int(col_end) > 0.0:
# col_end = int(col_end) + 1
# else:
# col_end = int(col_end)
# new_img[row_start:row_end, col_start:col_end, :] = img
# return new_img
