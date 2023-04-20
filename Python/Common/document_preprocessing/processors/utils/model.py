import os
import numpy as np
import logging
import sys
logger = logging.getLogger()



class DocumentModel(object):
    def __init__(self):
        self.document = {}


def make_toc (self, toc):
    self.document["TOC"]["isGenerated"]= True
    self.document["TOC"]["tocPageNumbers"] = toc["pages"]
    for item in toc["content"]:
        node ={"txt": item[0],
            "pageNumber": item [1],
            "depth": 0,
            "point":None
            }
    self.document["TOC"]["tocNodes"].append(node)


# def make_cover_page(self, cover_page):
#     self.document["cover_page"]["isGenerated"] = cover_page["cover_page_present"]
#     self.document["cover_page"]["coverPageNumbers"] = cover_page["pages"]


# def make_style(self, item):
#     style = {
#     "font": None,
#     "fontSize": None,
#     "fontColor": None,
#     "bold": false,
#     "italic": False,
#     "strikeout": false,
#     "underline": False
#     }
#     data = item [-2]
#     if data is None:
#         if item[3] and item[1]:
#             style["fontSize"] = int(round( (item[3] - item[1]), 0))
#         return style
#         if "Font_size" in data and data["Font_size"]:
#             style["fontSize"] = int(round(data["Font_size"],0))
#         elif item[3] and item [1]:
#             style["fontSize"] = int(round( (item [3] item[1]),0))
#         elif "font_size" in data:
#             style["fontSize"] = data["font_size"]
#         if "font_name" in data:
#             style["font"] = data["font_name"]

#         if "font_color" in data:
#             style["fontColor"] = data["font_color"]

#         if "bold" in data:
#             style["bold"] = data["bold"]

#         if "italic" in data:
#             style["italic"] = data["italic"]

#         if "strikeout" in data:
#             style["strikeout"] data["strikeout"]

#         if "underline" in data:
#             style["underline"] = data["underline"]
#         return style

def make_style( item):
    style = {
    "font": None,
    "fontSize": None,
    "fontColor": None,
    "bold": False,
    "italic": False,
    "strikeout": False,
    "underline": False
    }
    data = item [-2]
    if data is None:
        if item[3] and item[1]:
            style["fontSize"] = int(round( (item[3] - item[1]), 0))
            return style
    if "Font_size" in data and data["Font_size"]:
        style["fontSize"] = int(round(data["Font_size"],0))
    
    elif item[3] and item [1]:
        style["fontSize"] = int(round( (item [3]-item[1]),0))
    
    elif "font_size" in data:
        style["fontSize"] = data["font_size"]
    if "font_name" in data:
        style["font"] = data["font_name"]

    if "font_color" in data:
        style["fontColor"] = data["font_color"]

    if "bold" in data:
        style["bold"] = data["bold"]

    if "italic" in data:
        style["italic"] = data["italic"]

    if "strikeout" in data:
        style["strikeout"]=data["strikeout"]

    if "underline" in data:
        style["underline"] = data["underline"]
    return style
                          
# def make_paragraph (self, page_segment, content):
#     page_segment["isParagraph"] = True
#     page_segment["paragraph"] = {"words":[]}
#     for item in content:
#         word = {
#         "txt": item[-1],
#         "coordinates":{
#         "fromX": item[0],
#         "fromY": item[1,
#         "toX" :item[2],
#         "toY" :item[3]
#         },
#         "style": self.make_style(item)
#         }
#         page_segment["paragraph"]["words"].append(word)
#     return page_segment
                          
def model_make_paragraph ( page_segment, content):
    page_segment["isParagraph"] = True
    page_segment["paragraph"] = {"words":[]}
#     reorder_segment_text(content)
    for item in content:
        word = {
        "txt": item[-1],
        "coordinates":{
        "fromX": item[0],
        "fromY": item[1],
        "toX" :item[2],
        "toY" :item[3]
        },
                      
        "style": make_style(item)
        }

        page_segment["paragraph"]["words"].append(word)
    return page_segment
