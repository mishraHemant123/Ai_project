#!/usr/bin/env python
# coding: utf-8
#Importing all dependencies


import os


import flask
from flask import Flask, render_template, request ,jsonify

# Library to handle json format
# import simplejson as json

# Library to  maintain logs
import logging
from logging.handlers import RotatingFileHandler
import collections

#error log creation
log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
logFile = 'log.txt'
my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=50*1024*1024,backupCount=25, encoding=None, delay=0)

#error log monitoring
my_handler.setFormatter(log_formatter)
my_handler.setLevel(logging.INFO)
app_log = logging.getLogger('root')
app_log.setLevel(logging.INFO)
app_log.addHandler(my_handler)
app_log.info('------Started----')

app= Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
from kapitus_service import *

try:
    from kapitus_service import *
    country_code='US'
    request_id=123  
#     import argparse
#     import glob
#     import os
#     import sys
#     import json
#     import ast
#     import pandas
#     #from kapitus.extractors import extractor as extractor
#     import logging
#     logger = logging.getLogger()
#     import datetime
#     ALLOWED_EXTENSIONS = ["json"]

#     import spacy
#     import compile_defs as cdefs
#     import time
#     import re
#     import ast
#     import logging
#     logger = logging.getLogger()
#     import pandas as pd


#     from  Extractor_service import *
#     from  kapitus_extract_information_1 import *



#     spacy_model = spacy.load("en_core_web_sm")
#     document = None
#     content = None
#     defs = None
#     num_pages = None
#     toc_pages= None
#     filters = None
#     save_results= False
#     # dom_model_enabled= dom_model_enabled
#     # dom_model_name = dom_model_name
#     remove_key =False #True if remove_key == 1 else False
#     table_merge_for_two_columns = False # Later have to update _ Def= True
#     logger = logger
#     apply_known_ocr_fixes = False # Later have to update _ Def= True
#     ocr_fix_table = False # Later have to update _ Def= True
#     qa_model_to_use = 'bert_model'
#     #         extract_LCDY14.get("qa_model_to_use", "roberta_model")




#     # files=['Zero_Balance_Letter_6415011.json']
#     # dst='Output'
#     defs=['kapitus_defs.json']
#     data_dir='.'
#     # file_name='Zero_Balance_Letter_6415011'

#     model_dir='Model'
#     model_name='Bert'
#     overwrite=False
#     logs_dir='tmp'
#     dom_model_enabled=False
#     dom_model_name="v1"
#     country_code='US'
    

#     #         extract_LCDY14.get("qa_model_to_use", "roberta_model")
#     dom_model_enabled=False
#     dom_model_name="v1"
#     # files=['Zero_Balance_Letter_6415011.json']
#     # dst='Output'
#     defs=['kapitus_defs.json']
#     data_dir='.'
#     # file_name='Zero_Balance_Letter_6415011'
#     model_dir='Model'
#     model_name='Bert'
#     overwrite=False
#     logs_dir='tmp'
#     country_code='US'


except Exception as e:
    error_response_status={"code":301, "message":"unable to load model"} 
    response_status={"error":str(e)+" : Unable to load_model" ,"status":error_response_status}    
    app_log.info(e)
    
    
# setting up API endpoint  for ML model
@app.route('/process_doc', methods=['POST'])
def process_doc():
    try:
    	# validating the type of request
        if request.method=='POST': 
            try:
            	#taking input from the request
                req_data = request.get_json()             
                input_file=req_data["input"] 
                output_file=req_data["output"]                 
            except Exception as e:
                error_response_status={"code":301, "message":"error"} 
                response_status={"error":str(e)+" : Unable to prcoess request ,check format " ,"status":error_response_status}    
                app_log.info(e)
                return jsonify(response_status),301   

            try:
                
#                 convert(input_file,output_file)
#                 _,file_name = os.path.split(input_file)
#                 name,_=os.path.splitext(file_name)
#                 output_modified_name=name + ".json"
#                 kapitus_input_file=os.path.join(output_file, output_modified_name)
#                 print('kapitus_input_file',kapitus_input_file)
#                 input_file=[kapitus_input_file]
#                 extracted_json=process_files(input_file,output_file,defs,data_dir, model_dir,
#                               model_name, overwrite, logs_dir, dom_model_enabled, dom_model_name,country_code)
                print("pp")
                final_result=process_files_kapitus(input_file,output_file ,request_id, country_code,)

                
                # formating  Predcited categories and confidences in JSON Format  
               
                print('extracted_json:',final_result)
                success_response_status={"code":200, "message":"Success"} 
                results={"Output:":final_result,"status":success_response_status}
                # return results to user endpoint
                return jsonify (results),200
            
            except Exception as e:
                error_response_status={"code":301, "message":"error"} 
                response_status={"error":str(e)+" : Unable to predict" ,"status":error_response_status}    
                app_log.info(e)
                return jsonify(response_status),301   
                           
        else:
            error_response_status={"code":301, "message":"use Post method only"} 
            response_status={"error":" : Unable to process get request" ,"status":error_response_status}    
            app_log.info(e)
            return jsonify(response_status),301   
            
    except Exception as e:
        error_response_status={"code":301, "message":"error"} 
        response_status={"error":str(e)+" : Unable to connect" ,"status":error_response_status}    
        app_log.info(e)
        return jsonify(response_status),301   





    

