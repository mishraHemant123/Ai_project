"""

PDF to JSON Conversion
This module accepts a PDF file(text, scanned, or a mix of both) and converts it to a
JSON file.The JSON file captures the words in the document along with their bounding boxes.
Returns:boolean Flag indicates if the file was successfully converted.

"""
import os
import time
import pickle
import json
import shutil
import xml.etree.ElementTree
from lxml import etree
import cv2
from pdfminer.pdfdocument import PDFTextExtractionNotAllowed
import processors.utils.ocr as tess_utils
import processors.utils.image as img_utils
import processors.utils.xml as xml_utils
import processors.utils.segmentation as seg_utils
# import processors.utils.headers_footers as hf_utils
# import processors.utils.toc as toc_utils
# import processors.utils.cover_page as cover_page_utils
# import processors.utils. Underline_strikeout_words as Underline_strikeout_utils
# from processors.utils.model import DocumentModel
import processors.utils.model as model

# from multiprocessing.dummy import Pool as ThreadPool
# from processors.utils.detection import obiect_detection
# import processors.utils.arrange_segments as arrange_segments
import numpy as np
import tempfile
from pikepdf import Pdf
# import helper_utils.file_handler as file_handler
import warnings
warnings.filterwarnings ("ignore")
import logging
import sys
from threading import Lock
logger = logging.getLogger()
lock = Lock
import pdf2image

auto_detect_table=0
images_dir="C:/Users/vikas.bhadouria/Documents/Gyani_AI/Gyani_Demo_VM_v1.1/Python/projects/Kapitus/tmp"
const_threshold_scanned_pdf= 1.5
const_threshold_text_based_pdf= 1.75
osd=False
auto_detect_table=0
overwrite=False
dpi =300
ocr_language="eng"
# !export TESSDATA_PREFIX=/home/admin1/Gyani_AI/gyani/tessdata
# tessdata='/home/admin1/Gyani_AI/gyani/tessdata'
# tessdata='C:/Users/vikas.bhadouria/AppData/Local/Programs/Tesseract-OCR/tessdata'
tessdata="C:/Users/vikas.bhadouria/Documents/Gyani_AI/Gyani_Demo_VM_v1.1/Python/Common/document_preprocessing/tessdata"
rotation=0
oem_mode="v4"
psm_mode=3
flag_merge_table_neighbours=True
flag_merge_consecutive_tables=True
flag_merge_para_neighbours=True
use_Tabula=False
debug_segmentation=False
extract_type = "internal"

class Processor (object):
	"""
	PDF Processor
	"""
def __init__(self, source_file, dst, tessdata, overwrite, cleanup,oem,psm, store_results, debug_segmentation, restore_results,
flag_merge_table_neighbours, flag_merge_consecutive_tables,auto_detect_table, use_Tabula, rcnn_model_check_point, flag_merge_para_neighbours,
tf_api_url, table_extract_mode, dpi, ocr_language, isPageImagesRequired):

	"""
	Initialization
	--
	Arguments:
	source_file {str} Path to the source file
	dst {str} Path to the destination directory
	tessdata {str} Path to tessdata model
	overwrite {bool} If True, overwrite existing json file
	cleanup {true} If True, remove unwanted files after completion
	oem (string) Tesseract OCR Engine Mode (OEM). Two options V4 (LSTM-
	based) or v3 (Legacy Tesseract)
	store_results {true} -- If True, store intermediate results. Useful for
	debugging and experimenting.
	"""

	_, filename = os.path.split(source_file)
	name, _ = os.path.splitext(filename)
	tmp_dir = os.path.join(dst, "tmp")
	os.makedirs(tmp_dir, exist_ok=True)
	images_dir = os.path.join(dst, "images")
	os.makedirs(images_dir, exist_ok=True)
	self.source_file = source_file
	self.filename = filename
	self.name = name
	self.output_dir = dst
	self.tmp_dir = tmp_dir
	self.images_dir = images_dir
	self.tessdata=tessdata
	self.cleanup = cleanup
	self.oem_mode = oem
	self.psm_mode = psm
	self.store_results = store_results
	self.restore_results = restore_results
	self.debug_segmentation = debug_segmentation
	self.images_to_keep = []
	self.flag_merge_table_neighbours = flag_merge_table_neighbours
	self.flag_merge_consecutive_tables = flag_merge_consecutive_tables
	self.auto_detect_table = auto_detect_table
	self.use_Tabula = use_Tabula
	self.rcnn_model_check_point = rcnn_model_check_point
	self.flag_merge_para_neighbours = flag_merge_para_neighbours
	self.table_extract_mode = table_extract_mode
	self.tf_api_url = tf_api_url
	self.dpi = dpi
	self.ocr_language = ocr_language
	self.isPageImagesRequired = isPageImagesRequired
	self.const_threshold_scanned_pdf = 1.5
	self.const_threshold_text_based_pdf = 1.75
	self.debug_dir_matrix = os.path.join(self.output_dir, "debug_matrix")
	os.makedirs(self.debug_dir_matrix, exist_ok=True)

# def create_page_image(self, page_id):
# 	"""
# 	Create Page images
# 	"""
# 	image_file = img_utils.convert_page_to_image(page_id, self.source_file,
# 	os.path.join(self.images_dir,"%s%s.png" % ('page_', page_id)),False, True,int(self.dpi))
# # def create_page_image(page_id):
# # 	"""
# # 	Create Page images
# # 	"""
# # 	image_file = img_utils.convert_page_to_image(page_id, source_file,
# # 	os.path.join(images_dir,"%s%s.png" % ('page_', page_id)),False, True,int(dpi))
def create_page_image(page_id):
	"""
	Create Page images
	"""
	image_file = img_utils.convert_page_to_image(page_id, source_file,
	os.path.join(images_dir,"%s%s.png" % ('page_', page_id)),False, True,int(dpi))

    
    