def model_make_table(page_segment, content, headers) :
    page_segment["isTable"] = True
    page_segment["table"] ={
                "numRows": len(content),
                "numCols": len(content[0]),
                "headers": headers,
                "cells": []
}
    for row_index, row in enumerate(content):
        for col_index, cell_content in enumerate (row):
            cell = {
            "rowIndex": row_index,
            "colIndex": col_index,
            "coordinates" : get_cell_coordinates(cell_content),
            "words": []
        }
            for cell_word in cell_content:
                word = {
                    "txt": cell_word[-1],
                    "coordinates": {
                    "fromX": cell_word[0],
                    "fromY": cell_word[1],
                    "toX": cell_word[2],
                    "toY": cell_word[3]
            },
                "style": make_style(cell_word)
                }
                cell["words"].append(word)
            page_segment["table"]["cells"].append(cell)
    return page_segment                          
def make_image (self, page_segment, content):
	page_segment["isImage"] = True
	page_segment["image"] = {
		"isGraph": False,
		"isPicture": True,
		"path": content
}
	return page_segment

# def get_cell_coordinates(self, cell_content):
#     try:
#         X0 = 9999
#         y0 = 9999
#         x1 = 0
#         y1 = 0
#         for cell_word in cell_content:
#             x0 = min(x0, cell_word[0])
#             y0= min(y0, cell_word[1])
#             x1 = max(x1, cell_word[2])
#             y1 =max(y1, cell_word[3])
#         return [x0, y0, x1, y1]
#     except:
#         return [None, None, None, None]


            
def get_cell_coordinates(cell_content):
    try:
        x0 = 9999
        y0 = 9999
        x1 = 0
        y1 = 0
        for cell_word in cell_content:
            x0 = min(x0, cell_word[0])
            y0= min(y0, cell_word[1])
            x1 = max(x1, cell_word[2])
            y1 =max(y1, cell_word[3])
        return [x0, y0, x1, y1]
    except:
        return [None, None, None, None]
    S
# def make_table(self, page_segment, content, headers) :
#     page_segment["isTable"] = True
#     page_segment["table"] ={
#                 "numRows": len(content),
#                 "numCols": len(content[0]),
#                 "headers": headers,
#                 "cells": []
# }
#     for row_index, row in enumerate(content):
#         for col_index, cell_content in enumerate (row):
#             cell = {
#             "rowIndex": row_index,
#             "colIndex": col_index,
#             "coordinates" : self.get_cell_coordinates(cell_content),
#             "words": []
#         }
#             for cell_word in cell_content:
#                 word = {
#                     "txt": cell_word[-1],
#                     "coordinates": {
#                     "fromX": cell_word[0],
#                     "fromY": cell_word[1],
#                     "toX": cell_word[2],
#                     "toY": cell_word[3]
#             },
#                 "style": self.make_style(cell_word)
#                 }
#                 cell["words"].append(word)
#             page_segment["table"]["cells"].append(cell)
#     return page_segment
	
# def make_header(self, header):
#     header_segment = {
#     "isParagraph"; True,
#     "isTable": False,
#     "isImage": False,
#     "paragraph": {
#     "words": []
#         }
#     }
#     for item in header:
#         word = {
#         "txt": item[-1],
#         "coordinates": {
#         "fromX": item[0],
#         "fromY": item[1],
#         "tox": item[2],
#         "toY": item[3]
#         "style":self.make_style(item)
#         }
#         header_segment["paragraph"]["words"].append (word)
#     return header_segment


