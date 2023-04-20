#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import os
import datetime
import argparse
import json
import pandas as pd
import numpy as np
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__), '..\..')))

from Common.document_preprocessing  import convert_to_json as conv
#import extract_information as extr
#from bson import Objectid
import time
import re
import ast
import logging
logger = logging.getLogger()




import argparse
import glob
import os
import sys
import json
import ast
import pandas
import logging
logger = logging.getLogger()
import datetime
ALLOWED_EXTENSIONS = ["json"]

import spacy
# import compile_defs as cdefs
import time
import re
import ast
import logging
logger = logging.getLogger()
import pandas as pd


# from extractors import document_extractor as extractor
import  kapitus_extract_information as kap_i 



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


    
# try:

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

import spacy
# import compile_defs as cdefs
import time
import re
import ast
import logging
logger = logging.getLogger()
import pandas as pd


#     from  Extractor_service import *
#     from  kapitus_extract_information_1 import *



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




# files=['Zero_Balance_Letter_6415011.json']
# dst='Output'
# defs=['extractors/definition.json']

# data_dir='.'
# file_name='Zero_Balance_Letter_6415011'

model_dir='Model'
model_name='Bert'
overwrite=True
logs_dir='tmp'
dom_model_enabled=False
dom_model_name="v1"
country_code='US'


#         extract_LCDY14.get("qa_model_to_use", "roberta_model")
dom_model_enabled=False
dom_model_name="v1"
# files=['Zero_Balance_Letter_6415011.json']
# dst='Output'
defs=['extractors/definition.json']

data_dir='.'
# file_name='Zero_Balance_Letter_6415011'
model_dir='Model'
model_name='Bert'
overwrite=True
logs_dir='tmp'
country_code='US'
request_id=123
# In[2]:
# except Exception as e:
#     error_response_status={"code":301, "message":"unable to load model"} 
#     response_status={"error":str(e)+" : Unable to load_model" ,"status":error_response_status}    
#     app_log.info(e)

class ProcessException(Exception):
    pass

class ProcessValidation(Exception) :
    pass


# In[3]:


def process_files_kapitus(file_name, file_path, request_id, country_code, mode=0):
    print( 'running convert to json for {}'.format(file_path))
    logger.info('running convert to json for {}'.format(file_path))
    response_dict = None
    input_file=file_name
    output_file=file_path
    print('input_file',input_file)
#     try:
#         print('checking mime type for the request type LCDY14 Entity Extraction')
#         logger.info('checking mime type for the request type LCDY14 Entity Extraction')
#         mime_type=validate.validate_mime_type(file_path, extensions)
#         if mime_type!="success":
#             logger.info('Docuemnt is an unsupported Mime Type.')
#             response_dict = {"status" : STATUS_error, "return_code" : "1005"}
#             raise ProcessValidation

#     except Exception as e:
#         logger.error('Exception during Mime Type valdiation', exc_info=sys.exc_info())
#         raise ProcessException
    logger.info('started processing c2j')
    logger.info('calling process files of convert_to_json for converting into json {}'.format(file_name))
    print('input_file_x',input_file)
    conv.process_file(input_file,output_file)
#         file_name_list = conv(input_file,output_file)
    print('input_file_xx',input_file)
    print('output_file_xx',output_file)
    try:
        logger.info('started processing c2j')
        logger.info('calling process files of convert_to_json for converting into json {}'.format(file_name))
        print('input_file_x',input_file)
        conv.process_file(input_file,output_file)
#         file_name_list = conv(input_file,output_file)
        print('input_file_xx',input_file)
        print('output_file_xx',output_file)


#         file_name_list = [os.path.join(dst, os.path.splitext(x)[0], os.path.splitext(x)[0] + '.json') 
        logger.info('file got converted for the file {}'.format(file_name))
    except Exception as e:
        print('input_file_px',input_file)

        logger.error('Exception occurred convert to json', exc_info=sys.exc_info())
        raise ProcessException
  




    try:
        print('input_file_p',input_file)

        logger.info("processing converted json for entity extraction")
    #         defs_with_path = []
    #         def_with_path = os.path.join(Kapitus_project_config_dir, df)
    #         defs_with_path.append(def_with_path)
    #         _, name,= os. path.splitext(file_name)
        name,_=os.path.splitext(file_name)
        output_modified_name=name + ".json"
        output_modified_name=os.path.basename(output_modified_name)

        kapitus_input_file=os.path.join(file_path, output_modified_name)
        print('kapitus_input_file',kapitus_input_file)
        input_file=[kapitus_input_file]
        final_result=kap_i.process_files(input_file,output_file,defs,data_dir, model_dir,
                              model_name, overwrite, logs_dir, dom_model_enabled, dom_model_name,country_code)
        print('input_file_p',input_file)

    #         final_result=extr.process_files (file_name_list, output_dst, defs_with_path, name)
        logger.info("entity extraction completed successfully")
        return final_result
    except Exception as e:
            logger.error('Exception occurred for entity extraction', exc_info=sys.exc_info())
            raise ProcessException

# process_files_kapitus(file_name, file_path, request_id, country_code, mode=0)
