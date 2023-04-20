import os
import re
import cv2
import pandas as pd
import numpy as np
import itertools
# from tabula import read_pdf
import traceback
# import processor.utils.camelot as camelot
# from processor.utils.detect_table_row_column import DetectTableRowColumns
import warnings
warnings.filterwarnings("ignore")
import logging
logger=logging.getLogger()
import sys


# def make_image_from_words(words, width, height, clean_up=False):
# 	words=sorted(words, key=lambda x:(x[1],[0]))
# 	width= int(width)
# 	height=int(height)
# 	page_image_undilated=np.zeros((height, width), dtype=np.'uint8')
# 	word_heights=[]
# 	for word in words:
# 		x_0=int(word[0])
# 		x_1=int(word[2])
#         y_0=int(word[1])
#         y_1=int(word[3])
# 	if clean_up:
# 		if word[-1].lstrip().rstrip() in ["", "_","__" ,"$", "S", ")", "("]:
# 			continue
# 		if x_1 - x_0 >= width:
# 			continue
# 		word_heights.append(y_1 - y_0)
# 		page_image_undilated[y_0:y_1, x_0:x_1]=255
# 	ker = np.ones((1, int(round(0.01 * width))), dtype=np.uint8)
# 	page_image=cv2.dilate(page_image_undilated, ker, iterations=1)
# 	word_heights=[int(x) for x in word_heights]
# 	median_height=np.median(word_heights)
# 	return page_image_undilated, word_heights, median_height



def make_image_from_words(words, width, height, clean_up=False):
# 	print('words',words)
    words=sorted(words, key=lambda x:(x[1],[0]))
    width= int(width)
    height=int(height)
    page_image_undilated=np.zeros((height, width), dtype='uint8')
    word_heights=[]

    for word in words:
        x_0=int(word[0])
        x_1=int(word[2])
        y_0=int(word[1])
        y_1=int(word[3])
        if clean_up:
            if word[-1].lstrip().rstrip() in ["", "_","__" ,"$", "S", ")", "("]:
                continue
            if x_1 - x_0 >= width:
                continue
        word_heights.append(y_1 - y_0)
        page_image_undilated[y_0:y_1, x_0:x_1]=255
    ker = np.ones((2, int(round(0.01 * width))),dtype='uint8')
    page_image=cv2.dilate(page_image_undilated, ker, iterations=3)
    word_heights=[int(x) for x in word_heights]
    median_height=np.median(word_heights) 

    return page_image_undilated, page_image, median_height

# def cut_segment(segment):
#     binary = np.any(segment, axis=1).astype('uint8')
#     contours,_ = cv2.findContours(binary, cv2.RETR_TREE, CV2.CHAIN_APPROX_SIMPLE)
#     regions=[]
#     for contour in contours:
#         points =[list(x) for xx in contour for x in xx]
#         points = np.array(points)
#         points= points [:,1]
#         if len(points)==1:
#             regions.append([points[0], points[0]+1])
#         else:
#             points [1] += 1
#             regions.append(list(points))
#     regions = sorted(regions, key=lambda x: (x[0]))
#     return regions

def cut_segment(segment):
    binary = np.any(segment, axis=1).astype('uint8')
    contours,_ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    regions=[]
    for contour in contours:
        points =[list(x) for xx in contour for x in xx]
        points = np.array(points)
        points= points [:,1]
        if len(points)==1:
            regions.append([points[0], points[0]+1])
        else:
            points [1] += 1
            regions.append(list(points))
    regions = sorted(regions, key=lambda x: (x[0]))
    return regions



# def are_regions_nearby(box1, box2, words, median_height, threshold=0.75):
#     try:
#         prev_start, prev_stop = box1
#         start, stop = box2
#         prev_words = [w for w in words if prev_start <= w[1]<= prev_stop or prev_start <= w[3] <= prev_stop]
#         curr_words = [w for w in words if start <=w[1] <= stop or start <= w[3] <= stop]
#         prev_words = sorted(prev_words, key=lambda x: (x[1], x[0]))
#         curr_words = sorted(curr_words, key=lambda x: (x[1], x[0]))
#         prev_word = prev_words [-1]
#         curr_word = curr_words [0]
#         if (curr_word[1] - prev_word [3]) > threshold*median_height:
#             return False
#         return True
#     except:
#         return False

#segmentation.py
def are_regions_nearby(box1, box2, words, median_height, threshold=0.75):
    try:
        prev_start, prev_stop = box1
        start, stop = box2
        prev_words = [w for w in words if prev_start <= w[1]<= prev_stop or prev_start <= w[3] <= prev_stop]
        curr_words = [w for w in words if start <=w[1] <= stop or start <= w[3] <= stop]
        prev_words = sorted(prev_words, key=lambda x: (x[1], x[0]))
        curr_words = sorted(curr_words, key=lambda x: (x[1], x[0]))
        prev_word = prev_words [-1]
        curr_word = curr_words [0]
        if (curr_word[1] - prev_word [3]) > threshold*median_height:
            return False
        return True
    except:
        return False
    
    
# def is_alignment_similar(boxl, box2, page_matrix):
#     width = np.shape (page_matrix) [1]
#     prev_image = page_matrix[box1[0] :box1[1], :]
#     next_image = page_matrix[box2[0] :box2[1], :]
#     prev_cuts=cut_segment (prev_image.T)
#     next_cuts=cut_segment(next_image.T)
#     if not prev_cuts or not next_cuts:
#         return False
#     if prev_cuts[0][0] < width // 2 and next_cuts[0][0] > width // 2:
#         return False
#     return True

def is_alignment_similar (box1, box2, page_matrix):
    width = np.shape (page_matrix) [1]
    prev_image = page_matrix[box1[0] :box1[1], :]
    next_image = page_matrix[box2[0] :box2[1], :]
    prev_cuts=cut_segment (prev_image.T)
    next_cuts=cut_segment(next_image.T)
    if not prev_cuts or not next_cuts:
        return False
    if prev_cuts[0][0] < width // 2 and next_cuts[0][0] > width // 2:
        return False
    return True



# def are_columns_separable(box, page_matrix):
#     width = np.shape(page_matrix)[1]
#     box_matrix = page_matrix[box[0]:box[1], :]
#     ker = np.ones((1, int(round(0.01 * width))), dtype=np.uint8)
#     box_dilated = cv2.dilate (box_matrix, ker, iterations=3)
#     cuts = cut_segment(box_dilated.T)
#     if not cuts:
#         return False
#     return bool(len(cuts) > 1)

def are_columns_separable(box, page_matrix):
    width = np.shape(page_matrix)[1]
    box_matrix = page_matrix[box[0]:box[1], :]
    ker = np.ones((1, int(round(0.01 * width))), dtype=np.uint8)
    box_dilated = cv2.dilate (box_matrix, ker, iterations=3)
    cuts = cut_segment(box_dilated.T)
    if not cuts:
        return False
    return bool(len(cuts) > 1)

# def get_segment_margins(segment_matrix):
#     top, bottom, left, right = [0]*4
#     gaps_tb = list(np.any(segment_matrix, axis=1).astype('int'))
#     gaps_lr = list(np.any(segment_matrix.T, axis=1).astype('int'))
#     i = 0
#     for i, val in enumerate(gaps_tb):
#         if val == 1:
#             break
#     top = i
#     gaps_tb.reverse()
#     for i, val in enumerate (gaps_tb):
#         if val == 1:
#             break
#     bottom = len(gaps_tb) - i
#     for i, val in enumerate (gaps_lr):
#         if val == 1:
#             break
#     left=i
#     gaps_lr.reverse()
#     for i, val in enumerate (gaps_lr):
#         if val == 1:
#             break
#     right = len(gaps_lr) - i

#     return top, bottom, left, right

def get_segment_margins(segment_matrix):
    top, bottom, left, right = [0]*4
    gaps_tb = list(np.any(segment_matrix, axis=1).astype('int'))
    gaps_lr = list(np.any(segment_matrix.T, axis=1).astype('int'))
    i = 0
    for i, val in enumerate(gaps_tb):
        if val == 1:
            break
    top = i
    gaps_tb.reverse()
    for i, val in enumerate (gaps_tb):
        if val == 1:
            break
    bottom = len(gaps_tb) - i
    for i, val in enumerate (gaps_lr):
        if val == 1:
            break
    left=i
    gaps_lr.reverse()
    for i, val in enumerate (gaps_lr):
        if val == 1:
            break
    right = len(gaps_lr) - i

    return top, bottom, left, right


