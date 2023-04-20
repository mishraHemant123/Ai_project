"""
"Convert Documents to JSON
A program to convert documents (PDFs, TIFFs, Word and Excel documents) to a standard
JSON format.
"""
import socket
import os
import sys
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
import argparse
import shutil
import glob
import logging
import datetime
import time
from datetime import datetime
import re
# from processors import pdf, xlsx, word_docx, msg
from processors import pdf, msg

import subprocess
# import logger.logging_config as logging_config
import json
import warnings
warnings.filterwarnings("ignore")
logger = logging.getLogger (__name__)
ALLOWED_EXTENSIONS =["pdf", "doc", "docx","xls", "xlsx", "xlsm", "tiff", "tif","msg"]


# def get_files (src, formats):
# 	"""
# 	"Find files in the source directory matching the allowed or user-selected
# 	extensions
# 	Arguments:
# 	src {str} -- Path to the source directory
# 	formats {list) List of file formats

# 	Returns:
# 	[list]---List of absolute paths to files
# 	"""

# 	files = []
# 	for extension in formats:
# 		ext_files = glob.glob (os.path.join(src, "**/*." + extension), recursive=True)
# 	files += ext_files
	
# 	return files
	
# def process_files (files, dst, oem, overwrite, cleanup,store_results, debug_segmentation, restore_results, flag_merge_table_neighbours = True,flag_merge_consecutive tables= True, auto_detect_table = False, use_Tabula = False,rcnn_model_check_point=None,flag_merge_para_neighbours = True,dom_model_version = "V", table_extract_mode="stream",dpi=300,ocr_language="eng", isOutputHtml= False, isPageImagesRequired=False, psm_mode=3)
# 		"""
# 	""Process files and convert them to JSON.
# 	Arguments:
# 	files {list] List of absolute paths to files
# 	dst {str} Absolute path of output directory
# 	oem {str} OEM Mode to use for Tesseract. Options: 44 (LSTM) or v3 (LEGACY
# 	TESSERACT). Required only for PDF formats.
# 	overwrite {bool} Overwrite existing results. If True, will perform the
# 	entire conversion process from scratch.
# 	cleanup {bool} Cleanup files/directories after conversion.
# 	store_results {bool} Store intermediate results. Useful for debugging or
# 	resuming a process later on.
# 	"""
# 	clean_file_name_list=[]
# 	tessdata = os.path.join(os.path.dirname(__file__),"tessdata")
# 	if tessdata is not None:
# 		if not os.path.exists (tessdata):
# 			raise Exception("Tessdata directory (%s) does not exist." % (tessdata))
# 	if tf_api_url == "";
# 		tf_api_url = "http://" + socket.gethostname() + ":8833 /api/fasterrcnn/predict"
# 	for num, file in enumerate(files, 1)
# 		_, filename=os.path.split(file)
# 		name, ext = os.path.splitext(filename)
# 		ext = ext.lower()
# 	# Sanitize the file name. Replace whitespaces.
# 		clean_name = re.sub ('[^a-zA-Z0-9\.]|\s+', '_' name)
# 		clean_filename = clean_name + ext
# 		clean_file_name_list.append (clean_filename)

# 	# Make the output directory.
# 		output_dir = os. path.join(dst, clean_name)
# 		os.makedirs(output_dir, exist_ok=True)
# 		source_file = os.path.join(output_dir, clean_filename)
# 		shutil.copy2 (file, source_file)
# 		if ext=='.doc':
# 			source_file=convert_doc_to_pdf(source_file)
# 			ext='.pdf'
# 		preprocessing_json_file = os.path.join(output_dir, clean_name + ".json")
# 		logger.info("Processing File: %s %d/%d)", file, num, len(files))
# 		Logger.info("c2j gem mode %s", oem)
# 		logger.info("c2j psm mode %s",psm mode)
	
