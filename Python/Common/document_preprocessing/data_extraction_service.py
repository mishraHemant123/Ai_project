#!/usr/bin/env python
# coding: utf-8

# In[1]:


import argparse
import glob
import os
import sys
import json
import ast
import pandas
#from kapitus.extractors import extractor as extractor
import logging
logger = logging.getLogger()
import datetime
ALLOWED_EXTENSIONS = ["json"]
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import spacy
import compile_defs as cdefs
import time
import re
import ast
# from transformers import DistilBertTokenizer, DistilBertForQuestionAnswering
import torch
import pandas as pd
# from data_extractor_1 import *
from extractor import document_extractor as doc_ext


spacy_model = spacy.load("en_core_web_sm")
document = None
content = None
defs = None
num_pages = None
toc_pages= None
filters = None
save_results= False
# dom_model_enabled= dom_model_enabled
# dom_model_name = dom_model_name
remove_key =False #True if remove_key == 1 else False
table_merge_for_two_columns = False # Later have to update _ Def= True
logger = logger
apply_known_ocr_fixes = False # Later have to update _ Def= True
ocr_fix_table = False # Later have to update _ Def= True
qa_model_to_use = 'bert_model'
#         extract_LCDY14.get("qa_model_to_use", "roberta_model")
dom_model_enabled=False
dom_model_name="v1"
# files=['Zero_Balance_Letter_6415011.json']
# dst='Output'
defs=['extractor/definition.json']
data_dir='.'
# file_name='Zero_Balance_Letter_6415011'
model_dir='Model'
model_name='Bert'
overwrite=True
logs_dir='tmp'
dom_model_name=None
country_code='US'


# if qa_model_to_use == "bert_model":
# #     from transformers import AutoTokenizer, AutoModelForMaskedLM

# #     tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

# #     model = AutoModelForMaskedLM.from_pretrained("distilbert-base-uncased")
# #     from transformers import DistilBertTokenizer, DistilBertForQuestionAnswering
# #     import torch
#     try:
#         print("loading models")
#         tokenizer = DistilBertTokenizer.from_pretrained('./models/',return_token_type_ids = True)
#         model = DistilBertForQuestionAnswering.from_pretrained('./models/')
#     except:
#         print("downloading models")

#         tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased',return_token_type_ids = True)
#         model = DistilBertForQuestionAnswering.from_pretrained('distilbert-base-uncased-distilled-squad')
#     ga_model ='bert_model'
# In[2]:



def process_files(files, dst, defs, data_dir, model_dir,
model_name, overwrite, logs_dir, dom_model_enabled, dom_model_name,country_code):
    """
    '[summary]
    Arguments :
    files {[type]} -- [description]
    dst {[type]} -- [description]
    defs {[type]] [description]
    data_dir {[type]] -- [description]
    model_dir {[type]} [description]
    model_name {[type]} [description]
    overwrite {[type]} -- [description]
    country_code{[type]] -- [description]
    """
#     model=Extractor(country_code, data_dir, model_dir, model_name, logs_dir, dom_model_enabled, dom_model_name)
    for file in files:
        print("inside for loop", file)
        extracted_df = pandas.DataFrame()
        _,file_name = os.path.split(file)
        name,_=os.path.splitext(file_name)
        output_modified_name=name + "_modified.xlsx"
        output_path_modified=os.path.join(dst, output_modified_name)
        print('file:',file,'name',name,'output_modified_name',output_modified_name,'output_path_modified',output_path_modified)

        print('defs:',defs)
        for single_def in defs:


            _, defname=os.path.split(single_def)
            def_name,_=os.path.splitext(defname)
            output_name = name +" " + def_name + ".xlsx"
            output_dir=os.path.join(dst, name)
            print('single_def:',single_def)
            single_def=doc_ext.set_defs(single_def)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            output_path = os.path.join(output_dir, output_name)
            logger.info("Output path : {}".format(output_path))
            print('output_path',output_path)
#             if os.path.exists(output_path) and not overwrite:
#                 continue
            print('file',file)

            status,content = doc_ext.set_json(file)

            if not status:
                continue
            logger.info("starting data extraction")
            data_frame = doc_ext.extract(content=content,items=single_def)
            print('data_frame_',data_frame)
            logger.info("primary data extraction completed")
            extracted_df=data_frame
            extracted_df.to_excel(output_path)
            extracted_json=extracted_df.to_dict()
#             final_result=[]
            


            json_file=name+'.json'
            json_data=json.dumps(extracted_json)
            with open(json_file, "w") as json_file:
                json_file.write(json_data)
                json_file.close()
        return extracted_json           



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
            description='Extract Information & Retrieve Answers.',
            formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-i', '--input',nargs='+',
                        required=True,
                        help='List of Json files')

    parser.add_argument('-o', '--output',
                        required=True,
                        help='Path to destination of Output')
#     parser.add_argument('-d', '--defs',nargs='+',
#                     required=True,
#                     help='Path to Config file')

    parser.add_argument('-v', '--version',
                        action='version',
                        version='v. 0.1')

    args = parser.parse_args()

#     process_files(input_path=args.input,
#             output_path=os.path.splitext(args.output))
    process_files(args.input,args.output,defs,data_dir, model_dir,
model_name, overwrite, logs_dir, dom_model_enabled, dom_model_name,country_code)