def clean_dirs(self):
	"""
	Clean up unwanted directories and files after completion.
	"""
	if not self.store_results:
		file_handler.remove_dir(self.tmp_dir)
	if os. path.exists(self.images_dir):
		images_list = [os.path.join(self.images_dir, x)
			for x in os.listdir(self.images_dir)]
		images_to_remove =[x for x in images_list if x not in self.images_to_keep]
		for image in images_to_remove:
			file_handler.remove_file(image)
	file_handler.remove_dir(self.debug_dir_matrix)
	file_handler.remove_dir(os.path.join(self.output_dir,"png_preprocessed"))
	file_handler.remove_dir(self.source_file)



def save_document(self, document):
    """
    "Serialize the final document to a JSON file
    Arguments:
    document {object)
    Document object
    """

    path = os.path.join(self.output_dir, self.name + ".json")
    with open(path, "w") as fi:
        json.dump(document, fi)

def save_intermediate_results(self, page_id, results):
    """
    Save intermediate results
    Arguments:
    page_id [str] Page number
    results {object} Intermediate results object
    """

    path = os.path.join(self. tmp_dir, "intermediate.pkl")
    if os. path.exists (path):
        data = pickle.load(open(path, "rb"))
    else:
        data = {}
    data[page_id] = results
    with open(path, "wb") as fi:
        pickle.dump(data,fi)
        
def load_intermediate_results(self, page_id):
     
    """
    "Load intermediate results for a specific page
    Arguments:
    page_id {str} -- Page number
    Returns:
    object
    Intermediate results object
    path = os.path.join(self.tmp_dir, "intermediate.pkl")
    if not os. path.exists (path):
            return None
    data = pickle.load(open(path, "rb"))
    try:
        results = data[page_id]
        return results
    except KeyError:
        return None

# def get_words_from_ocr(self, image_file, x_offset=0, y_offset=0, pad_offset=0,osd=True) : 
#     """
#         "Perform OCR on a given image
#         Arguments:
#         image_file {str} -- Path to the image file on which OCR needs to be applied
#         Keyword Arguments:
#         x_offset {int}
#         Required for cropped images to get the correct bounding box
#         y_offset {int}
#         Required for cropped images to get the correct bounding box
#         pad_offset {int} -- Padding offset
#         osd {bool} If True, perform orientation detection
#         Returns:
#         words [list] -- List of words along with their bounding boxes
#         orientation[float] -- Orientation of the image
#     """

#     orientation = None
#     if osd:
#         osd =tess_utils.OSD(image_file, self.tessdata, self.ocr_language)
#     rotation = osd.perform_osd()
#     if rotation != 0:
#         orientation = 360.-rotation
#         image_file = img_utils.rotate_image(image_file, rotation)
#     ocr = tess_utils.OCR(image_file, self.tessdata, self.oem_mode,self.ocr_language,self.psm_mode)
#     words = ocr.perform_ocr(x_offset=x_offset, y_offset=y_offset, pad_offset=pad_offset)
#     words = [[int(w[0]), int(w[i]), int(w[2]),int(w[3]), w[4], w[-1]] for w in words]
#     return words, orientation

                       

# From pdf.py
def get_words_from_ocr( image_file, x_offset=0, y_offset=0, pad_offset=0,osd=True) : 
    """
    "Perform OCR on a given image
    Arguments:
    image_file {str} -- Path to the image file on which OCR needs to be applied
    Keyword Arguments:
    x_offset {int}
    Required for cropped images to get the correct bounding
    box
    y_offset {int}
    Required for cropped images to get the correct bounding
    box
    pad_offset {int} -- Padding offset
    osd {bool} If True, perform orientation detection
    Returns:
    words [list] -- List of words along with their bounding boxes
    orientation[float] -- Orientation of the image
    """

    orientation = None
    if osd:
        osd =tess_utils.OSD(image_file,tessdata,ocr_language)
    rotation = osd.perform_osd()
    # 	if rotation != 0:
    # 		orientation = 360.-rotation
    # 		image_file = img_utils.rotate_image(image_file, rotation)
    ocr = tess_utils.OCR(image_file, tessdata, oem_mode,ocr_language,psm_mode)
    words = ocr.perform_ocr(x_offset=x_offset, y_offset=y_offset, pad_offset=pad_offset)

    words = [[float(w[0]), float(w[1]), float(w[2]),float(w[3]), w[4], w[-1]] for w in words]
    return words, orientation
                       
                       
                       
# def get_words_from_image(self, image_blocks, width, height, page_id):
# 	"""
# 	Process image blocks found in the page
# 	1. Convert the page to image
# 	2. Identify if the page is an image
# 	3. (Optional) Crop the image
# 	4. Perform OCR
# 	Arguments:
# 	image_blocks {list}
# 	-- List of bounding box information for each image
# 	block
# 	width (int)
# 	height {int}
# 	page_id [str]
# 	Width of the page
# 	Height of the page
# 	Page number
# 	Returns:

# 	regions [list] -- List of bounding box information for each image region
# 	regions_words[list] -- List of words along with bounding boxes for each
# 	mage region
# 	raw_images [list] List of file paths for each image
# 	is_page_image[bool] -- If True, the entire page is detected as an image
# 	padding[float] Padding amount applied to the image
# 	orientation[float] Orientation of the image as detected by OSD

# """
# -
# 	regions =[]
# 	regions_words =[]