# 		if ext == ".pdf" or ext.startswith(".tif") or ext == ".gif" or ext.startswith(".jp"):
# 			job = pdf.Processor(source_file, output_dir,tessdata, overwrite, cleanup, oem, psm_mode,store_results,debug_segmentation, restore_results,
# 			flag_merge_table_neighbours,flag_merge_consecutive_tables, auto_detect_table,use_Tabula, rcnn_model_check_point,flag_merge_para_neighbours,
# 			tf_api_url,table_extract_mode, dpi,ocr_language, isPageImagesRequired)
			
# 			job.run()
		
# 		elif ext == ".doc":
# 			job = word_docx.Processor(source_file, output_dir, tessdata, overwrite,cleanup, oem, ocr_language)
# 			job.run()
# 		elif ext == ".msg":
# 			job = msg.Processor(source_file, output_dir, tessdata, overwrite, cleanup,oem)
# 			job.run()

# 		elif ext == ".docx":
# 			job = word_docx.Processor(source_file, output_dir, tessdata, overwrite,cleanup, oem, ocr language, isOutputHtml)
# 			job.run()

# 		elif ext.startswith(".xls"):
# 		job = xlsx.Processor(source_file, output_dir, overwrite, cleanup)
# 		job.run()
		
# 		else:
# 			raise Exception ("Unknown extension (%)" % file)
# 	return clean_file_name_list


# def convert_doc_to_pdf(source_doc_file):
# 	base_dir=os.path.dirname(os.path.realpath(__file__))
# 	unix_script_path = os.path.join(base_dir,"../../unix_scripts/antiword_doc.sh")
# 	_, filename =os.path.split(source_doc_file)
# 	name, ext =os.path.splitext(filename)
# 	name=name+'.pdf"
# 	output_pdf_file=(os.path.join(_, name))
# 	cmd=unix_script_path+'%s %s' %(source_doc_file, output_pdf_file)
# 	process_result=subprocess.run(cmd, shell = True, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
# 	print(process_result.returncode)
# 	if process_result.returncode==0:
# 		return output_pdf_file
# 	else:
# 		raise Exception('Process Failed while converting doc type document to pdf document.')

# def run(src, dst, formats, oem, overwrite, cleanup, store_results, debug_segmentation,restore_results, psm_mode, flag_merge_table_neighbours, flag_merge_consecutive_tables, auto_detect_table
# 		use_Tabula rcnn_model_check_point , flag_merge_para_neighbours,tf_api_url, dom_model_version, table_extract_mode, dpi, ocr_language, isOutputHtml, isPageImagesRequired):

# 		"""
# 		"Process files and convert them to JSON.
# 		Arguments:--files {list] List of absolute paths to files
# 		dst {str} -- Absolute path of output directory
# 		oem {str} -- OEM Mode to use fon Tesseract. Options: 14 (LSTM) or v3 (LEGACY
# 		TESSERACT). Required only for PDF formats.
# 		overwrite {bool) Overwrite existing results. If True, will perform the entire conversion from scratch
# 		cleanup {bool} Cleanup files/directories after conversion.
# 		store_results {bool} Store intermediate results. Useful for debugging or
# 		resuming a process later on.
# 		"""
	

# 	log_file_name = os.path.join(dst, datetime.now().strftime('Convert_to_Json_%H_%M_%S_%d_%m_%Y.log'))
# 	if debug_segmentation:
# 		logging_config.configure_logging (logfile_path = log_file_name, logging_level =logging.DEBUG, print_console = False)
# 	else:
# 		logging_config.configure_logging (logfile_path = log_file_name, logging level =logging.INFO, print console = False)
# 		logger = logging.getLogger(__name__)
# 		src =os.path.abspath(src)
	
# 	if not os.path.exists(src):
# 		raise Exception("Source directory (%) does not exist." %(src))
# 	formats = formats if formats else ALLOWED_EXTENSIONS
# 	overwrite = bool(overwrite)
# 	cleanup = bool(cleanup)
# 	debug_segmentation = bool(debug_segmentation)
# 	store_results =bool(store_results)
# 	restore_results=bool(restore_results)
	