# def make_footer(self, footer):
#     footer_segment = {
#     "isParagraph": True,
#     "isTable": false,
#     "isImage": false,
#     "paragraph": {
#     "words": []
#         }
#     }
#     for item in footer:
#         word = {
#         "txt": item[-1],
#         "coordinates":
#         "fromX": item[0],
#         "from": item[1],
#         "toX": item[2] ,
#         "toY": item [3]
#         },
#         "style": self.make_style (item)
#         }
#         footer_segment["paragraph"]["words"].append(word)
#     return footer_segment

# def make_generic(self, data):
#     self.document["numPages = data["num_pages"] if "num_pages" in data else No
#     self.document["TOC"]={}
#         "isGenerated": false,
#         "tocPageNumbers": [],
#         "tocNodes": []
#     }
#     if "toc" in data:
#         self.make_toc(data["toc"])
#         self.document["cover_page"] = {
#     "isGenerated": false,
#     "coverPageNumbers": [],
#     }
# if "cover_page" in data:
# self.make_cover_page (data["cover_page"])
# self. document["documentPages"] = [] ]
# for page in data["pages"]:
# document_page = {"pageNumber": page['page_number"], "errorFlag": False
# "error": None}
# if "error" in page:
# document_page["error Flag"] True
# document_page["error"] = page("error"]
# self.document["documentPages') .append(document_page)
# continue
# document_page["pageWidth"] = int(page ["width"]) if "width" in page else
# None
# document_page["pageHeight"] = int(page["height"]) if "height" in page e
# None
# document_page["marginLeft"] None
# document_page["marginTop") = None
# document_page["marginRight"] = None
# document_page["marginBottom"] = None
# document_page["pageImageOrientation'] = page["orientation"] if
# "orientation" in page else None
# document_page["isPageImage"] = page["is_page_image"] if "is_page_image"
# page else None
# document_page["pageSegments"] = []
# document_page["pageHeaders"] = []
# document_page["pageFooters'] = []
# boxes = []
# for segment in page["segments"]:
# box = segment["bbox"]
# if box:
# boxes.append(box)
# label = segment["label"]
# content segment["content"]
# headers = segment["headers']
# page_segment = {
# "isParagraph": false,
# "isTable": false,
# "isImage": false,
# "coordinates"
# "fromX": box[0] if box else None,
# "fromy": box[1] if box else None,
# "tox": box[2] if box else None,
# "toY": box[3] if box else None
# if label == "PARA":
# page_segment = self.make_paragraph (page_segment, content)
# elif label == "TABLE":
# page_segment = self.make_table (page_segment, content, headers)
# elif label == "IMAGE":
# page_segment = self.make_image (page_segment, content)
# document_page["pageSegments"].append(page_segment)
# for header in page["headers"] :
# document_page["pageHeaders"].append(self.make_header(header))
# for footer in page["footers"]:
# document_page["pageFooters"].append(self.make_footer (footer))

# if boxes and "width" in page and "height", in page:
# boxes = np.array(boxes).astype (l'int")
# left, top = list(np.min(boxes[:, 0:2), axis=0))
# right, bottom = list(np.max (boxes[:, 2:4], axis=0 ) )
# document_page["marginLeft ] = int(left)
# document_page["marginTop") = int(top)
# document_page["marginRight) = int(page["width"])-int(right)
# document_page["marginBotton'] = int(page["height"])-int(bottom)