# 	raw_images = []
# 	is_page_image = False
# 	padding = 10
# 	orientation = 0.
# 	image_file = None
# 	image_file = img_utils.convert_page_to_image(page_id, self.source_file,os.path.join(self.images_dir,"%s%s.png" % ('page_', page_id)),
# 	self.overwrite, True, int(self.dpi))
# 	if not image_blocks:
# 		return regions, regions_words, raw_images, is_page_image, padding,orientation

# 	for box in image_blocks:
# 		if int(box[2] - box[0])-int(width) < 25 and int(box[3]- box[1])= =int(height):
# 			is_page_image = True
# 			words, orientation = self.get_words_from_ocr(image_file,pad_offset=None)
# 			regions_words.append(words)
# 			regions.append(box)
# 			raw_images.append(image_file)
# 			break
# 		else:
# 			cropped_file, pad_offset = img_utils.crop_image(image_file, box,self.overwrite, width, height, padding=padding)
# 			words, _ = self.get_words_from_oor(cropped_file, x_offset=box[0],y_offset=box[1], pad_offset=pad_offset) #osd=False
# 			regions_words.append(words)
# 			regions.append (box)
# 			raw_images.append(cropped_file)
# 	self.images_to_keep.extend(raw_images)
# 	return regions, regions_words, raw_images, is_page_image, padding, orientation
	
                       
                       
 #From pdf.py
def get_words_from_image( image_blocks, width, height, page_id,source_file):
    """
    Process image blocks found in the page
    1. Convert the page to image
    2. Identify if the page is an image
    3. (Optional) Crop the image
    4. Perform OCR
    Arguments:
    image_blocks {list}
    -- List of bounding box information for each image
    block
    width (int)
    height {int}
    page_id [str]
    Width of the page
    Height of the page
    Page number
    Returns:

    regions [list] -- List of bounding box information for each image region
    regions_words[list] -- List of words along with bounding boxes for each
    mage region
    raw_images [list] List of file paths for each image
    is_page_image[bool] -- If True, the entire page is detected as an image
    padding[float] Padding amount applied to the image
    orientation[float] Orientation of the image as detected by OSD

    """

    regions =[]
    regions_words =[]
    images_to_keep=[]
    raw_images = []
    is_page_image = False
    padding = 0
    orientation = 0.
    image_file = None
    image_file = img_utils.convert_page_to_image(page_id, source_file,os.path.join(images_dir,"%s%s.png" % ('page_', page_id)),overwrite,True,int(dpi))
    if not image_blocks:

        return regions, regions_words, raw_images, is_page_image, padding,orientation

    for box in image_blocks:

        if int(box[2] - box[0])-int(width)<25 and int(box[3]- box[1])==int(height):


            is_page_image = True
            words, orientation = get_words_from_ocr(image_file,pad_offset=None)
            regions_words.append(words)
            regions.append(box)
            raw_images.append(image_file)
            break
        else:

            cropped_file, pad_offset = crop_image(image_file, box,overwrite, width, height, padding=padding)
            words,_ = get_words_from_ocr(image_file=cropped_file, x_offset=box[0],y_offset=box[1], pad_offset=pad_offset) #osd=False
            regions_words.append(words)
            regions.append (box)
            raw_images.append(cropped_file)
    # 			print('regions_words_=',regions_words,'regions_=',regions)
    images_to_keep.extend(raw_images)
    return regions, regions_words, raw_images, is_page_image, padding, orientation

                       
# def make_segments(self, words, image_regions, image_words, image_paths, page_id, width, height, is_page_image, orientation) :

# 	"""
# 	[summary]

# 	Arguments:
# 	words {[type]} -- [description]
# 	image_regions {[type]} [description]
# 	image_words {[type]} [description]
# 	page_id {[type]} [description]
# 	width {[type]} -- [description]
# 	height {[type]} -- [description]
# 	I
# 	Returns:
# 	[]
# 	type]--[description]
# 	"""
# 	if orientation == 90 or orientation==270
# 		temp = width
# 		width = int(height)
# 		height = int(temp)
# 	blocks = []
# 	for region, region_words, image_path in zip(image regions, image_words,image_paths):
# 		if region_words:
# 			words.extend(region_words)
# 		else:
# 		block=list(region)
# 		block.extend(["image", None, image_path])
# 		block.(region)
# 	words = sorted (words, key=lambda x: (x[1], x[0]))
# 	new_words = []
# 	for word in words:
# 		if (word[2] - word[0] == int(width)) and (word[3] - word[1]==int(height)):
# 			continue
# 		new_words.append(word)
# 	words = new_words
# 	_, page_matrix, median_height = seg_utils.make_image_from_words(words, width,height)
# 	cv2.imwrite(os.path.join(self.debug_dir_matrix, "page_%s.png" % (page_id)),page_matrix)
# 	tabl_segments = None
# 	if self.auto_detect_table !=0:
# 		tabl_segments, page_image = self.obj_table_detection.run(page_id, width,height, is_page_image, page_matrix, self.overwrite)
# 	tb_cuts = seg_utils.cut_segment(page_matrix)
# 	lr_cuts = []
# 	for t_b in tb_cuts:
# 		segment_image = page_matrix[t_b[0] :t_b[1], :).T
# 		1_r = seg_utils.cut_segment(segment_image)
# 		lr_cuts.append(l_r)
# 	if is_page_image:
# 		t_b_threshold = self.const_threshold_scanned_pdf
# 	else:
# 		t_b_threshold = self.const_threshold_text_based_pdf
# 	segments = seg_utils. label_segments (tb_cuts, lr_cuts, page_matrix, words)
# 	if self. flag_merge_table_neighbours:
# 		segments = seg_utils.merge_table_neighbors(segments, page_matrix, words,median_height, t_b_threshold)