# 	if os.path.isdir(src):
# 		files=get_files(src,formats)
# 	else:
# 	    files=[src]
	
# 	if not files:
# 		raise Exception("Found 0 files in %s" % (src))
# 	dst= os.path.abspath(dst)
# 	os.makedirs(dst, exist_ok=True)
# 	start_time = time.time()
# 	process_files (files, dst,oem, overwrite, cleanup, store_results, debug_segmentation,restore_results,flag_merge_table_neighbours flag_merge_consecutive_tables,auto_detect_table,use_Tabula rcnn_model_check_point flag_merge_para_neighbours,
# 	tf_api_url, dom_model_version, table_extract_mode, dpi, ocr_language, isOutputHtml, is Page ImagesRequired, psm_mode)
# 	stop_time = time.time ()
# 	print ("Total Time:", stop_time - start_time)


# if __name__=__main__
# 	PARSER = argparse. ArgumentParser("Command line arguments for Document Conversion to JSON")
# 	PARSER.add_argument("-s",
# 					"--src",
# 					type=str,
# 					required=True,
# 					dest="src",
# 					help="Source directory of files/Path to a single file
# 	PARSER.add_argument("-d",
# 					"--dst",
# 					type=str,
# 					required=True,
# 					dest="dst",
# 					help="destination directory")
# 	PARSER.add_argument("-f",
# 					"--formats",
# 					nargs="*",
# 					type=str,
# 					choices=["pdf", "tiff", "tif", "xls",
# 					"xlsx", "xlsm", "doc", "docx","msg"],
# 					dest="formats",
# 					help="File formats to process. Leave empty for all formats."
# )

# 	PARSER.add_argument("-oem",
# 		type=str,
# 		dest="oem",
# 		choices=["V4", "V3", "v3+v4"] ,
# 		default="V3",
# 		help="OEM Mode for Tesseract")

# 	PARSER.add_argument("-o",
# 				"--overwrite",
# 				type=int,
# 				choices=[0, 1],
# 				default=0,
# 				dest="overwrite",
# 				help="Overwrite files")
			
# 	PARSER.add_argument("-c"
# 						"--cleanup",
# 						type=int,
# 						choices=[0,1],
# 						default=1
# 						dest="cleanup",
# 						help="Clean up temporary files/directories")
# 	PARSER.add_argument("-st",
# 	"--store_results",
# 	type=int,
# 	choices= [0, 1],
# 	default=0,
# 	dest="store_results",
# 	help="Store intermediate results (useful for debugging)")


# 	PARSER.add_argument("-ds",
# 						"--debug_segmentation",
# 						type=int,
# 						choices=[0, 1],
# 						default=0,
# 						dest="debug_segmentation",
# 						help="Debug segmentation results")
	
# 	PARSER.add_argument("-rst",
# 						"--restore_results",
# 						type=int,
# 						choices=[0, 1],
# 						default=0,
# 						dest="restore_results",
# 						help="Restore intermediate results (useful for debugging)")

# 	PARSER.add_argument("-psm",
# 						type=int,
# 						choices=[0,1,2,3,4,5,6,7,8,9,10,11,12,13],
# 						default=3,
# 						dest="psm_mode",
# 						help="Page segmentation mode for OCR")
	
# 	PARSER.add_argument("-fmtn",
# 						"--flag_merge_table_neighbours",
# 						type=int,
# 						choices= [0,1],
# 						default=1
# 						dest="flag_merge_table_neighbours",
# 						help="flag_merge_table_neighbours"
# 						)
# 	PARSER.add_argument("-fmct",
# 						"--flag_merge_consecutive_tables",
# 						type=int,
# 						choices=[0, 1],
# 						default=1
# 						dest="flag_merge_consecutive_tables",
# 						help="flag_merge_consecutive_tables")

# 	PARSER.add_argument("-att",
# 						"--auto_detect_table",
# 						type=int,
# 						choices=[0, 1, 2],
# 						default=0,
# 						dest="auto_detect_table",
# 						help="Choice to Detect Table. 0: LR/TB Cut \n1: Faster R-CNN Deep Learning Model \n2: Use Of Camelot Library")
	