# def is_region_sparse(box, page_matrix, threshold=0.8):
#     box_matrix = page_matrix [box[0]: box[1], :]
#     margins = get_segment_margins(box_matrix)
#     cropped_matrix = box_matrix[margins [0] :margins [1], margins[2] :margins [3]]
#     num_white_pix= np.sum(cropped_matrix == 255)
#     total_pix = cropped_matrix.shape [0]*cropped_matrix.shap[1]
#     ratio = float(num_white_pix)/total_pix
#     return bool(ratio <= threshold)
def is_region_sparse(box, page_matrix, threshold=0.8):
    box_matrix = page_matrix [box[0]: box[1], :]
    margins = get_segment_margins(box_matrix)
    cropped_matrix = box_matrix[margins [0] :margins [1], margins[2] :margins [3]]
    num_white_pix= np.sum(cropped_matrix == 255)
    total_pix = cropped_matrix.shape [0]*cropped_matrix.shape[1]
    ratio = float(num_white_pix)/total_pix
    return bool(ratio <= threshold)




# def is_first_column_bullet_points(t_b, l_r, words) :
#     y0, yl = t_b
#     x0, xl = l_r[0]
#     column_words = [w for w in words if w[0] >= x0]
#     column_words = [w for w in column_words if w[2] <= x1]
#     column_words = [w for w in column_words if w[1] >= y0]
#     column_words = [w for w in column_words if w[3] <= yl]
#     if not column_words:
#         return True
#     column_words = sorted(column_words, key=lambda x: (x[1], x[0]))
#     column_text= "".join([w[-1] for w in column_words])
#     # Check for non alpha-numeric characters
#     pattern = re.compile("[^a-zA-Z0-9$]")
#     text = re.sub(pattern, "", column_text)
#     text= ''.join([w for w in text.split() if w])
#     if not text:
#         return True
#     # Check for bullet point patterns - a., A. or 1., etc
#     pattern = re.compile("^[a-zA-Z0-9]+\.$")
#     match = re.findall(pattern, column_text)
#     if match:
#         return True
#     # Check for bullet point patterns (a), (A) or (1), etc.
#     pattern = re.compile("^\([a-zA-Z0-9]+)$")
#     match = re.findall(pattern, column_text)
    
#     if match:
#         return True
#     return False

def is_first_column_bullet_points(t_b, l_r, words) :
    y0, y1 = t_b
    x0, x1 = l_r[0]
    column_words = [w for w in words if w[0] >= x0]
    column_words = [w for w in column_words if w[2] <= x1]
    column_words = [w for w in column_words if w[1] >= y0]
    column_words = [w for w in column_words if w[3] <= y1]
    if not column_words:
        return True
    column_words = sorted(column_words, key=lambda x: (x[1], x[0]))
    column_text= "".join([w[-1] for w in column_words])
    # Check for non alpha-numeric characters
    pattern = re.compile("[^a-zA-Z0-9$]")
    text = re.sub(pattern, "", column_text)
    text= ''.join([w for w in text.split() if w])
    if not text:
        return True
    # Check for bullet point patterns - a., A. or 1., etc
    pattern = re.compile("^[a-zA-Z0-9]+\.$")
    match = re.findall(pattern, column_text)
    if match:
        return True
    # Check for bullet point patterns (a), (A) or (1), etc.
    pattern = re.compile("^\[a-zA-Z0-9]+$")
    match = re.findall(pattern, column_text)

    if match:
        return True
    return False
                    
# def is_table_in_page_header(t_b, l_r, words, page_header_threshold=60):
#     if t_b[0] < page_header_threshold:
#         return True
#     else:
#         return False

def is_table_in_page_header(t_b, l_r, words, page_header_threshold=60):
    if t_b[0] < page_header_threshold:
        return True
    else:
        return False


# def label_segments(tb_cuts, Ir_cuts, page_matrix, words):
#     # Label segments as PARA or TABLE First Pass
#     segments=[]
#     for t_b, l_r in zip(tb_cuts, lr_cuts):
#         num_cols=len(l_r)
#         if (num_cols) > 1:
#             if is_region_sparse(t_b, page_matrix) and \
#                 are_columns_separable(t_b, page_matrix) and not \
#                 is_first_column_bullet_points(t_b, l_n, words) and not \
#                 is_table_in_page_header (t_b, l_r, words):
#                 block_type="TABLE"
#             else:
#                 block_type="PARA"
#         elif num_cols==1:
#             block_type="PARA"
#         else:
#             block_type = None
#         if block_type:
#             segments.append([t_b[0], t_b[1], block_type])
#     return segments

def label_segments(tb_cuts, lr_cuts, page_matrix, words):
    # Label segments as PARA or TABLE First Pass

    segments=[]
    for t_b, l_r in zip(tb_cuts, lr_cuts):
        num_cols=len(l_r)
        if (num_cols) > 1:
            if is_region_sparse(t_b, page_matrix) and \
                are_columns_separable(t_b, page_matrix) and not \
                is_first_column_bullet_points(t_b, l_r, words) and not \
                is_table_in_page_header (t_b, l_r, words):
                block_type="TABLE"
            else:
                block_type="PARA"
        elif num_cols==1:
            block_type="PARA"
        else:
            block_type = None
        if block_type:
            segments.append([t_b[0], t_b[1], block_type])
    return segments	


# def merge_table_neighbors(segments, page_matrix, words, median_height, threshold) :
# processed = []
# merged_segments = []
# for idx, segment in enumerate (segments):
# merge []
# if idx in processed:
# continue
# label = segment
# if label != "TABLE":
# continue
# prev =
# int(idx)
# while True:
# prev = 1
# if prev <0 or prev in processed:
# break
# prev_segment = segments [prev]
# prev_start, prev_stop, prev_label prev_segment
# if prev_label == "TABLE":
# start, stop, label = segments [prev+1]
# is nearby = are regions_nearby ([prev_start, prev_stop], [
# start, stop], words, median_height, threshold)
# if is nearby:
# merge.append(prev)
# processed.append(prev)
# else:
# break
# elif prev_label == "PARA":
# # Check distance, check alignment
# start, stop, label = segments [prev+1]
# is_nearby = are_regions_nearby ([prev_start, prev_stop], [
# start, stop), words, median_height,
# if is nearby:
# tmp = page_matrix[prev_start:prev_stop, :]
# tmp_width = np.shape (page_matrix)[1]
# tmp_cuts = cut_segment(tmp.T)
# if (tmp_cuts[0][0] < tmp_width // 2):
# if (tmp_cuts[0][1] > tmp_width // 2):
# break
# merge.append(prev)
# processed.append(prev)

# else:
# 	break
# _, _, label=segment

# nxt=int(idx)
# while True :
# 	nxt += 1
# if nxt >= len(segments) or nxt in processed:
# break
# nxt_segment = segments [nxt]
# nxt_start, nxt_stop, nxt_label = nxt_segment
# if nxt_label == "TABLE":
# start, stop, label = segments [nxt-1]
# is_nearby = are regions_nearby
# [start, stop], [nxt_start, nxt_stop), words, median_height,
# if is nearby:
# merge. append(nxt)
# processed.append(nxt)
# else:
# break
# elif nxt_label == "PARA":
# # Check distance, check alignment
# start, stop, label segments [nxt-1]
# is_nearby = are regions_nearby
# [start, stop], [nxt_start, nxt_stop], words, median_height,
# if is nearby:
# tmp = page_matrix[nxt_start:nxt_stop, :]
# tmp_width = np.shape (page_matrix)[1]
# tmp_cuts = cut_segment (tmp.T)
# if (tmp_cuts[0][0] <tmp_width // 2):
# 	if (tmp_cuts[0][1] > tmp_width // 2):
	