# 	if self.flag_merge_para_neighbours:
# 		segments = seg_utils.merge_paragraph_neighbors(segments, page_matrix, words, median_height, t_b_threshold)

# 	if self.flag_merge_consecutive_tables:
# 		segments = seg_utils.merge_consecutive_tables(segments, tb_cuts, lr_cuts,page_matrix)
# 	logger.debug ("Running for Page number : %s", str(page_id))
# 	rule_tabl_segments = [segment for segment in segments if segment[2] == 'TABLE']

#     if rule_tabl_segments is not None : 
#         logger.debug("Table Section Detected from rule based system: {}", format(''.join(map(str, rule_tabl_segments))))
#         para_segments =[segment for segment in segments if segment[2] == 'PARA' ]
#         if para_segments is not None : 
#             logger.debug("Para Section Detected from Rule based system:{}"format(''.join(map (str, para segments))))

# 	if self.auto_detect_table==1:
# 		if tabl_segments is not None : 
#             logger.debug("Table Section Detected from RCNN Model : {}".format(''.join(map (str, tabl_segments))))
#             segments = arrange_segments.process(tabl_segments, rule_tabl_segments, para_segments)
# 		if segments is not None :
#             logger.debug("Final segment is : {}". format(''.join(map(str, segments))))

# 	elif self.auto_detect_table == 2:
# 		para_segments = [[segment[@], segment[1], 'PARA'] for segment in segments]

# 		if tabl_segments is not None : logger.debug("Table Section Detected from library : {}".Format(" '.join(map(str, tabl_segments))))
# 			segments = arrange_segments.process(tabl_segments, [], para_segments)
# 	if segments is not None : logger.debug("Final segment is : {}" format(''.join(map(str, segments))))
# 		blocks.extend(seg_utils.make_blocks(segments, page_matrix,words, self.source_file,page_id, self.use_Tabula, is_page_image, width, height,self.table_extract_mode))

# 	if self.debug_segmentation:
# 		if self.auto_detect_table ==0:
# 			outfile = os.path.join(self.images_dir, 'page_ + page_id + '.png')
# 			img_utils.convert_page_to_image(int(page_id), self.source_file, outfile, False, True, int(self.dpi))

# 			outfile, False, True, int(self.dpi))
# page_image = img_utils.get_image_using_page_no (page_id,self.source_file)
# self.debug_dir = os.path.join(self.output_dir, "debug")
# os.makedirs(self.debug_dir, exist_ok=True)
# outfile = os.path.join(self.debug_dir, "%s-%s.png" % (self.name, page_id))
# debug_image = cv2.resize(page_image, (int(width), int(height)))
# for block in blocks:
#     x_0, y_0, x_1, y_1, label,block
#     if label == "PARA":
#         color = (0, 255, 0)
#     elif label == "TABLE":
#         color = (0, 0, 255)
#     else:
#         color = (255, 0, 0)
#         cv2.rectangle(debug_image, (int(x_0),int(y_0)),(int(x_1), int(y_1)), color, 1)
#         cv2.imwrite(outfile, debug_image)
#     return blocks



    
    
# def make_segments( words, image_regions, image_words, image_paths, page_id, width, height, is_page_image, orientation,source_file) :

#     """
#     [summary]

#     Arguments:
#     words {[type]} -- [description]
#     image_regions {[type]} [description]
#     image_words {[type]} [description]
#     page_id {[type]} [description]
#     width {[type]} -- [description]
#     height {[type]} -- [description]
#     I
#     Returns:
#     []
#     type]--[description]
#     """
#     if orientation == 90 or orientation==270:
#         temp = width
#         width = int(height)
#         height = int(temp)
#     blocks = []

#     for region, region_words, image_path in zip(image_regions, image_words,image_paths):
#         if region_words:
#             words.extend(region_words)

#         else:
#             block=list(region)
#             block.extend(["image", None, image_path])
#     # 			block.append(region)
#     words = sorted (words, key=lambda x: (x[1], x[0]))

#     new_words = []
#     for word in words:
#         if (word[2] - word[0] == int(width)) and (word[3] - word[1]==int(height)):
#             continue
#         new_words.append(word)
#     words = new_words
#     # 	print('new_words_app',words)

#     _, page_matrix, median_height = seg_utils.make_image_from_words(words, width,height)


#     # 	plt.imshow(page_matrix)
#     # 	plt.show()
#     # 	debug_dir = os.path.join(output_dir, "debug")

#     tabl_segments = None
#     # 	segments=None
#     is_page_image=False
#     auto_detect_table==0  
#     if auto_detect_table==1:
#         tabl_segments, page_image = obj_table_detection.run(page_id, width,height, is_page_image, page_matrix, overwrite)
#     tb_cuts =seg_utils.cut_segment(page_matrix)
#     lr_cuts = []
#     for t_b in tb_cuts:
#         segment_image = (page_matrix[t_b[0] :t_b[1],:]).T
#         l_r = seg_utils.cut_segment(segment_image)
#         lr_cuts.append(l_r)
#     if is_page_image:
#         t_b_threshold = const_threshold_scanned_pdf
#     else:
#         t_b_threshold = const_threshold_text_based_pdf

#     segments = seg_utils.label_segments (tb_cuts, lr_cuts, page_matrix, words)

#     print('sorted_wrods_segments',segments)

#     if flag_merge_table_neighbours:
#         print("segsss",segments)
#         segments = seg_utils.merge_table_neighbors(segments, page_matrix, words,median_height, t_b_threshold)

#     if flag_merge_para_neighbours:
#         segments = seg_utils.merge_paragraph_neighbors(segments, page_matrix, words, median_height, t_b_threshold)