# @app.route('/predict_img', methods=['POST'])
# def predict_img():
#     try:
#         if request.method=='POST': 
#             try:
                 

#                 #read image file string data
#                 filestr = request.files['file']
#                 image_name=filestr.filename
# 				#saving image in server
#                 filestr.save('temp.png')


                
#             except Exception as e:
#                 error_response_status={"code":301, "message":"error"} 
#                 response_status={"error":str(e)+" : Unable to prcoess request ,check format of image " ,"status":error_response_status}    
#                 app_log.info(e)
#                 return jsonify(response_status),301   

#             try:
                
# 				# predictions from  model for image
#                 confidence_list=[]
                
#                 img=open_image('temp.png')                
#                 preds,tensor,probs=CV_image_classification_Model.predict(img)    
                 
                           
#                 classes=CV_image_classification_Model.data.classes
#                 # using small functions to get top 5 predictions with probability             
#                 top_5_predictions,top_5_confidence=top_5_pred_labels(probs,classes)  
                                         
#                 # coverting Probabilites in Confidence for Users 
                                  
#                 predict=str(top_5_predictions)
#                 for i in top_5_confidence:    
#                     i=str(i)
#                     i=i.replace('tensor(','')
#                     i=i.replace(')','')
#                     i=float(i)*100
#                     confidence_list.append(i)
                    
                    
#                 # formating  Predcited categories and confidences in JSON Format                
#                 result=dict(zip(top_5_predictions,confidence_list))    
#                 lists=[]
#                 for u,v in result.items():
#                     dict_temp={"Category":u,"Confidence":v}
#                     lists.append(dict_temp)
                                    
#                 success_response_status={"code":200, "message":"Success"} 
#                 results={"TOP 5 Predicted classes":lists,"status":success_response_status}
#                 # return results to user endpoint
#                 return jsonify (results),200
            
#             except Exception as e:
#                 error_response_status={"code":301, "message":"error"} 
#                 response_status={"error":str(e)+" : Unable to predict" ,"status":error_response_status}    
#                 app_log.info(e)
#                 return jsonify(response_status),301   
                           
#         else:
#             error_response_status={"code":301, "message":"use Post method only"} 
#             response_status={"error":str(e)+" : Unable to process get request" ,"status":error_response_status}    
#             app_log.info(e)
#             return jsonify(response_status),301   
            
#     except Exception as e:
#         error_response_status={"code":301, "message":"error"} 
#         response_status={"error":str(e)+" : Unable to connect" ,"status":error_response_status}    
#         app_log.info(e)
#         return jsonify(response_status),301   

# @app.route('/predict_nlp', methods=['POST'])
# def predict_nlp():
#     try:
#         if request.method=='POST': 
#             try:
#             	#taking input text from the request

#                 req_data = request.get_json()             
#                 input_data=req_data["data"] 
#             except Exception as e:
#                 error_response_status={"code":301, "message":"error"} 
#                 response_status={"error":str(e)+" : Unable to prcoess request ,check format " ,"status":error_response_status}    
#                 app_log.info(e)
#                 return jsonify(response_status),301   

#             try:
#             	# predictions from  model for text
#             	confidence_list=[]            
                
#                 preds,tensor,probs=NLP_model.predict(img)                  
#                 classes=NLP_model.data.classes            
#                 # using small functions to get top 5 predictions with probability    
#                 top_5_predictions,top_5_confidence=top_5_pred_labels(probs,classes)  
                                         
#                 # coverting Probabilites in Confidence for Users                   
#                 predict=str(top_5_predictions)
#                 for i in top_5_confidence:    
#                     i=str(i)
#                     i=i.replace('tensor(','')
#                     i=i.replace(')','')
#                     i=float(i)*100
#                     confidence_list.append(i)
                    
                    
#                 # formating  Predcited categories and confidences in JSON Format                 
#                 result=dict(zip(top_5_predictions,confidence_list))    
#                 lists=[]
#                 for u,v in result.items():
#                     dict_temp={"Category":u,"Confidence":v}
#                     lists.append(dict_temp)
                                    
#                 success_response_status={"code":200, "message":"Success"} 
#                 results={"TOP 5 Predicted classes":lists,"status":success_response_status}
#                 # return results to user endpoint
#                 return jsonify (results),200
            
#             except Exception as e:
#                 error_response_status={"code":301, "message":"error"} 
#                 response_status={"error":str(e)+" : Unable to predict" ,"status":error_response_status}    
#                 app_log.info(e)
#                 return jsonify(response_status),301   
                           
#         else:
#             error_response_status={"code":301, "message":"use Post method only"} 
#             response_status={"error":str(e)+" : Unable to process get request" ,"status":error_response_status}    
#             app_log.info(e)
#             return jsonify(response_status),301   
            
#     except Exception as e:
#         error_response_status={"code":301, "message":"error"} 
#         response_status={"error":str(e)+" : Unable to connect" ,"status":error_response_status}    
#         app_log.info(e)
#         return jsonify(response_status),301    







if __name__ == '__main__':
    app.run(host='0.0.0.0',threaded=True,debug=True)