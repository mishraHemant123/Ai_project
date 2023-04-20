               
import os
import subprocess
import sys
from tesserocr import PyTessBaseAPI, RIL, PSM,OEM, iterate_level
import numpy as np
import logging
logger=logging.getLogger()

class OSD(object):
	def __init__(self, image_file, tessstdata,lang="eng"):
		self.image_file=image_file
		self.tessstdata=tessstdata
		self.lang="eng"
		api=PyTessBaseAPI(path=tessstdata, psm=PSM.OSD_ONLY, lang=self.lang)
		api.SetImageFile(image_file)
		self.api=api

        
        
	def perform_osd(self):
		api=self.api
		osd=api.DetectOrientationScript()
# 		if osd is not None:
# 			orientattion=osd["orient_deg"]
# 			rotation=(360-orientattion) if rotation!=0 else 0
# 		else:
		rotation=0
		return rotation

class OCR(object):
    def __init__(self, image_file, tessstdata, oem_mode, lang="eng", psm_mode=3):
        self.enhance_image(image_file)
        self.deskew_correcton(image_file)
        self.lang=lang
        if oem_mode=="v3":
            oem=OEM.TESSRACT_ONLY
        elif oem_mode=="v4":
            oem=OEM.LSTM_ONLY
        else :
            oem="TESSRACT_LSTM_COMBINED"
        api=PyTessBaseAPI(path=tessstdata, oem=oem, lang=self.lang, psm=psm_mode)
        api.SetImageFile(image_file)
        self.api=api
        boxes = api.GetComponentImages(RIL.TEXTLINE, True)
        print('Found {} textline image components.'.format(len(boxes)))
        print('self;',self.api)
#         api=self.api


    def deskew_correcton(self, image_file,confidence=40):
        cmd=f'convert -deskew {confidence}% {image_file} {image_file}'
        try:
            subprocess.call(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CallledProcessError:
            raise Exception("Image convesion Error during deskew correction")

    def enhance_image(self, image_file):
        cmd=f'textcleaner -g -e normalize -f 25 -o 10 -u -s l - 10 {image_file} {image_file}'
        try:
            subprocess.call(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CallledProcessError:
            raise Exception("Image convesion Error during enhance image correction")
            


    def remove_noise(self , image_file):
        img=cv2.imread(image_file)
        gray=cv2.cvcvtColor(img, cv2.COLOR_BGR2GRAY)
        gray=cv2.thresshold(gray,0, 255, cv2.THRESH_BNARY | cv2.THRESH_OTSU)[1]
        gray=cv2.medianBlur(gray, 3)
        cv2.imrite(image_file, gray)

    def rank_distance(self, lines,word):
        words=[word for _ in range(len(lines))]
        lines=np.array(lines)
        words=np.array(words)
#         print('lines rd:',lines,'words rd :',words)
        lines=np.take(lines, [1,3], axis=1)
        words=np.take(words, [1, 3], axis=1)
        distances=np.power(lines-words, 2)
        distances=np.sum(distances, axis=1).ravel().tolist()
        min_d=np.argmin(distances)
        return min_d
    
    def perform_ocr(self, x_offset=0, y_offset=0, pad_offset=None, scale=None):
        if not scale:
            scale=72/200
            lines=[]
            words=[]
            api=self.api
            api.Recognize()
            
            ri=api.GetIterator()
            level=RIL.TEXTLINE
            for r in iterate_level( ri, level):

                try:
                    line=r.GetUTF8Text(level)

                    bbox=list(r.BoundingBox(level))
                    bbox=[float(b) for b in bbox]
                    bbox=[float(b)*scale for b in bbox]
                    bbox[0]+=x_offset
                    bbox[2] +=x_offset
                    bbox[1] +=y_offset
                    bbox[3] += y_offset
                    if pad_offset is not None:
                        bbox[0]+=pad_offset[0]
                        bbox[1]+=pad_offset[1]
                        bbox[2]+=pad_offset[0]
                        bbox[3]+=pad_offset[1]
                    line=line.rstrip().lstrip()
                    if line:
                        bbox.append(line)
                        lines.append(bbox)
                except Exception as e:
                    pass
            ri=api.GetIterator()
            level=RIL.WORD
            for r in iterate_level(ri, level):
                try:
                    word=r.GetUTF8Text(level)
#                     print('word',word)
                    bbox=list(r.BoundingBox(level))
#                     print('bbox',bbox)
                    font_info=r.WordFontAttributes()
                    bbox=[float(b) for b in bbox]
                    bbox=[float(b)*scale for b in bbox]
                    bbox[0]+=x_offset
                    bbox[2] +=x_offset
                    bbox[1] +=y_offset
                    bbox[3] += y_offset
                    if pad_offset is not None:
                        bbox[0]+=pad_offset[0]
                        bbox[1]+=pad_offset[1]
                        bbox[2]+=pad_offset[0]
                        bbox[3]+=pad_offset[1]
                    word=word.rstrip().lstrip()
                    if word:
                        bbox.append(font_info)
                        bbox.append(word)
                        words.append(bbox)
                except Exception as e:
                    pass
            lines_to_words={}
            lines_boxes=[]
            indices=[]
            for line in lines:
                bbox=line[0:4]
#                 print('line_bbox_line:',line)
#                 print('line_bbox:',bbox)
                lines_boxes.append(bbox)
                lines_to_words[tuple(bbox)]=[]
                for index, word in enumerate(words):
                    if index in indices:
                        continue
                    wbox=word[0:4]
                    if (wbox[0]>=bbox[0] and (wbox[1]>=bbox[1] and (wbox[2]<=bbox[2] and wbox[3]<= bbox[3]))):
                        lines_to_words[tuple(bbox)].append(word)
                        indices.append(index)
            indices=list(set(indices))
            indices.sort()
            for index , word in enumerate(words):
                if index not in indices:
#                     print('word_enum',word)
                    bbox=word[0:4]
                    matching_index=self.rank_distance(lines_boxes, bbox)
                    lines_to_words[tuple(lines_boxes[matching_index])].append(word)
                    indices.append(index)
            words=[]
            for k, v in lines_to_words.items():
                for item in v:
                    item[1]=k[1]
                    item[3]=k[3]
                    words.append(item)
        return words




   