#     if flag_merge_consecutive_tables:
#         segments = seg_utils.merge_consecutive_tables(segments, tb_cuts, lr_cuts,page_matrix)
#     # 		logger.debug ("running for Page number : %s", str(page_id))
#     rule_tabl_segments = [segment for segment in segments if segment[2] == 'TABLE']

#     if rule_tabl_segments is not None : 
#         print("Table Section Detected from rule based system: {}".format(''.join(map(str, rule_tabl_segments))))
#     # 		logger.debug("Table Section Detected from rule based system: {}".format(''.join(map(str, rule_tabl_segments))))

#     para_segments =[segment for segment in segments if segment[2] == 'PARA' ]


#     if para_segments is not None : 


#         if tabl_segments is not None : 
#     # 			logger.debug("Table Section Detected from library : {}".Format(''.join(map(str, tabl_segments))))
#             segments = arrange_segments.process(tabl_segments, [], para_segments)
#         if segments is not None : 
#     # 			print('para_segments_segements_bloc',segments)
#     # 			print('para_segments_words',words)
#             blocks.extend(seg_utils.make_blocks(segments, page_matrix,words, source_file,page_id, use_Tabula, is_page_image, width, height))

#     # 			print('segments_blocks',blocks)            
#     outfile = os.path.join(images_dir, 'page_' + page_id + '.png')
#     img_utils.convert_page_to_image(int(page_id), source_file, outfile, False, True, int(dpi))

#     page_image = img_utils.get_image_using_page_no(page_id,source_file)
#     debug_dir = os.path.join("Output", "debug")
#     os.makedirs(debug_dir, exist_ok=True)
#     outfile = os.path.join(debug_dir,"%s_%s.png" %(source_file[:-4],page_id))

#     debug_image = cv2.resize(page_image, (int(width), int(height)))
#     for block in blocks:
#         x_0, y_0, x_1, y_1, label,_,_=block
#         if label == "PARA":
#             color = (0, 255, 0)
#         elif label == "TABLE":
#             color = (0, 0, 255)
#         else:
#             color = (255, 0, 0)
#         cv2.rectangle(debug_image, (int(x_0),int(y_0)),(int(x_1), int(y_1)), color, 1)
#         cv2.imwrite(outfile, debug_image)
#     # 	print('blocks', blocks)
#     return blocks

def make_segments( words, image_regions, image_words, image_paths, page_id, width, height, is_page_image, orientation,source_file) :

	"""
	[summary]

	Arguments:
	words {[type]} -- [description]
	image_regions {[type]} [description]
	image_words {[type]} [description]
	page_id {[type]} [description]
	width {[type]} -- [description]
	height {[type]} -- [description]
	I
	Returns:
	[]
	type]--[description]
	"""
	if orientation == 90 or orientation==270:
		temp = width
		width = int(height)
		height = int(temp)
	blocks = []

	for region, region_words, image_path in zip(image_regions, image_words,image_paths):
		if region_words:
			words.extend(region_words)

		else:
			block=list(region)
			block.extend(["image", None, image_path])
# 			block.append(region)
	words = sorted (words, key=lambda x: (x[1], x[0]))

	new_words = []
	for word in words:
		if (word[2] - word[0] == int(width)) and (word[3] - word[1]==int(height)):
			continue
		new_words.append(word)
	words = new_words
# 	print('new_words_app',words)

	_, page_matrix, median_height = seg_utils.make_image_from_words(words, width,height)


# 	plt.imshow(page_matrix)
# 	plt.show()
	debug_dir = os.path.join(images_dir, "debug")

	tabl_segments = None
# 	segments=None
	is_page_image=False
	auto_detect_table==0  
	if auto_detect_table==1:
		tabl_segments, page_image = obj_table_detection.run(page_id, width,height, is_page_image, page_matrix, overwrite)
	tb_cuts = seg_utils.cut_segment(page_matrix)
	lr_cuts = []
	for t_b in tb_cuts:
		segment_image = (page_matrix[t_b[0] :t_b[1],:]).T
		l_r =seg_utils.cut_segment(segment_image)
		lr_cuts.append(l_r)
	if is_page_image:
		t_b_threshold = const_threshold_scanned_pdf
	else:
		t_b_threshold = const_threshold_text_based_pdf

	segments = seg_utils.label_segments (tb_cuts, lr_cuts, page_matrix, words)

	print('sorted_wrods_segments',segments)

	if flag_merge_table_neighbours:
		print("segsss",segments)
		segments = seg_utils.merge_table_neighbors(segments, page_matrix, words,median_height, t_b_threshold)
		print("merge_table_neighbors_seg",segments)
	if flag_merge_para_neighbours:
		segments = seg_utils.merge_paragraph_neighbors(segments, page_matrix, words, median_height, t_b_threshold)
		print("merge_paragraph_neighbors_seg",segments)
	if flag_merge_consecutive_tables:
		segments = seg_utils.merge_consecutive_tables(segments, tb_cuts, lr_cuts,page_matrix)
		print("merge_consecutive_tables_seg",segments)

# 		logger.debug ("running for Page number : %s", str(page_id))
	rule_tabl_segments = [segment for segment in segments if segment[2] == 'TABLE']

	if rule_tabl_segments is not None : 
		print("Table Section Detected from rule based system: {}".format(''.join(map(str, rule_tabl_segments))))
# 		logger.debug("Table Section Detected from rule based system: {}".format(''.join(map(str, rule_tabl_segments))))

	para_segments =[segment for segment in segments if segment[2] == 'PARA' ]


	if para_segments is not None : 


		if tabl_segments is not None : 