# 	PARSER.add_argument("-rcnn_model_check_point",
# 						"--rcnn_model_check_point",
# 						type=str,
# 						default="110c2ee8456b",
# 						dest="renn_model_check_point",
# 						help="Check point of Fast R-CNN Model")
	
# 	PARSER.add_argument("-ut"
# 						"--use_Tabula",
# 						type=int,
# 						choices=[0, 1, 2, 3],
# 						default=0),
# 						dest="use_Tabula",
# 						help="Which Table Extraction system ? -- 0 : internal logicUse Tabula , 2: Camelot 3: Computer Visioon")


# 	PARSER.add_argument("-flag merge para neighbours",
# 						"--mar menpe para.netchbours",
# 						type=int,
# 						choices[0, 1]
# 						dest="merge par neighbours",
# 						help=flag merge para neighbours")

# 	PARSER.add argument ("-tau"
# 						"--tf_api_url"
# 						type=str,
# 						default=""
# 						dest="--tf_api_url"
# 						help="")
	
# 	PARSER.add_argument("-domv",
# 						"--dom_model_version",
# 						type=str,
# 						default="v1"
# 						dest="dom_model_version",
# 						help="Version of the document object Model to be used")

# 	PARSER.add_argument("-tem",
# 						"--table_extract_mode",
# 						type=str,
# 						choices=["stream", "lattice"] ,
# 						default="stream",
# 						dest="table_extract_mode",
# 						help="Whether to use stream or lattice mode of Tabula or camelot")


# 	PARSER.add_argument("-dpi",
# 						"--pixel_density_intensity",
# 						type=int,
# 						default=300,
# 						dest="dpi",
# 						help="pixel density intensity for Ghost script")

# 	PARSER.add_argument("-lang",
# 						"--ocr_language",
# 						type=str,
# 						default="eng"
# 						dest="ocr_language"
# 						help="language pack of OCR"
# 						)
						
# 	PARSER.add argument("-html",
# 						"--isOutputHtml",
# 						type=int,
# 						choices=[0, 1],
# 						default=0,
# 						dest="isOutputHtml",
# 						help="get html file as output (only applicable for docx)"
# )
# 	PARSER.add argument("-ipr",
# 						"--isPageImagesRequired",
# 						type=int,
# 						choices=[0, 1],
# 						default=0,
# 						dest="lisPageImagesRequired",
# 						help="If Page Images Required for Traceback")
# 	FLAGS = PARSER.parse_args


# 	run(**vars (FLAGS)


def convert_type(o):
    if isinstance(o, np.int64): return int(o)  
    raise TypeError
def process_file(input_path,output_dir):
    file_name=os.path.splitext(input_path)[-2]
#     file_name=file_name.replace('.pdf','')
    print(file_name)
    tmp_dir='tmp'
    images_dir='tmp'
    source_file=input_path
    output_dir=output_dir
    document,document_data,_=pdf.run(source_file,output_dir, file_name,tmp_dir)
    print("output_dir",output_dir,"file_name")
    filename= os.path.splitext(os.path.basename(file_name))[0]
    json_file=os.path.join("./Output",filename+'.json')
    print('json_file',json_file,"filename",filename)
    json_data=json.dumps(document, default=convert_type)
    with open(json_file, "w") as json_file:
        json_file.write(json_data)
        json_file.close()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
            description='Convert PDF file  notebook to JSON.',
            formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-i', '--input',
                        required=True,
                        help='Path to the PDF file')

    parser.add_argument('-o', '--output',
                        required=True,
                        help='Path to the JSON script file')

    parser.add_argument('-v', '--version',
                        action='version',
                        version='v. 0.1')

    args = parser.parse_args()

#     process_files(input_path=args.input,
#             output_path=os.path.splitext(args.output))

    process_file(args.input,args.output)