# merge.append(nxt)
# processed.append(nxt)
# else:
# break
# if merge:
# merge.append(idx)
# merge.sort()
# processed.append(idx)
# merged_segments.append(merge)
# new_segments = []
# indices
# for seg in merged_segments:
# indices.extend (seg)
# start = segments[seg[0]] [0]
# stop = segments[seg[-1]][1]
# new_segments.append([start, stop, "TABLE"])
# indices = list(set(indices))
# indices.sort()
# for idx, segment in enumerate (segments):
# if idx not in indices:
# new_segments.append(segment)
# segments = sorted(new_segments, key lambda : (x[0]))
# return segments


def merge_table_neighbors(segments, page_matrix, words, median_height, threshold) :
    processed = []
    merged_segments = []
    new_segments = []
    indices=[]
#     new_segments = []
#     indices=[]
    for idx, segment in enumerate (segments):
        merge=[]
        if idx in processed:
            continue
        _,_, label = segment
        if label != "TABLE":
            continue
        prev =int(idx)
        while True:
            prev-=1
            if prev <0 or prev in processed:
                break

            prev_segment = segments[prev]
            prev_start, prev_stop, prev_label=prev_segment

            if prev_label == "TABLE":
                start, stop, label = segments[prev+1]

                is_nearby = are_regions_nearby([prev_start, prev_stop], [start, stop], words, median_height, threshold)
                if is_nearby:

                    merge.append(prev)
                    processed.append(prev)
                else:

                    break
            elif prev_label == "PARA":
    # Check distance, check alignment
                start, stop, label = segments [prev+1]
                is_nearby = are_regions_nearby ([prev_start, prev_stop], [start, stop], words, median_height,threshold)
                if is_nearby:
                    tmp = page_matrix[prev_start:prev_stop, :]
                    tmp_width = np.shape(page_matrix)[1]
                    tmp_cuts = cut_segment(tmp.T)
                    if (tmp_cuts[0][0] < tmp_width // 2):
                        if (tmp_cuts[0][1] > tmp_width // 2):
                            break
                        merge.append(prev)
                        processed.append(prev)

                    else:
                        break
#     _, _, label=segment

        nxt=int(idx)
        while True :
            nxt += 1
            if nxt >= len(segments) or nxt in processed:
                break
            nxt_segment = segments [nxt]
            nxt_start, nxt_stop, nxt_label = nxt_segment

            if nxt_label == "TABLE":
                
                start, stop, label = segments[nxt-1]

                is_nearby = are_regions_nearby ([prev_start, prev_stop], [start, stop], words, median_height,threshold)
                if is_nearby:
                    merge.append(nxt)
                    processed.append(nxt)
                else:
                    break
            elif nxt_label == "PARA":
            # Check distance, check alignment
                start, stop, label= segments[nxt-1]
                is_nearby = are_regions_nearby ([prev_start, prev_stop], [start, stop], words, median_height,threshold)
                if is_nearby:
                    tmp = page_matrix[nxt_start:nxt_stop, :]
                    tmp_width = np.shape (page_matrix)[1]
                    tmp_cuts = cut_segment (tmp.T)
                    if (tmp_cuts[0][0] <tmp_width // 2):
                        if (tmp_cuts[0][1] > tmp_width // 2):

                            merge.append(nxt)
                            processed.append(nxt)
                    else:
                        break
        if merge:

            merge.append(idx)
            merge.sort()
            processed.append(idx)
            merged_segments.append(merge)

        for seg in merged_segments:
            indices.extend(seg)
            start = segments[seg[0]] [0]
            stop = segments[seg[-1]][1]
            new_segments.append([start, stop, "TABLE"])
            indices = list(set(indices))
            indices.sort()
    for idx, segment in enumerate(segments):
        if idx not in indices:
            new_segments.append(segment)
            segments = sorted(new_segments, key= lambda x:(x[0]))
    return segments


# def merge_paragraph_neighbors (segments, page_matrix, words, median_height, threshold):
# 	processed []
# 	merged_segments = []
# 	for idx, segment in enumerate(segments) :
# 		merge=[]
# 		if idx in processed:
# 			continue
# 		_, _, label = segment
# 		if label != "PARA":, 
# 			continue
# 		prev=int(idx)
# 		while True:
# 			prev-=1
# 			if prev <0 or prev in processed:
# 				break
# 			prev_segment = segments[prev]
# 			prev_start, prev_stop, prev_label = prev_segment
# 			if prev_label == "PARA":
# 				start, stop, label = segments[prev+1]
# 				# Check distance
# 				is_nearby = are_regions_nearby([prev_start, prev_stop], [start, stop], words, median_height, threshold)
# 				if is_nearby:
# 					if is_alignment_similar ([prev_start, prev_stop], [start, stop], page_matrix):
# 						merge.append(prev)
# 						processed.append(prev)
# 					else:
# 						break
# 				else:
# 					break
# 			else:
# 				break	
# 		nxt=int(idx)
# 		while True:
# 			nxt += 1
# 			if nxt >= len(segments) or nxt in processed:
# 				break
# 			nxt_segment = segments [nxt]
# 			nxt_start, nxt_stop, nxt_label= nxt_segment
# 			if nxt_label == "PARA":
# 				start, stop, label =segments[nxt-1]
# 				is_nearby = are_regions_nearby([start, stop], [nxt_start, nxt stop], words, median_height, threshold)
# 				if is_nearby:
# 					if is_alignment similar([start, stop], [nxt_start, nxt_stop], page_matrix):
# 						merge. append (nxt)
# 						processed.append(nxt)
# 					else:
# 						break
# 				else:
# 					break
# 		if merge:
# 			merge.append(idx)
# 			merge.sort()
# 			processed.append(idx)
# 			merged_segments.append(merge)
# 		new_segments = []
# 		indices =[]
# 		for seg in merged_segments:
# 			indices.extend(seg)
# 			start=segments[seg[0]][0]
# 			stop = segments (seg[-1]][1]
# 			new_segments.append([start, stop, "PARA
# 			indices=list(set(indices))
# 			indices.sort()
# 	for idx, segment in enumerate(segments):
# 		if idx not in indices:
# 			new_segments.append(segment)
# 			segments = sorted (new_segments, key=lambda x: (x[0]))
# 		return segments



def merge_paragraph_neighbors (segments, page_matrix, words, median_height, threshold):
    processed=[]
    merged_segments = []
    for idx, segment in enumerate(segments) :
        merge=[]
        if idx in processed:
            continue
        _, _, label = segment
        if label != "PARA":
            continue
        prev=int(idx)
        while True:
            prev-=1
            if prev <0 or prev in processed:
                break
            prev_segment = segments[prev]
            prev_start, prev_stop, prev_label = prev_segment
            if prev_label == "PARA":
                start, stop, label = segments[prev+1]
                # Check distance
                is_nearby = are_regions_nearby([prev_start, prev_stop], [start, stop], words, median_height, threshold)
                if is_nearby:
                    if is_alignment_similar ([prev_start, prev_stop], [start, stop], page_matrix):
                        merge.append(prev)
                        processed.append(prev)
                    else:
                        break
                else:
                    break
            else:
                break
        nxt=int(idx)
        while True:
            nxt += 1
            if nxt >= len(segments) or nxt in processed:
                break
            nxt_segment = segments [nxt]
            nxt_start, nxt_stop, nxt_label= nxt_segment
            if nxt_label == "PARA":
                start, stop, label =segments[nxt-1]
                is_nearby = are_regions_nearby([start, stop], [nxt_start, nxt_stop], words, median_height, threshold)
                if is_nearby:
                    if is_alignment_similar([start, stop], [nxt_start, nxt_stop], page_matrix):
                        merge.append (nxt)
                        processed.append(nxt)
                    else:
                        break
                else:
                    break

        if merge:
            merge.append(idx)
            merge.sort()
            processed.append(idx)
            merged_segments.append(merge)
        new_segments = []
        indices =[]
        for seg in merged_segments:
            indices.extend(seg)
            start=segments[seg[0]][0]
            stop = segments [seg[-1]][1]
            new_segments.append([start, stop, "PARA"])
            indices=list(set(indices))
            indices.sort()
    for idx, segment in enumerate(segments):
        if idx not in indices:
            new_segments.append(segment)
            segments = sorted (new_segments, key=lambda x: (x[0]))
        return segments
                

# def are_tables_similar(segment1, segment2, tb_cuts, lr_cuts, height):
# 	start1, stopl, =segment1
# 	start2, stop2, =segment2
# 	gap = float(start2-stop1)
# 	if gap > 0.05*height:
# 		return False
# 	rows1 = []
# 	for index, t_b in enumerate(tb_cuts):
# 		if t_b[0] < start1:
# 			continue
# 		if t_b[1] > stopl:
# 			continue
# 		rows1.append(index)
	
# 	rows 2 = []
# 	for index, t_b in enumerate (tb_cuts):
# 		if t_b[0] < start2:
# 			continue
# 		if t_b[1] > stop2:
# 			continue
# 		rows2.append(index)
		
# 		cutsl (tr cuts[1] for in rows1
# cuts2 = [lr_cuts[1] for i in rows2]
# if not cutsl or not cuts2:
# return false
# left1 = min([x[0] for xx in cutsl for x in xx])
# left2 = mìn([x[0] for xx in cuts2 for x in xx])
# right1 = max([x[1] for xx in cutsl for x in xx])
# right2 = max( [x[1] for xx in cuts2 for x in xx])
# pixels
# if np.abs (left1
# return True
# left2) < 5 and np.abs (right
# right2) < 5:
# return false


def are_tables_similar(segment1, segment2, tb_cuts, lr_cuts, height):
    start1, stop1, _ =segment1
    start2, stop2, _ =segment2
    gap = float(start2-stop1)
    if gap > 0.05*height:
        return False
    rows1 = []
    for index, t_b in enumerate(tb_cuts):
        if t_b[0] < start1:
            continue
        if t_b[1] > stop1:
            continue
        rows1.append(index)

    rows2 = []
    for index, t_b in enumerate (tb_cuts):
        if t_b[0] < start2:
            continue
        if t_b[1] > stop2:
            continue
        rows2.append(index)

    cuts1=[lr_cuts[i] for i in rows1]
    cuts2 = [lr_cuts[i] for i in rows2]
    if not cuts1 or not cuts2:
        return False
    left1 = min([x[0] for xx in cuts1 for x in xx])
    left2 = min([x[0] for xx in cuts2 for x in xx])
    right1 = max([x[1] for xx in cuts1 for x in xx])
    right2 = max( [x[1] for xx in cuts2 for x in xx])
    
    if np.abs (left1-left2)<5 and np.abs (right1-right2) < 5:
        return True
    return False

                
                
# def merge_consecutive_tables (segments, tb_cuts, lr_cuts, page_matrix)
# processed = []
# merged_segments = []
# for idx, segment in enumerate (segments):
# merge = []

# if idx in processed:
# continue
# label = segment
# if label != "TABLE":
# continue
# nxt =
# int(idx)
# while True:
# nxt += 1
# if nxt >= len(segments) or nxt in processed:
# break
# nxt_segment = segments [nxt]
# nxt_segment
# if nxt label != "TABLE":
# break
# is_similar = are_tables similar
# segments [nxt-1], nxt_segment, tb_cuts, ir cuts, page_matrix.shape [0])
# if is similar:
# merge.append(nxt)
# processed.append(nxt)
# else:
# break
# -, nxt_label
# if merge :
# merge.append(idx)
# merge.sort()
# processed.append(idx)
# merged_segments.append(merge)
# new_segments = []
# indices = []
# for seg in merged_segments:
# indices.extend(seg)
# start = segments[seg[0]][0]
# stop = segments (seg[-1]][1]
# new_segments.append([start, stop, TABLE"])
# indices = list(set(indices))
# indices.sort()
# for idx, segment in enumerate (segments):
# if idx not in indices:
# new_segments.append(segment)
# segments = sorted(new_segments, key=lambda x: (x[0]))
# return segments

 
def merge_consecutive_tables(segments, tb_cuts, lr_cuts, page_matrix):
    processed = []
    merged_segments = []
    for idx, segment in enumerate(segments):
        merge = []
        if idx in processed:
            continue
        _,_, label = segment
        if label == "TABLE":
            continue 
        nxt = int(idx) 
        while True:
            nxt += 1
            if nxt >= len(segments) or nxt in processed:
                break

            nxt_segment = segments[nxt]
            _,_, nxt_label = nxt_segment
            if nxt_label != "TABLE":
                break
            is_similar = are_tables_similar(
                segments[nxt-1], nxt_segment, tb_cuts, lr_cuts, page_matrix.shape[0])


            if is_similar:
                merge .append (nxt)
                processed. append (nxt)
            else:
                  break

        if merge:
            merge.append (idx)
            merge.sort()
            processed.append(idx)
            merged_segments.append (merge)

    new_segments = []
    indices = []
    for seg in merged_segments:
        indices.extend(seg)
        start = segments[seg[0]] [0]
        stop = segments[seg[-1]][1]
        new_segments.append([start, stop, "TABLE"]) 
    indices = list(set (indices) )
    indices.sort()

    for idx, segment in enumerate(segments) :
        if idx not in indices:
            new_segments.append (segment)

    segments = sorted(new_segments, key=lambda x: (x[0])) 
    return segments

# def make_cells (segment, margins, words, start, stop):
#     tb_cuts = cut_segment(segment)
#     lr_cuts=[]
#     max_len=0
#     max_idx = -1
#     for idx, t_b in enumerate (tb_cuts):
#         row_matrix = segment[t_b[0]:t_b[1], :].T
#         l_r = cut_segment (row_matrix)
#         lr_cuts.append(l_r)
#         if len(l_r) > max_len:
#             max_len =len(l_r)
#             max_idx = idx
#     table=[]
#     if max_idx == -1:
#         return table

#     ref_cells = lr_cuts [max_idx]
#     for idx, (t_b, l_r) in enumerate (zip(tb_cuts, lr_cuts)):
#         y_0 = float(start + t_b[0])
#         y_1 = float(start + t_b[1])
#         row_words = [w for w in words if w[1] >= y_0]
#         row_words=[w for w in row_words if w[3] <= y_1]
#         row=[]
#         row=[[] for _ in range (max_len)]
#         non_empty = False
#         for cell_x_0, cell_x_1 in l_r:
#             cell_words = [w for w in row_words if w[0] >= cell_x_0]
#             cell_words=[w for w in cell_words if w[2] <= cell_x_1]
#             if not cell_words:
#                 continue
#             cell_words = reorder_words(cell_words)
#             cell_start=cell_words[0][0]
#             cell_stop = cell_words[-1][2]
#             selected_cell = None
#             for cell_idx, tmp in enumerate(ref_cells):
#                 if cell_start <= tmp[1]:
#                     selected_cell=cell_idx
#                     break
#             if selected_cell is not None:
#                 row[selected_cell] += cell_words
#                 non_empty = True
#         if non_empty:
#             table.append(row)
#     return table

def make_cells (segment, margins, words, start, stop):
    tb_cuts = cut_segment(segment)
    lr_cuts=[]
    max_len=0
    max_idx = -1
    for idx, t_b in enumerate (tb_cuts):
        row_matrix = segment[t_b[0]:t_b[1], :].T
        l_r = cut_segment (row_matrix)
        lr_cuts.append(l_r)
        if len(l_r) > max_len:
            max_len =len(l_r)
            max_idx = idx
    table=[]
    if max_idx == -1:
        return table

    ref_cells = lr_cuts [max_idx]
    for idx, (t_b, l_r) in enumerate (zip(tb_cuts, lr_cuts)):
        y_0 = float(start + t_b[0])
        y_1 = float(start + t_b[1])
        row_words = [w for w in words if w[1] >= y_0]
        row_words=[w for w in row_words if w[3] <= y_1]
        row=[]
        row=[[] for _ in range (max_len)]
        non_empty = False
        for cell_x_0, cell_x_1 in l_r:
            cell_words = [w for w in row_words if w[0] >= cell_x_0]
            cell_words=[w for w in cell_words if w[2] <= cell_x_1]
            if not cell_words:
                continue
            cell_words = reorder_words(cell_words)
            cell_start=cell_words[0][0]
            cell_stop = cell_words[-1][2]
            selected_cell = None
            for cell_idx, tmp in enumerate(ref_cells):
                if cell_start <= tmp[1]:
                    selected_cell=cell_idx
                    break
            if selected_cell is not None:
                row[selected_cell] += cell_words
                non_empty = True
        if non_empty:
            table.append(row)
    return table

# def is_y_similar(iteml, item2):
#     _, y_0, _, y_l = item1[0:4]
#     _, yy_0, _, yy_l=item2[0:4]
#     d_0 = np.abs(y_0 - yy_0)
#     d_1 = np.abs(y_1 - yy_1)
#     np.abs(y_1 - yy_1)
#     if d_0 < 5 and d_1 < 5:
#         return True
#     return false

def is_y_similar(item1, item2):
    _, y_0, _, y_1 = item1[0:4]
    _, yy_0, _, yy_1=item2[0:4]
    d_0 = np.abs(y_0 - yy_0)
    d_1 = np.abs(y_1 - yy_1)
    np.abs(y_1 - yy_1)
    if d_0 < 5 and d_1 < 5:
        return True
    return False


# def reorder_words(words):
#     words = sorted(words, key=lambda x: (x[1], x[0]))
#     indices = []
#     unique_y = {}
#     for idx, item in enumerate (words) :
#         if idx not in indices:
#             indices.append(idx)
#             unique_y[tuple(item[0:4])] =[item]
#             for idx2, item2 in enumerate (words):
#                 if idx2 not in indices:
#                     y_similar=is_y_similar(item, item2)
#                     if y_similar:
#                         unique_y[tuple (item[0:4])].append(item2)
#                         indices.append(idx2)
#     new_words =[]
#     for _, value in unique_y.items():
#         y_0 = min([x[1] for x in value])
#         y_1 = max([x[3] for x in value])
#         for x in value:
#             new_words.append([x[0], y_0, x[2], y_1, x[-2], x[-1]])
#     new_words = sorted (new_words, key=lambda x: (x[1],x[0]))
#     return new_words
#segmentation.py
def reorder_words(words):
    words = sorted (words, key=lambda x: (x[1], x[0]))
    indices = []
    unique_y = {}
    for idx, item in enumerate (words) :
        if idx not in indices:
            indices.append(idx)
            unique_y[tuple(item[0:4])] = [item]
            for idx2, item2 in enumerate (words):
                if idx2 not in indices:
                    y_similar=is_y_similar(item, item2)
                    if y_similar:
                        unique_y[tuple (item[0:4])].append(item2)
                        indices.append(idx2)
    new_words =[]
    for _, value in unique_y.items():
        y_0 = min([x[1] for x in value])
        y_1 = max([x[3] for x in value])
        for x in value:
            new_words.append([x[0], y_0, x[2], y_1, x[-2], x[-1]])
    new_words = sorted (new_words, key=lambda x: (x[1],x[0]))
    return new_words

                                
                                  
# def make_paragraph (words, start, stop):
#     block = None
#     start = float(start)-2
#     stop == float(stop) + 2
#     para_words = [w for w in words if w[1] >= start]
#     para_words = [w for w in para_words if w[3] <= stop]
#     para_words = sorted(para_words, key=lambda x: (x[1]))
#     para_words = reorder_words (para_words)
#     if para_words:
#         points = [w[0:4] for w in para_words]
#         points = np.array (points)
#         x_0, y_0 = np.min(points [:, 0:2], axis=0)
#         x_1, y_1 = np.max (points[:, 2:4], axis=0)
#         return [x_0, y_0, x_1, y_1, "PARA", None, para_words]
#     return block

#segmentation.py
def make_paragraph (words, start, stop):
#     print('make_paragraph_start_words',words)

    block = None
    start = float(start)-2
    stop = float(stop) + 2
    para_words = [w for w in words if w[1] >= start]
   
    para_words = [w for w in para_words if w[3] <= stop]
  
    para_words = sorted(para_words, key=lambda x: (x[1]))

    para_words = reorder_words (para_words)

    
    if para_words:
        points = [w[0:4] for w in para_words]
        points = np.array (points)
        x_0, y_0 = np.min(points [:, 0:2], axis=0)
        x_1, y_1 = np.max (points[:, 2:4], axis=0)
        
        return [x_0, y_0, x_1, y_1, "PARA", None, para_words]
    
    return block



# def split_multiline_cells(table):
#     new_table = []
#     for row in table:
#         num_lines = []
#         cols = []
#         for cell in row:
#             lines = get_lines (cell)
#             cols.append(lines)
#             num_lines.append(len(lines))
#         unique = set(num_lines)
#         if 0 in unique :
#             unique. remove (0)
#         if len(unique)==1:
#             if 1 in unique :
#                 new_table.append (row)
#                 continue
#             else:
#                 num = list(unique) [0]
#                 for idx in range (num):
#                     new_row = []
#                     for cell in cols:
#                         try:
#                             new_row.append(cell[idx])
#                         except:
#                             new_row.append([])
#                 new_table.append(new_row)
#         else:
#             max_lines_idx = np.argsort(num_lines)[-1]
#             ref = cols[max_lines_idx]
#             prev_rr = False
#             p_rr = [[] for _ in range (len(cols))]
#             rr = [[] for _ in range (len(cols))]
#             for line in ref:
#                 y_0 = min([w[1] for w in line])
#                 y_1 = max([w[3] for w in line])
#                 rr[max_lines_idx].extend(line)
#                 for idx, col in enumerate (cols):
#                     if idx == max_lines_idx:
#                         continue
#                     for line2 in col:
#                         yy_0 = min([w[1] for w in line2])
#                         yy_1 = max( [w[3] for w in line2])
#                         d_0 = np.abs(y_0 - yy_0)
#                         d_1 = np.abs(y_l - yy_1)
#                         if (d_0<5) and (d_1<5):
#                             rr[idx].extend(line2)
#                 ll = [float(len(xx)>0) for xx in rr]
#                 m = np.mean(ll)
#                 if m <= 0.5:
#                     if prev_rr is False:
#                         new_table.append(rr)
#                         prev_rr = False
#                         p_rr = [[] for _ in range(len(cols))]
#                         rr=[[] for _ in range(len(cols))]
#                     else:
#                         for j, tmp in enumerate(rr):
#                             p_rr[j].extend(tmp)
#                         prev_rr=True
#                         rr = [[] for _ in range(len(cols))]
#                 else:
#                     if prev_rr is not False:
#                         new_table.append(p_rr)
#                         p_rr = rr
#                         prev_rr = True
#                     rr = [[] for _ in range(len(cols))]
                    
#             if prev_rr is not False:
#                 new_table.append(p_rr)
#     return new_table

#segmentation.py
def split_multiline_cells(table):
    new_table = []
    for row in table:
        num_lines = []
        cols = []
        for cell in row:
            lines = get_lines (cell)
            cols.append(lines)
            num_lines.append(len(lines))
        unique = set(num_lines)
        if 0 in unique :
            unique. remove (0)
        if len(unique)==1:
            if 1 in unique :
                new_table.append (row)
                continue
            else:
                num = list(unique) [0]
                for idx in range (num):
                    new_row = []
                    for cell in cols:
                        try:
                            new_row.append(cell[idx])
                        except:
                            new_row.append([])
                new_table.append(new_row)
        else:
            max_lines_idx = np.argsort(num_lines)[-1]
            ref = cols[max_lines_idx]
            prev_rr = False
            p_rr = [[] for _ in range (len(cols))]
            rr = [[] for _ in range (len(cols))]
            for line in ref:
                y_0 = min([w[1] for w in line])
                y_1 = max([w[3] for w in line])
                rr[max_lines_idx].extend(line)
                for idx, col in enumerate (cols):
                    if idx == max_lines_idx:
                        continue
                    for line2 in col:
                        yy_0 = min([w[1] for w in line2])
                        yy_1 = max( [w[3] for w in line2])
                        d_0 = np.abs(y_0 - yy_0)
                        d_1 = np.abs(y_1 - yy_1)
                        if (d_0<5) and (d_1<5):
                            rr[idx].extend(line2)
                ll = [float(len(xx)>0) for xx in rr]
                m = np.mean(ll)
                if m <= 0.5:
                    if prev_rr is False:
                        new_table.append(rr)
                        prev_rr = False
                        p_rr = [[] for _ in range(len(cols))]
                        rr=[[] for _ in range(len(cols))]
                    else:
                        for j, tmp in enumerate(rr):
                            p_rr[j].extend(tmp)
                        prev_rr=True
                        rr = [[] for _ in range(len(cols))]
                else:
                    if prev_rr is not False:
                        new_table.append(p_rr)
                        p_rr = rr
                        prev_rr = True
                    rr = [[] for _ in range(len(cols))]
                    
            if prev_rr is not False:
                new_table.append(p_rr)
    return new_table


# def get_lines(cell_words): 
#     cell_words = sorted (cell_words, key=lambda x: (x[1], x[0]))
#     indices = []
#     unique_Y = {}
#     for idx, item in enumerate(cell_words) :
#         if idx not in indices:
#             indices.append(idx)
#             unique_y[tuple(item [0:4])] = [item]
#             for idx2, item2 in enumerate(cell_words):
#                 if idx2 not in indices:
#                     y_similar = is_y_similar(item, item2)
#                     if y_similar:
#                         unique_y[tuple(item [0:4])].append(item2)
#                         indices.append(idx2)
#     lines=[]
#     for _ , value in unique_y.item():
#         lines.append(sorted(value,key=lambda x: (x[1], x[0])))
#     return lines

def get_lines(cell_words): 
    cell_words = sorted (cell_words, key=lambda x: (x[1], x[0]))
    indices = []
    unique_y = {}
    for idx, item in enumerate(cell_words) :
        if idx not in indices:
            indices.append(idx)
            unique_y[tuple(item [0:4])] = [item]
            for idx2, item2 in enumerate(cell_words):
                if idx2 not in indices:
                    y_similar = is_y_similar(item, item2)
                    if y_similar:
                        unique_y[tuple(item [0:4])].append(item2)
                        indices.append(idx2)
    lines=[]
#     print("unique_yx",unique_y)
    for _ , value in unique_y.items():
        lines.append(sorted(value,key=lambda x: (x[1], x[0])))
    return lines


# def guess_table_headers(table):
#     """
#     We're estimating the table headers based on the boldness of the first row of
#     information is not
#     available, we're empirically determining boldness.
#     """
#     headers = []
#     num_rows = len(table)
#     if num_rows == 0 :
#         return None
#     num_cols = len(table[0])
#     if num_rows == 1:
#         return headers
#     max_font_width = {}
#     for row_index, row in enumerate (table):
#         row_words = [x for cell in row for x in cell if x]
#         row_words = sorted (row_words, key=lambda x: (x[1], x[0]))
#         if not row_words:
#             continue
#         sizes = [float(w[2]-w[0])/len(w[-1]) for w in row_words if w[-1]]
#         if not sizes:
#             continue
#         mean_size = np.mean(sizes)
#         max_font_width[row_index] = mean_size
#         first_row_size = max_font_width[0] if 0 in max_font_width else None
#         if first_row_size is None:
#             return headers
#         keys=list(max_font_width.keys())
#         keys.remove(0)
#         other_sizes = max([max_font_width[k] for k in keys])
#         if first_row_size > other_sizes :
#             cells = table[O]
#             for cell in cells:
#                 cell_words =" ".join([w[-1] for w in cell])
#                 headers.append(cell_words)
#         return headers



#segmentation.py
def guess_table_headers(table):
    """
    We're estimating the table headers based on the boldness of the first row of
    information is not
    available, we're empirically determining boldness.
    """
    headers = []
    num_rows = len(table)
    if num_rows == 0 :
        return None
    num_cols = len(table[0])
    if num_rows == 1:
        return headers
    max_font_width = {}
    for row_index, row in enumerate (table):
        row_words = [x for cell in row for x in cell if x]
        row_words = sorted (row_words, key=lambda x: (x[1], x[0]))
        if not row_words:
            continue
        sizes = [float(w[2]-w[0])/len(w[-1]) for w in row_words if w[-1]]
        if not sizes:
            continue
        mean_size = np.mean(sizes)
        max_font_width[row_index] = mean_size
        first_row_size = max_font_width[0] if 0 in max_font_width else None
        if first_row_size is None:
            return headers
        keys=list(max_font_width.keys())
#         keys.remove(0)
        other_sizes = max([max_font_width[k] for k in keys])
        if first_row_size > other_sizes :
            cells = table[O]
            for cell in cells:
                cell_words =" ".join([w[-1] for w in cell])
                headers.append(cell_words)
        return headers



# def make_table(segment_matrix, words, start, stop, label, source_file, page_id, width, height,
# extract_type, table_extract_mode):
#     """
#     "Create a Table using the Table area given from either PDF sourcefile
#     Arguments:
#         segment_matrix : segment_matrix
#         words : words
#         start : Table start y0
#         stop : Table stop y1
#         source_file : PDF sourcefile
#         page_id: page number
#         width: width of the page
#         height : height of the page
#         extract_type : whether to use Tabula or Camelot for table extraction
#     Returns:
#         arranged segments

#     """
#     try:
#         page_number = int(page_id)
#         x1_t = 10
#         X2_t = segment_matrix.shape[1] - 10
#         y1_t = start
#         y2_t= stop
#         bounding_box = [yl_t, xl_t, y2_t, x2_t]
#         if extract_type == "tabula":
#             if table_extract_mode=="stream":
#                 df = read_pdf(source_file, pages = page_number, 
#                             output_format= 'json', multiple_tables=False,
#                             stream = True, options="--silent",
#                             area = bounding_box, guess = False,
#                             silent = True, pandas_options={'header': None})
#             else:
#                 df = read_pdf(source_file, pages = page_number,
#                             output_format= 'json', multiple_tables=False,
#                             lattice = True, options="--silent", 
#                             area=bounding_box, guess = False,
#                             silent = True, pandas_options={"header": None})
#             table_dict=df[0]
#             data_dict = table_dict['data']
#             new_row = []
#             for row in data_dict:
#                 new_column=[]
#                 for cell in row:
#                     text = cell['text']
#                     x1 = cell['left']
#                     x2 = x1 + cell['width']
#                     yl = cell['top']
#                     y2=  yl + cell['height']
#                     font = {'font_name': 'Arial', 'pointsize': 9}
#                     cell_new = [x1, y1, x2, y2, font, text]
#                     new_column.append([cell_new])
#                 new_row.append([new_column])
#             block=[x1_t, y1_t,x2_t,y2_t, label, [], new_row]
#         elif extract_type == "camelot":
#             yl_t, xl_t, y2_t, x2_t = bounding_box
#             xl = xl_t
#             yl = height - yl_t
#             x2 = x2_t
#             y2 = height - y2_t
#             bounding_box_camelot = [xl, yl, X2, y2]
#             bounding_box_camelot = [str(item) for item in bounding_box_camelot]
#             area = ",".join(bounding_box_camelot)
#             tables = camelot.read_pdf(source_file, pages= str(page_id), flavor= table_extract_mode,table_areas=[area])
#             data_dict = tables[0].df_json
#             new_row=[]
#             for row in data_dict:
#                 new_column = []
#                 for cells in row:
#                     cell = cells[0]
#                     text = cell[-1]
#                     x1 = cell[0]
#                     yl = height- cell[3]
#                     x2 = cell [2]
#                     y2 = height - cell[1]
#                     font = cell[4]
#                     cell_new=[x1, y1, x2, y2, font,text]
#                     new_column.append([cell_new] )
#                 new_row.append(new_column)
#             block=[x1_t, y1_t,x2_t,y2_t, label, [], new_row]
#         elif extract_type == "internal":
#             margins = get_segment_margins(segment_matrix)
#             table = make_cells(segment_matrix, margins, words, start, stop)
#             block = None
#             table = split_multiline_cells(table)
#             headers = guess_table_headers(table)
#             words= [x for row in table for cell in row for x in cell if x]
#             words = sorted (words, key=lambda x: (x[1], x[0]))
#             if words:
#                 points = [w[0:4] for w in words]
#                 points = np.array (points)
#                 x_0, y_0 = np.min(points[:, 0:2], axis=0)
#                 x_l, y_1 = np.max (points[:, 2:4], axis=0)
#                 block = [x_0, y_0, x_1, y_1, "TABLE", headers, table]

#         elif extract_type =="vision_logic":
#             table_row_col_detector = DetectTableRowColumns()
#             area = [xl_t, yl_t, x2_t, y2_t]
#             table = table_row_col_detector.get_table(source_file, page_id, [area],words)
#             block = [xl_t, yl_t, x2_t, y2_t, "TABLE", [], table]
#         if not block or block[-1]==[]:
#             return None, None
#         else:
#             isMultiple, block, is_valid= isValidTable(block)
#             if is_valid:
#                 return isMultiple, block
#             else: 
#                 return None ,None
#     except Exception as e:
#         logger.error("Page Number :%s",page_id)
#         logger.error("Table Extraction Type :%s", extract_type)
#         logger.error('Exception occurred during segmentation make_table')
#     return None, None

def make_table(segment_matrix, words, start, stop, label, source_file, page_id, width, height,
extract_type, table_extract_mode):
    """
    "Create a Table using the Table area given from either PDF sourcefile
    Arguments:
        segment_matrix : segment_matrix
        words : words
        start : Table start y0
        stop : Table stop y1
        source_file : PDF sourcefile
        page_id: page number
        width: width of the page
        height : height of the page
        extract_type : whether to use Tabula or Camelot for table extraction
    Returns:
        arranged segments

    """

    page_number = int(page_id)
    x1_t = 10
    x2_t = segment_matrix.shape[1]-10
    y1_t = start
    y2_t= stop
    bounding_box = [y1_t, x1_t, y2_t, x2_t]
    if extract_type == "tabula":
        if table_extract_mode=="stream":
            df = read_pdf(source_file, pages = page_number, 
                        output_format= 'json', multiple_tables=False,
                        stream = True, options="--silent",
                        area = bounding_box, guess = False,
                        silent = True, pandas_options={'header': None})
        else:
            df = read_pdf(source_file, pages = page_number,
                        output_format= 'json', multiple_tables=False,
                        lattice = True, options="--silent", 
                        area=bounding_box, guess = False,
                        silent = True, pandas_options={"header": None})
        table_dict=df[0]
        data_dict = table_dict['data']
        new_row = []
        for row in data_dict:
            new_column=[]
            for cell in row:
                text = cell['text']
                x1 = cell['left']
                x2 = x1 + cell['width']
                yl = cell['top']
                y2=  yl + cell['height']
                font = {'font_name': 'Arial', 'pointsize': 9}
                cell_new = [x1, y1, x2, y2, font, text]
                new_column.append([cell_new])
            new_row.append([new_column])
        block=[x1_t, y1_t,x2_t,y2_t, label, [], new_row]
    elif extract_type == "camelot":
        yl_t, xl_t, y2_t, x2_t = bounding_box
        xl = xl_t
        yl = height - yl_t
        x2 = x2_t
        y2 = height - y2_t
        bounding_box_camelot = [xl, yl, X2, y2]
        bounding_box_camelot = [str(item) for item in bounding_box_camelot]
        area = ",".join(bounding_box_camelot)
        tables = camelot.read_pdf(source_file, pages= str(page_id), flavor= table_extract_mode,table_areas=[area])
        data_dict = tables[0].df_json
        new_row=[]
        for row in data_dict:
            new_column = []
            for cells in row:
                cell = cells[0]
                text = cell[-1]
                x1 = cell[0]
                yl = height- cell[3]
                x2 = cell [2]
                y2 = height - cell[1]
                font = cell[4]
                cell_new=[x1, y1, x2, y2, font,text]
                new_column.append([cell_new] )
            new_row.append(new_column)
        block=[x1_t, y1_t,x2_t,y2_t, label, [], new_row]
    elif extract_type == "internal":
        print('pp')
        margins = get_segment_margins(segment_matrix)
        print('marginsx',margins)

        table = make_cells(segment_matrix, margins, words, start, stop)
        print('tablex',table)

        block = None
        table = split_multiline_cells(table)
        print('tablex_multiline',table)

        headers = guess_table_headers(table)
        print('headersx',headers)

        words= [x for row in table for cell in row for x in cell if x]
        words = sorted (words, key=lambda x: (x[1], x[0]))
        print('wordsx',words)

        if words:
            points = [w[0:4] for w in words]
            points = np.array (points)
            x_0, y_0 = np.min(points[:, 0:2], axis=0)
            x_1, y_1 = np.max (points[:, 2:4], axis=0)
            block = [x_0, y_0, x_1, y_1, "TABLE", headers, table]
            print('blockx',block)


    elif extract_type =="vision_logic":
        table_row_col_detector = DetectTableRowColumns()
        area = [xl_t, yl_t, x2_t, y2_t]
        table = table_row_col_detector.get_table(source_file, page_id, [area],words)
        block = [xl_t, yl_t, x2_t, y2_t, "TABLE", [], table]
    if not block or block[-1]==[]:
        return None, None
    else:
        isMultiple, block, is_valid= isValidTable(block)
        print("isMultiple, block, is_valid",isMultiple, block, is_valid)
        if is_valid:
            return isMultiple, block
        else: 
            return None ,None

# def make_blocks(segments, page_matrix, words, source_file, page_id, use_Tabula,
#     is_page_image, width, height, table_extract_mode = "stream"):
#     blocks=[]
#     for segment in segments:
#         block = {}
#         start, stop, label=segment
#         start= int(start)
#         stop = int(stop)
#         if Label== "TABLE":
#             segment_matrix=page_matrix[start:stop, :]
#             if not is_page_image :
#                 if use_Tabula==1:
#                     extract_type= "tabula"
#                 elif use_Tabula==2:
#                     extract_type="camelot"
#                 else:
#                     extract_type = "internal"
#             else:
#                 if use_Tabula == 1 :
#                     extract_type="vision_logic"
#                 else:
#                     extract_type = "internal"
#             if not source_file.endswith(".pdf"):
#                 extract_type = "internal"
#             isMultiple, block = make_table(segment_matrix, words, start, stop, label, source_file,page_id, width, height, extract_type, table_extract_mode)
#             if block:
#                 block = None
#             if block is None:
#                 block = make_paragraph(words, start, stop)
#                 if block is not None:
#                     blocks.append(block)
#             else:
#                 if isMultiple:
#                     for block_individual in block:
#                         if block_individual is not None and block_individual[-1] != []:
#                             blocks.append(block_individual)
#                 else:
#                     blocks.append (block)
#         else:
#             block = make_paragraph (words, start, stop)
#             if block is not None:
#                 blocks.append(block)
#     return blocks

  
    
    
def make_blocks(segments, page_matrix, words, source_file, page_id, use_Tabula,
    is_page_image, width, height, table_extract_mode = "stream"):
    blocks=[]
    for segment in segments:
        block = {}
        start, stop, label=segment
        start= int(start)
        stop = int(stop)
        if label== "TABLE":
            segment_matrix=page_matrix[start:stop, :]
            if not is_page_image :
                if use_Tabula==1:
                    extract_type= "tabula"
                elif use_Tabula==2:
                    extract_type="camelot"
                else:
                    extract_type = "internal"
            else:
                if use_Tabula == 1 :
                    extract_type="vision_logic"
                else:
                    extract_type = "internal"
            if not source_file.endswith(".pdf"):
                extract_type = "internal"
            isMultiple, block = make_table(segment_matrix, words, start, stop, label, source_file,page_id, width, height, extract_type, table_extract_mode)
            if block==[]:
                block = None
            if block is None:
                block = make_paragraph(words, start, stop)
                if block is not None:
                    blocks.append(block)
            else:
                if isMultiple:
                    for block_individual in block:
                        if block_individual is not None and block_individual[-1] != []:
                            blocks.append(block_individual)
                else:
                    blocks.append(block)
        else:
            block = make_paragraph (words, start, stop)
            if block is not None:
                blocks.append(block)
    return blocks
             
# def isValidTable(block, para_splitting=False):
#     """
#         * Check if Table is valid table or not and return cleaned table with trimed paragraphs
#         Arguments:
#         table
#         Table as List of List
#         Returns:
#         isMultiple : Whether the block contains multiple blocks
#         isvalid : Whether a table is a valid table or not
#         block : Content of the block
#     """

#     xl_t, yl_t, x2_t, y2_t, lable, table_header, table = block
#     data =[[" ".join([word[-1] for word in col]) for col in row] for row in table]
#     data=pd.DataFrame(data)
#     data =data.fillna("")
    
#     if data.shape[1] < 2 or data.shap[0] < 2 :
#         return False, None, False
#     else:
#         lst_col_to_be_dropped =[]
#         for i in range(data.shape [1]):
#             col_item_cnt = len([item for item in data.iloc[:, i].values if item.lstrip().rstrip()!=""])
#             if col_item_cnt < 2 :
#                 lst_col_to_be_dropped.append(i)
#         data = data.drop(columns = lst_col_to_be_dropped)
#         if data.shape[1] < 2 or data.shape[0] < 2 :
#             return False, None, False
#         try:
#             if not para_splitting:
#                 return False, block, True
#             top_rows_cnt = 0
#             bot_rows_cnt=0
#             top_para_segment=None
#             bot_para_segment = None
#             for i in range (data.shape[0]):
#                 if str(data.iloc[i, 0]).lstrip().rstrip()!= "" and str("".join(list(data.iloc[i,1:]))).lstrip().rstrip() == " ":
#                     top_rows_cnt += 1
#                 else:
#                     break

#                 for i in range (data.shape[0] -1 , top_rows_cnt -1):
#                     if str(data.iloc[i, 0]).lstrip().rstrip()!= "" and str(" ".join(list(data.iloc[i,:]))).lstrip().rstrip() == " ":
#                         bot_rows_cnt += 1
#                     else:
#                         break

#                 if top_rows_cnt > 0 or bot_rows_cnt >0:
#                     blocks = []
#                     if top_rows_cnt > 0:
#                         top_para_block =table[: top_rows_cnt]
#                         top_para_block =list(itertools.chain.from_iterable(top_para_block))
#                         top_para_words= [para for para in top_para_block if para[-1].lstrip().rstrip()!=""]
#                         if top_para_words !=[]:
#                             top_para_segment = [int(min([word[0] for word in top_para_words if word[0]!=0])),
#                                                 int(min([word [1] for word in top_para_words if word[1] !=0])),
#                                                 int(max([word[2] for word in top_para_words if word [2] !=0])),
#                                                 int(max([word [3] for word in top_para_words if word [3] !=0]))]

#                             blocks.append([top_para_segment[0], top_para_segment[1]-2 ,top_para_segment[2], top_para_segment[3] + 2, "PARA", None, top_para_words])


#                     if bot_rows_cnt > 0:
#                         bot_para_block = table[ : bot_rows_cnt]
#                         bot_para_block= list(itertools.chain.from_iterable(bot_para_block))
#                         bot_para_block = list(itertools.chain.from_iterable(bot_para_block))
#                         bot_para_words = [para for para in bot_para_block if para[-1].lstrip().rstrip()!=""]

#                         if bot_para_words != []:
#                             bot_para_segment[int(min([word[0] for word in bot_para_words if word[0]!=0])),
#                                             int(min([word[1] for word in bot_para_words if word[1]!=0])),
#                                             int(max([word[2] for word in bot_para_words if word [2]!=0])),
#                                             int(max([word[3] for word in bot_para_words if word[3]!=0]))]

#                             blocks.append( [bot_para_segment[0], bot_para_segment[1]-2,bot_para_segment[2], bot_para_segment[3] + 2, "PARA", None, bot_para_words])
#                     blocks.append( [xl_t, top_para_segment[3] + 2 if top_para_segment else yl_t, x2_t, bot_para_segment[3]-2 if bot_para_segment else y2_t,
#                                 "TABLE", [], table[top_rows_cnt : data.shape[0] - bot_rows_cnt]])
#                     return True, blocks, True
#                 else:
#                     return False, block, True
#         except Exception as e:
#             logger.error('Exception occurred during isMultiple', exc_info=sys.exc_info())
#             return False, block, True



def isValidTable(block, para_splitting=False):
    """
        * Check if Table is valid table or not and return cleaned table with trimed paragraphs
        Arguments:
        table
        Table as List of List
        Returns:
        isMultiple : Whether the block contains multiple blocks
        isvalid : Whether a table is a valid table or not
        block : Content of the block
    """

    x1_t, y1_t, x2_t, y2_t, lable, table_header, table = block
    data =[[" ".join([word[-1] for word in col]) for col in row] for row in table]
    data=pd.DataFrame(data)
    data =data.fillna("")
    
#     if data.shape[1] < 1 or data.shape[0] < 1 :
#         return False, None, False
#     else:
    lst_col_to_be_dropped =[]
    for i in range(data.shape [1]):
        col_item_cnt = len([item for item in data.iloc[:, i].values if item.lstrip().rstrip()!=" "])
        if col_item_cnt < 2 :
            lst_col_to_be_dropped.append(i)
    data = data.drop(columns = lst_col_to_be_dropped)
#         if data.shape[1] < 1 or data.shape[0] < 1 :
#             return False, None, False
    try:
        if not para_splitting:
            return False, block, True
        top_rows_cnt = 0
        bot_rows_cnt=0
        top_para_segment=None
        bot_para_segment = None
        for i in range (data.shape[0]):
            if str(data.iloc[i, 0]).lstrip().rstrip()!= " " and str(" ".join(list(data.iloc[i,1:]))).lstrip().rstrip() == " ":
                top_rows_cnt += 1
            else:
                break

            for i in range (data.shape[0] -1 , top_rows_cnt, -1):
                if str(data.iloc[i, 0]).lstrip().rstrip()!=  " " and str(" ".join(list(data.iloc[i,1:]))).lstrip().rstrip() == " ":
                    bot_rows_cnt += 1
                else:
                    break

            if top_rows_cnt > 0 or bot_rows_cnt >0:
                blocks = []
                if top_rows_cnt > 0:
                    top_para_block =table[: top_rows_cnt]
                    top_para_block =list(itertools.chain.from_iterable(top_para_block))
                    top_para_words= [para for para in top_para_block if para[-1].lstrip().rstrip()!=" "]
                    if top_para_words !=[]:
                        top_para_segment = [int(min([word[0] for word in top_para_words if word[0]!=0])),
                                            int(min([word [1] for word in top_para_words if word[1] !=0])),
                                            int(max([word[2] for word in top_para_words if word [2] !=0])),
                                            int(max([word [3] for word in top_para_words if word [3] !=0]))]

                        blocks.append([top_para_segment[0], top_para_segment[1]-2 ,top_para_segment[2], top_para_segment[3] + 2, "PARA", None, top_para_words])


                if bot_rows_cnt > 0:
                    bot_para_block = table[ : bot_rows_cnt]
                    bot_para_block= list(itertools.chain.from_iterable(bot_para_block))
                    bot_para_block = list(itertools.chain.from_iterable(bot_para_block))
                    bot_para_words = [para for para in bot_para_block if para[-1].lstrip().rstrip()!=" "]

                    if bot_para_words != []:
                        bot_para_segment[int(min([word[0] for word in bot_para_words if word[0]!=0])),
                                        int(min([word[1] for word in bot_para_words if word[1]!=0])),
                                        int(max([word[2] for word in bot_para_words if word [2]!=0])),
                                        int(max([word[3] for word in bot_para_words if word[3]!=0]))]

                        blocks.append( [bot_para_segment[0], bot_para_segment[1]-2,bot_para_segment[2], bot_para_segment[3] + 2, "PARA", None, bot_para_words])
                blocks.append( [xl_t, top_para_segment[3] + 2 if top_para_segment else yl_t, x2_t, bot_para_segment[3]-2 if bot_para_segment else y2_t,
                            "TABLE", [], table[top_rows_cnt : data.shape[0] - bot_rows_cnt]])
                return True, blocks, True
            else:
                print("elsex")
                return False, block, True
    except Exception as e:
        print("exceptionx")
        logger.error('Exception occurred during isMultiple', exc_info=sys.exc_info())
        return False, block, True