# 			logger.debug("Table Section Detected from library : {}".Format(''.join(map(str, tabl_segments))))
			segments = arrange_segments.process(tabl_segments, [], para_segments)
		if segments is not None : 
# 			print('para_segments_segements_bloc',segments)
# 			print('para_segments_words',words)
			blocks.extend(seg_utils.make_blocks(segments, page_matrix,words, source_file,page_id, use_Tabula, is_page_image, width, height))

			print('make_blocks_',blocks)            
	outfile = os.path.join(images_dir, 'page_' + page_id + '.png')
	img_utils.convert_page_to_image(int(page_id), source_file, outfile, False, True, int(dpi))

	page_image = img_utils.get_image_using_page_no(page_id,source_file)
	debug_dir = os.path.join("./Output","debug")
	os.makedirs(debug_dir, exist_ok=True)
	outfile = os.path.join(debug_dir,"%s_%s.png" %(source_file[:-4],page_id))
	print("\n outfile",outfile,"\n images_dir" ,images_dir,"\n debug_dir",debug_dir,"\n page_image",page_image)
	debug_image = cv2.resize(page_image, (int(width), int(height)))
	for block in blocks:
		x_0, y_0, x_1, y_1, label,_,_=block
		if label == "PARA":
			color = (0, 255, 0)
		elif label == "TABLE":
			color = (0, 0, 255)
		else:
			color = (255, 0, 0)
		cv2.rectangle(debug_image, (int(x_0),int(y_0)),(int(x_1), int(y_1)), color, 1)
		cv2.imwrite(outfile, debug_image)
# 	print('blocks', blocks)
	return blocks

# def make_page(self, args) :
#     """
#     [summary]
#     Keyword Arguments:
#     root {[type]} -- [description] (default: {None})
#     image_file {[type]} -- [description] (default: {None})
#     page_id {[type]} [description] (default: {None})
#     width {[type]} -- [description] (default: {None})
#     height {[type]} [description] (default: {None})
#     Returns:
#     [type]
#     [description]
#     """
#     text_words =[]
#     text_figure_words = []
#     image_words = []
#     image_regions = []
#     raw_images = []

#     root = args["root"]
#     width = args["width"]
#     height = args["height"]
#     page_id = args["page_id"]
#     image_file = args["image_file"]
#     orientation = args["orientation"]
#     if not self.restore_results:
#         if root is not None:
#         selector = "./page[@id='%s']" % page_id
#         tree = root.find(selector)
#         text_words = xml_utils.scan_texts(tree, width, height)
#         text_figure_words = xml_utils.scan figures (tree, width, height)
#         image_blocks = xml_utils.scan images (tree, width, height)
#         image_regions, image_words, raw_images, is_page_image, padding,
#         orientation = self.get_words_from_image (
#         image_blocks, width, height, page_id)
#         if (image_file) or (not text_words and not text_figure_words and not
#         image_regions):
#         is_page_image = True
#         padding = 0
#         image_file = img_utils.convert_page_to_image (page_id,
#         self.source_file,
#         os.path.join(
#         self.images_dir, "%
#         s.png" % (self.name, page_id)),
#         self.overwrite)
#         ocr_words, orientation = self.get_words_from_ocr
#         image_file, pad_offset=None
#         image_words.append(ocr_words)
#         image_regions.append([0, 0, width, height])
#         raw_images.append(image_file)
#         self.images_to_keep.extend (raw_images)

#         intermediate_data = {
#         "text_words": text_words,
#         "text_figure_words": text_figure_words,
#         "image_regions": image_regions,
#         "image_words": image_words,
#         "raw_images": raw_images,
#         "is_page_image": is_page_image,
#         "padding": padding,
#         "orientation": orientation,
#         "images_to_keep": self.images_to_keep
#         }

#         if self.store_results:
#             self.save_intermediate_results(page_id, intermediate_data)
#         else:
#             intermediate_data = self.load_intermediate_results(page_id)
#             text_words = intermediate_data["text_words"]
#             text_figure_words = intermediate_data["text_figure_words"]
#             image_regions = intermediate_data["image_regions"]
#             image_words = intermediate_data["image_words"]
#             raw_images = intermediate_data["raw_images"]
#             is_page_image = intermediate_data["is_page_image"]
#             padding = intermediate_data["padding"]
#             orientation = intermediate_data["orientation"]
#             self.images_to_keep = intermediate_data["images_to_keep"]

#             if is_page_image:
#                 words = list(image_words[0])
#                 image_regions = []
#                 image_words = []
#             else:
#             words = text_words + text_figure_words
#             segments = self.make_segments (
#             words, image _regions, image_words, raw_images, page_id, width, height, is_page_image, orientation)
#             page = {"page_number": int(page_id), "width": width, "height": height,"is_page_image": is_page_image, "orientation":orientation, "segment":[]}
#             for segment in segments:
#                 x_0, y_0, x_1, y_l, label, headers, data = segment
#                 page_segment = {"bbox": [int(x_0), int(y_0), int(x_1), int(y_1)], "label": label, "content": data, "headers":headers}
#                 page["segments"].append(page_segment)
#                 if self.isPageImagesRequired:
#                     self.create_page_image(page_id)
#     return page