def make_generic(document, data):
    document["numPages"] = data["num_pages"] if "num_pages" in data else None
    document["TOC"]={
        "isGenerated": False,
        "tocPageNumbers": [],
        "tocNodes": []
}
    if "toc" in data:
        make_toc(data["toc"])
    
    document["cover_page"] = {
        "isGenerated": False,
        "coverPageNumbers": []
}
    if "cover_page" in data:
        make_cover_page (data["cover_page"])
        
    document["documentPages"] = [] 
    
    for page in data["pages"]:
        document_page = {"pageNumber": page["page_number"], "errorFlag":False,"error": None}
        if "error" in page:
            document_page["errorFlag"]=True
            document_page["error"] = page["error"]
            document["documentPages"].append(document_page)
            continue
        
        if "width" in page and page["width"] is not None :
            document_page["pageWidth"] = int(page ["width"]) if "width" in page else None
        else:
            document_page["pageWidth"]=None
            
        if "height" in page and page["height"] is not None :
             document_page["pageHeight"] = int(page["height"]) if "height" in page else None
        else:
            document_page["pageHeight"]=None
   
        document_page["marginLeft"]=None
        document_page["marginTop"] = None
        document_page["marginRight"] = None
        document_page["marginBottom"] = None
        document_page["pageImageOrientation"] = page["orientation"] if "orientation" in page else None
        document_page["isPageImage"] = page["is_page_image"] if "is_page_image" in page else None
        document_page["pageSegments"] = []
        document_page["pageHeaders"] = []
        document_page["pageFooters"] = []
        boxes = []
        for segment in page["segments"]:
            
#             box = segment["bbox"]
#             box = segment[0:4]
#             if box:
#                 boxes.append(box)
#             label = segment[4]
#             print('label:',len(label),label)
#             headers = str(segment[5])
#             print('headers:',len(headers),headers)
#             content =segment[6]
#             print('content:',len(content),content)
            box = segment["bbox"]
            if box:
                boxes.append(box)
            label = segment["label"]
            content =segment["content"]
            headers = segment["headers"]
#             print('content_',content)
#             content.sort(key=lambda x:x[2])

            page_segment = {
                "isParagraph": False,
                "isTable": False,
                "isImage": False,
                "coordinates":{
                "fromX":box[0] if box else None,
                "fromY":box[1] if box else None,
                "toX":box[2] if box else None,
                "toY":box[3] if box else None,
                }}
            if label == "PARA":
                page_segment = model_make_paragraph(page_segment, content)
            elif label == "TABLE":
                page_segment = model_make_table(page_segment, content, headers)
            elif label == "IMAGE":
                page_segment = make_image(page_segment, content)
               
            document_page["pageSegments"].append(page_segment)
        
#         for header in page["headers"] :
#             document_page["pageHeaders"].append(make_header(header))
#         for footer in page["footers"]:
#             document_page["pageFooters"].append(make_footer (footer))

        if boxes and "width" in page and "height" in page:
            boxes = np.array(boxes).astype("int")
            left, top = list(np.min(boxes[:, 0:2], axis=0))
            right, bottom = list(np.max(boxes[:, 2:4], axis=0))
            document_page["marginLeft"] = int(left)
            document_page["marginTop"] = int(top)
            document_page["marginRight"] = int(page["width"])-int(right)
            document_page["marginBotton"] = int(page["height"])-int(bottom)
        document["documentPages"].append(document_page)


def reorder_segment_text(content):
    for i in range(len(content)):
        if content[i][4] is None:
            temp=content[i]
            content[i]=content[i-1]
            content[i-1]=temp
    i=0
    while i< len(content):
#         print('\n i',i)
        if content[i][4] is None:
            word_len=len(content[i][5])
#             print(len(tex),word_len,tex[i][5],i)
            temp=content[i]
            del content[i]
#             print('move',i+(word_len))
            content.insert(i+(word_len), temp)
            i=i+(word_len+1)
#             print('\n data: ',temp,word_len, i)

        else :
            i=i+1

# def create(self, data, source_file, source_format, error=None):
#     self.document["source_file"] = source_file
#     self.document["source_format"] = source_format
#     self.document["errorFlag"] = False
#     self. document["error"] = None
#     if data is None :
#         self.document["errorflag"] = True
#         self. document["error"] = error
#         return self.document
#     self.make_generic(data)
#     return self.document

def create( data, source_file, source_format, error=None):
    document={}
    document["source_file"] = source_file
    document["source_format"] = source_format
    document["errorFlag"] = False
    document["error"] = None
    if data is None :
        document["errorflag"] = True
        document["error"] = error
        return document
    make_generic(document,data)
    return document
		