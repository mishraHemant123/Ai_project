import cv2
import numpy as np
from. import image as img_utils
import os
import logging
import sys
logger = logging.getLogger()


# def resize_with_aspect(img, final_size, fill_color = 255):
# h, w, C = None None, None
# if len(img.shape) > 2: # channel present
# h, w, Cimg.shape
# else: # no channel
# h, w = img.shape
# C = 1
# img = img.reshape (h, W, c)
# new_img = np.zeros((final_size, final_size, c))
# new_img[:,:,:] = fill_color
# new_w, new_h = final_size, final_size
# # print("h=" + str(h) + "=" + str (w))
# resize = False
# if h <= new_h and w <= new_w:
# new_h = h
# new_W = W
# else:
# img_aspect = w / h
# resize = True
# # print("image_aspect = " + str(img_aspect))
# if (new_ht img_aspect > new_w):
# new_w = final size
# new_h = new_w / img_aspect
# elif (new_w / img_aspect > new_h):
# new_h = final_size
# new_w = new_h * img_aspect
# # print(new_h, new_w)
# new_w, new_h = int(new_w), int(new_h)
# if (new_w <= 0):
# new_W = 1
# if (new_h <= 0):
# new_h = 1
# # print(img)
# if resize:
# img cv2.resize(img, (new_w, new_h), cv2.INTER_CUBIC)
# if len(img.shape) < 3:
# img = img.reshape(new_h, new_w, c)
# cx, cY = int(final_size / 2), int(final_size / 2)
# row_start = cX - int(new_h / 2)
# row_end = cx + int(new_h / 2)
# col_start = cY - int(new_w / 2)
# col_end = cY + int(new_w | 2)
# # print (row_start, row_end, col_start, col_end)
# h_diff = row_end - row_start
# w_diff = col_end - col_start
# if h_diff > new_h:
# row_start += abs (new_h h_diff)
# if h_diff < new_h:
# row_start -= abs (rew_h - h_diff)
# if w_diff > new_w:
# col_start += abs (new_w w_diff)
# if w_diff <new_w:
# col_start -= abs(new_w - W_diff)
# # print(newImg.shape, img, shape)
# # print (row_start, row end, col start, col end)
# new_img[row_start:row_end, col_start:col_end, :] = img
# return new_img



# def convert_pdf_to_image (pdf_file, dst_dir):
# pdf_file_name = os.path.basename (pdf_file).split(".")[0]
# images = img_utils.convert_pdf_to_image (infile=pdf_file,
# outfile=os.path.join(dst_dir, pdf_file_name + ".png"), overwrite=True)
# filtered_images = []
# for img_path in images:
# if not "Thumbs.db" in img_path:
# filtered_images.append(img_path)
# return filtered_images
# def get_page_content_angle(image):
# binary_img = CV2. threshold (image, 150, 255, CV2. THRESH_BINARY_INV)
# indices = np.where (binary_img > 0)
# coords = np.column_stack((indices[1], indices[0]))
# angle = CV2.minAreaRect(coords) (-1)
# orig-angle = angle
# if angle <-45:
# angle = -(90 + angle)
# print(angle)
# return angle, orig_angle

# def fix_page_orientation_v2 (image):
# h, w, c = (0, 0, 0)
# try:
# h, w, c = image.shape
# except:
# h, w = image.shape
# T
# margin_h = int(h / 8)
# margin_w = int(w / 10)
# sub_img = image[margin_h : h - margin_h, margin_w: w - margin_w]
# rot_anglel, orig_anglel = get_page_content_angle (sub_img)
# img1 = image.copy ()
# M = cv2.getRotationMatrix2D ((w/2, h/2), rot anglei, 1)
# image = CV2.warpaffine (image, M, (w,h), borderValue= (255, 255, 255))
# if abs (rot_angle1) == abs(orig_anglel) or abs (orig_anglel) > 89.7:
# return image
# else:
# M = cv2.getRotationMatrix2D ((w/12, h/2), -rot_angle1, 1)
# img1 = CV2.warpAffine (imgi, M, (w,h), borderValue = (255, 255, 255))
# return img1

# def normalize_image(src):
# """
# Normalize and Clean a given image
# Arguments:
# src : Given Image for cleaning
# Returns:
# bw: Cleaned Image
# """
# kernel = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]], dtype=np.float32)
# imgLaplacian = CV2.filter2D(src, CV2.CV_32F, kernel)
# sharp = np. float32 (src)
# imgResult = sharp - imgLaplacian
# imgresult = np.clip(imgresult, 0, 255)
# imgresult = img Result.astype ('uint8')
# imgLaplacian = np.clip (imgLaplacian, 0, 255)
# imgLaplacian = np.uint8 (imgLaplacian)
# bw = cv2.cvtColor (imgresult, CV2.COLOR_BGR2GRAY)
# bw = CV2. threshold (bw, 40, 255, CV2. THRESH_BINARY | CV2.THRESH_OTSU)
# return bw