def make_page(args,source_file) :
    """
    [summary]
    Keyword Arguments:
    root {[type]} -- [description] (default: {None})
    image_file {[type]} -- [description] (default: {None})
    page_id {[type]} [description] (default: {None})
    width {[type]} -- [description] (default: {None})
    height {[type]} [description] (default: {None})
    Returns:
    [type]
    [description]
    """
    text_words =[]
    text_figure_words = []
    image_words = []
    image_regions = []
    raw_images = []
    root = args["root"]
    width = args["width"]
    height = args["height"]
    page_id = args["page_id"]
    image_file = args["image_file"]
    orientation = args["orientation"]
    is_page_images_required=False
    restore_results=False
    store_results=True
    images_to_keep=[]
    if not restore_results:
        if root is not None:
            selector = "./page[@id='%s']" % page_id
            tree = root.find(selector)
            text_words = xml_utils.scan_texts(tree, width, height)
            
            text_figure_words = xml_utils.scan_figures(tree, width, height)
            print('tree',tree)
            image_blocks = xml_utils.scan_images(tree, width, height)
            image_regions, image_words, raw_images, is_page_image, padding,orientation = get_words_from_image (image_blocks, width, height, page_id)
        if (image_file) or (not text_words and not text_figure_words and not image_regions):
            is_page_image = True
            padding = 0
            image_file = img_utils.convert_page_to_image (page_id, source_file,os.path.join(images_dir,(source_file[:-4]+str(page_id)+'.png')),overwrite)
            ocr_words, orientation = get_words_from_ocr(image_file, pad_offset=None)
            image_words.append(ocr_words)
            image_regions.append([0, 0, width, height])
            raw_images.append(image_file)
            images_to_keep.extend(raw_images)
            print("image_words_",image_words,"image_regions_",image_regions)

        intermediate_data = {
        "text_words": text_words,
        "text_figure_words": text_figure_words,
        "image_regions": image_regions,
        "image_words": image_words,
        "raw_images": raw_images,
        "is_page_image": is_page_image,
        "padding": padding,
        "orientation": orientation,
        "images_to_keep": images_to_keep
}


        if is_page_image:
            words = list(image_words[0])
            image_regions = []
            image_words = []
        else:
            words = text_words + text_figure_words
#             print('words__',words)
        segments = make_segments (
        words, image_regions, image_words, raw_images, page_id, width, height, is_page_image, orientation,source_file)
        print('segments__',segments)
    
        page = {"page_number": int(page_id), "width": width, "height": height,"is_page_image": is_page_image,
                "orientation":orientation, "segments":[]}
        for segment in segments:
            x_0, y_0, x_1, y_1, label, headers, data = segment
            page_segment = {"bbox": [int(x_0), int(y_0), int(x_1), int(y_1)], "label": label,
                            "content": data, "headers":headers}
            page["segments"].append(page_segment)
            if is_page_images_required:
                create_page_image(page_id)
#         print('make_page:',text_words,text_figure_words, image_regions, image_words, raw_images, is_page_image, padding,
#             orientation)
#     print('page_op',page)
    return page

                       
                       

# def make_json(self, xml_file=None, images=None, downsample=True) :
#     """
#     [summary]
#     Keyword Arguments:
#     xml_file {[type]}---[description] (default: {None})
#     images {[type]}---[description] (default: {None})
#     Returns:
#     [type]---[description]
#     """
#     document = {"num_pages": 0, "pages": []}
#     page_args =[]
#     pool = ThreadPool(4)
#     if xml_file is not None:
#         tree_parser = etree. XMLParser(recover=True)
#         root = etree.fromstring(open(xml_file, "rb").read(), parser=tree_parser)

#         for child in root:
#             tag = child.tag
#         if tag =='page':
#             obj= xml_utils.get_attribs(child.items ())
#             page_id= obj["id"]
#             width, height =obj["bbox"].split(",")[2:]
#             width =float(width)
#             height = float Cheight)
#             page_orientation=float(obj["rotate"])
#             if page_orientation != 0:
#                 page_orientation=360.- page_orientation
#             page_args.append({"page_id": page_id,
#                 "width": width,
#                 "height": height,
#                 "root": root,
#                 "image_file": None,
#                 "orientation":page_orientation})
#             document["num_pages"]+=1

#     elif images is not None:
#         for index, image_file in enumerate(images, 1):
#             page_id = str(index)
#             image = cv2.imread(image_file)
#             height, width, = image.shape
#             height = (height*72/300.)
#             width = (width*72/300.)
#             width = float(width)
#             height = float (height)
#             page_args.append({
#             "page_id": page_id,
#             "width": width,
#             "height": height,
#             "root": None ,
#             "image_file": image_file,
#             "orientation" : None
#             })
#         document["num_pages"] +=1

#     if self.auto detect_table!=0:
#     self.obj_table_detection = object_detection(self.source_file, self.rcnn_model_check_point,self.tf_api_url,self.tessdata,self.auto_detect_table,
#     self.table_extract_mode,self.dpi)
#     results=[]
#     for page_args_ in page_args:
#         rslts=make_page(page_args_)
#         results.append(rslts)
#     document["pages"] = results
#     toc_utils.add_toc(document)
#     cover_page_utils.get_cover_page(document)
#     hf_utils.add_headers_footers(document)
#     return document

def make_json(source_file,xml_file=None, images=None, downsample=True) :
    
    """
    [summary]
    Keyword Arguments:
    xml_file {[type]}---[description] (default: {None})
    images {[type]}---[description] (default: {None})
    
    Returns:
    [type]---[description]
    """
    document = {"num_pages": 0, "pages": []}
    page_args =[]
 #   pool = ThreadPool(4)
    if xml_file is not None:
        tree_parser = etree. XMLParser(recover=True)
        root = etree.fromstring(open(xml_file, "rb").read(), parser=tree_parser)
        for child in root:

            tag = child.tag
 
            if tag =='page':
                obj= xml_utils.get_attribs(child.items ())

                page_id= obj["id"]


                width, height =obj["bbox"].split(",")[2:]
                width =float(width)
                height = float (height)
                page_orientation=float(obj["rotate"])
                if page_orientation != 0:
                    page_orientation=.360 - page_orientation
                page_args.append({"page_id": page_id,
                    "width": width,
                    "height": height,
                    "root": root,
                    "image_file": None,
                    "orientation":page_orientation})
                document["num_pages"]+=1

    elif images is not None:
        for index, image_file in enumerate(images, 1):
            page_id = str(index)
            image = cv2.imread(image_file)

            height, width, = image.shape[0],image.shape[1]
            height = (height*72/300.)
            width = (width*72/300.)
            width = float(width)
            height = float (height)
            page_args.append({
            "page_id": page_id,
            "width": width,
            "height": height,
            "root": None ,
            "image_file": image_file,
            "orientation" : None
            })
        document["num_pages"] +=1
        
    if auto_detect_table !=0:
        
        obj_table_detection = object_detection(self.source_file, self.rcnn_model_check_point,self.tf_api_url,self.tessdata,self.auto_detect_table,
        table_extract_mode,self.dpi)
    results=[]
    for page_args_ in page_args:
        rslts=make_page(page_args_,source_file)
        results.append(rslts)
        print('\n rslts',rslts)
    document["pages"] = results
#                 toc_utils.add_toc(document)
#                 cover_page_utils.get_cover_page(document)
#                 hf_utils.add_headers_footers(document)
        

    return document
                       
# def make_xml(self):
#     """
#     "Convert PDF to XML using pdfminer
#     HII
#     Returns:
#     xml_file[str]---Path to xml file

#     """
#     xml_file = os.path.join(self.tmp_dir, self.name + ".xml")
#     if not os.path.exists(xml_file) or self.overwrite:
#         lock.acquire().
#         xml_utils.convert(self.source_file, xml_file)
#         lock.release()
#     parser = etree. XMLParser (recover=True)
#     root = etree.fromstring (open (xml_file, "rb").read(), parser=parser)
#     if not list (root):
#         raise PDFTextExtractionNotAllowed
#     return xml_file
def make_xml(source_file,name,tmp_dir):
    """
    "Convert PDF to XML using pdfminer
    Returns:
    xml_file[str]---Path to xml file
    """
    xml_file = os.path.join(tmp_dir, name + ".xml")

    if not os.path.exists(xml_file):

        xml_data=xml_utils.convert(source_file, xml_file)
        xml_data=xml_data+('</pages>')



        open(xml_file,"a",encoding="utf-8").write(xml_data)

    parser = etree.XMLParser(recover=True)
    root = etree.fromstring(open (xml_file, "rb").read(), parser=parser)
    if not list (root):
        raise PDFTextExtractionNotAllowed
    return xml_file

# def run(self)
#     """
#     "Run the PDF to JSON conversion on a single PDF
#     Returns:
#     status [bool]---If True, conversion was successful
#     """

#     start_time = time.time()
#     json_file = os. path.join(self.output_dir, self.name + ".json")
#     if os.path.exists(json_file) and not self.overwrite:
#     `	return True
#     if self.source_file.endswith(".pdf"):
#         try:
#             xml_file = self.make_xml()
#             data =self.make_json(xml_file-xml_file, images=None)
#         except PDFTextExtractionNotAllowed:
#             outfile = os.path.join(self.images_dir, self.name + ".png")
#             images = img_utils.convert_pdf_to_image(infile=self.source_file, outfile-outfile, overwrite=self.overwrite)
#             data = self.make_json (xml_file=None, images=images)
#     else:
#         outfile = os.path.join(self, images_dir, self.name + ".png")
#         images = img_utils.convert_page_to_image(infile=self.source file, outfile-outfile, overwrite=self.overwrite)
#         data = self.make_json(xml_file=None, images=images)

#     document = DocumentModel()
#     self.save_document(document.create(data, self.source_file, "pdf"))
#     if self.cleanup:
#         self.clean_dirs()
#         stop_time = time.time()
#         logger.info("Total time: %s", stop_time - start_time)
#         return True



def run(source_file,output_dir,name,tmp_dir):
    """
    "Run the PDF to JSON conversion on a single PDF
    Returns:
    status [bool]---If True, conversion was successful
    """

#     start_time = time.time()
    json_file = os.path.join(output_dir, name + ".json")
    print("json_file",json_file,"output_dir",output_dir)
#     if os.path.exists(json_file):
#         return True
#     if source_file.endswith(".pdf"):
#         try:
#             xml_file = make_xml(source_file,name, tmp_dir)
# #             print('xml_file',xml_file)
#             save_json(xml_file,json_file)
#             document_data=make_json(xml_file, images=None)
#         except PDFTextExtractionNotAllowed:
#             outfile = os.path.join(self.images_dir, self.name + ".png")
#             images = img_utils.convert_pdf_to_image(infile=self.source_file, outfile=outfile, overwrite=self.overwrite)
#             document_data = self.make_json (xml_file=None, images=images)
#             open(json_file,"a",encoding="utf-8").write(str(data))

#     else:
    outfile = os.path.join(output_dir, name + ".png")
    print("outfile",outfile,"output_dir",output_dir)
    images = img_utils.ocr_convert_page_to_image(infile=source_file, outfile=outfile, overwrite=True)
#     images=  pdf2image.convert_from_path(source_file)
    print("outfile1",outfile,"output_dir",output_dir)
    document_data = make_json(source_file=source_file,xml_file=None, images=images)
    print("outfile2",outfile,"output_dir",output_dir)
#         document = DocumentModel()
    document=model.create(document_data, source_file, "pdf")
    print("outfile3",outfile,"output_dir",output_dir)
#    if self.cleanup:
#        self.clean_dirs()
#     stop_time = time.time()
#     print("Total time: %s", stop_time - start_time)
    return document,document_data, True