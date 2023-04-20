#!/usr/bin/env python
# coding: utf-8

# In[15]:
import spacy
import compile_defs as cdefs
import time
import re
import ast
import logging
logger = logging.getLogger()
import pandas as pd
import json
from transformers import DistilBertTokenizer, DistilBertForQuestionAnswering
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

spacy_model = spacy.load("en_core_web_sm")
document = None
content = None
defs = None
num_pages = None
toc_pages= None
filters = None
save_results= False
dom_model_enabled=False
dom_model_name="v1"
remove_key =False #True if remove_key == 1 else False
table_merge_for_two_columns = False # Later have to update _ Def= True
logger = logger
apply_known_ocr_fixes = False # Later have to update _ Def= True
ocr_fix_table = False # Later have to update _ Def= True
qa_model_to_use = 'bert_model'
#         extract_LCDY14.get("qa_model_to_use", "roberta_model")

if qa_model_to_use == "bert_model":
#     from transformers import AutoTokenizer, AutoModelForMaskedLM

#     tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

#     model = AutoModelForMaskedLM.from_pretrained("distilbert-base-uncased")
    from transformers import DistilBertTokenizer, DistilBertForQuestionAnswering
    import torch
    try:
        print("loading models1")
        tokenizer = DistilBertTokenizer.from_pretrained('./models/',return_token_type_ids = True)
        model = DistilBertForQuestionAnswering.from_pretrained('./models/')
    except:
        print("downloading models1")

        tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased',return_token_type_ids = True)
        model = DistilBertForQuestionAnswering.from_pretrained('distilbert-base-uncased-distilled-squad')
    ga_model ='bert_model'
    
def qa_model_extract(question, context):
    shortword = re.compile(r'\W*\b\w{1,1}\b')
    context=shortword.sub('', context)
    inputs = tokenizer(question, context, add_special_tokens=True, return_tensors="pt")
    input_ids = inputs["input_ids"].tolist()[0] # the list of all indices of words in question + context

    text_tokens = tokenizer.convert_ids_to_tokens(input_ids) # Get the tokens for the question + context
    answer_start_scores, answer_end_scores = model(**inputs).values()

    answer_start = torch.argmax(answer_start_scores)  # Get the most likely beginning of answer with the argmax of the score
    answer_end = torch.argmax(answer_end_scores) + 1  # Get the most likely end of answer with the argmax of the score

    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))

    print(f"Question: {question}")
    print(f"Answer: {answer}")
    return answer
def remove_keyword(name, key, ans):

    ans=ans.replace(key,'')
    return ans
    
class PredictException (Exception):
	pass

# class Extractor (object):

#     def __init__(self, country_code, data_dir, model_dir, model_name, log_dir,dom_model_enabled=False, dom_model_name="v1",
#                  remove_key=0):
#         self.country_code=country_code
#         self.spacy_model = spacy.load("en_core_web_sm")
#         self.document = None
#         self.content = None
#         self.defs = None
#         self.num_pages = None
#         self. toc_pages= None
#         self. filters = None
#         self.save_results= False
#         self.dom_model_enabled= dom_model_enabled
#         self.dom_model_name = dom_model_name
#         self.remove_key =False #True if remove_key == 1 else False
#         self. table_merge_for_two_columns = False # Later have to update _ Def= True
#         self.logger = logger
#         self. apply_known_ocr_fixes = False # Later have to update _ Def= True
#         self.ocr_fix_table = False # Later have to update _ Def= True
#         self.qa_model_to_use = 'bert_model'
# #         extract_LCDY14.get("qa_model_to_use", "roberta_model")

#         if self.qa_model_to_use == "bert_model":
#             from transformers import AutoTokenizer, AutoModelForMaskedLM

#             tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

#             model = AutoModelForMaskedLM.from_pretrained("distilbert-base-uncased")
#             from transformers import DistilBertTokenizer, DistilBertForQuestionAnswering
#             import torch

#             self.tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased',return_token_type_ids = True)
#             self.model = DistilBertForQuestionAnswering.from_pretrained('distilbert-base-uncased-distilled-squad')

        
# #             from Common.entites_extractors.extractors.BERT.evaluate import bert_model
#             self.ga_model ='bert_model'
# #             self.qa_model_service_func = self.call_Bert_predict
        
#     # 	elif self.qa_model_to_use == "roberta_model":
#     # 		from Common.entites_extractors.extractors.ROBERTA. evaluate import roberta_model
#     # 		self.ga_model = roberta_model
#     # 		self.qa_model_service_func =self.caul_roberta_predict

#     # 	elif self.qa_model_to_use == "qanet_model":
#     # 		from Common.entites_extractors.extractors. QANet.evaluate import qa_model
#     # 			self.ga_model = qa_model
#     # 			self.qa_model_service_func = self.call_qanet_predict
#     # 	else:
#     # 		from Common.entites_extractors.extractors.BERT.evaluate import bert_model
#     # 		self.ga_model ='bert_model
#     # 		self.qa_model_service_func = self.call_Bert_predict

def parse_paragraph(paragraph):
    text = []
    for word in paragraph.get("words"):
        text.append(word.get("txt"))
    raw_text = " ".join(text)
    return raw_text
def parse_table(table):
    print("parse_table",table)        
    num_rows = table.get("numRows")
    print("parse_table num_rows",num_rows)        

    num_cols = table.get("numCols")
    print("parse_table num_cols",num_cols)  
    data = [[[] for _ in range(num_cols)] for _ in range (num_rows)]
    for cell in table.get("cells"):
#         print("parse_table cell",cell)  

        row_index = cell.get("rowIndex")
        col_index=cell.get("colIndex")
        text = []
        for word in cell.get("words"):
#             print("parse_table word",word)  

            text.append(word.get("txt"))
        text = " ".join(text)
        data[row_index][col_index] = text
#         print("parse_table text",text)  

        new_data=[]
        for row in data:
#             print("parse_table row",row) 
            row = [x for x in row if x != []]
            cells=[x for x in row if len(x.rstrip().lstrip()) > 0]
#             cells=[i.split(":") for i in cells ]

#             print("parse_table row cells",cells) 
#             try:
#                 for i in cells :
#                     if len(i)==1:                                           
#                         cells=i.split(":")
#                     else:
                        
#             except:
#                 print("error")
            new_data.append(cells)
#             print("parse_table new_data",new_data) 
        lines = [" ".join(row) for row in new_data]

        raw_text = "\n".join([line for line in lines])
#         print("parse_table raw_text",raw_text)  

    return raw_text,new_data

def clean_table(table):
    """
        making more than 2 column table to 2 column table
    """
    try:
        data = pd.DataFrame(table)
        result = combine_drop_val(data.copy())
        table = []
        for i in range(data.shape[0]):
            col = []
            for j in range(data.shape[1]):
                col.append(data.iloc[i, j])
            table.append(col)
        return table
    except:
        return table
    
    
def finetune_table(data):
    num_rows = len(data)
    if num_rows == 0 :
        return data
    num_cols = len(data[0])
    if num_cols != 2 :
        return data

    new_data = []
    for row in range(0, num_rows):
        if row > 0 :
            curr_key = data[row][0]
            if not curr_key:
                prev_value= ''.join((prev_value, data[row][1].strip()))

            else:
                new_data.extend([[prev_key, prev_value ]])
                prey_key = data[row][0].strip ()
                prev_value = data[row][1]. strip ()

        else:
                prev_key = data[row][0].strip()
                prev_value = data[row][1].strip()

        new_data.extend([[prev_key, prev_value ]])
        return new_data

def parse_document(pages):
    content ={}
    for page in pages:
        page_number = int(page.get("pageNumber"))
    raw_text = []
    segments = []
    for segment in page.get("pageSegments"):
        if (segment.get("isParagraph")):
            text = parse_paragraph(segment.get("paragraph"))
            raw_text.append(text)
            para_dict = {"paragraph": text}
            para_dict.update(segment.get("coordinates"))
            segments.append(para_dict)
        elif(segment.get("isTable")):
            text, table = parse_table(segment.get("table"))
            table = clean_table(table)
            raw_text.append(text)
        if table_merge_for_two_columns :
            table = finetune_table(table)
            table_dict ={"table": table}
            table_dict.update(segment.get("coordinates"))
            segments.append(table_dict)
    raw_text= "\n".join(raw_text)
    if apply_known_ocr_fixes:
        raw_text = fix_ocr_issues_in_raw_text(raw_text)
    content["page_number"]={
                "raw_text": raw_text,
                "segments" : segments
            }
    return content
def parse_document(pages):
    content ={}
    raw_text = []
    segments = []
    for page in pages:
        page_number = int(page.get("pageNumber"))

        for segment in page.get("pageSegments"):
            if (segment.get("isParagraph")):
                text = parse_paragraph(segment.get("paragraph"))
                raw_text.append(text)
                para_dict = {"paragraph": text}
                para_dict.update(segment.get("coordinates"))
                segments.append(para_dict)
#                 print("\n parse_document_segment_","page_number_",page_number,"text_",text,"segment_",segment)

            elif(segment.get("isTable")):
                text, table = parse_table(segment.get("table"))
#                 print("isTablex text, table",text, table)
                table = clean_table(table)
#                 print("isTablex clean_table", table)
                raw_text.append(text)
#                 print("isTablex raw_text", raw_text)

#                 print("\n parse_document_segments_t",segment)


                if table_merge_for_two_columns :
                    print("table_merge_for_two_columns",table_merge_for_two_columns)
                    table = finetune_table(table)
                table_dict ={"table": table}
#                 print("table_dictx",table_dict)

                table_dict.update(segment.get("coordinates"))
                segments.append(table_dict)
#                 print("table_dict segments x",segments)

#     raw_text= "\n".join(raw_text)
#     print("table_dict raw_text",raw_text)

    if apply_known_ocr_fixes:
        raw_text = fix_ocr_issues_in_raw_text(raw_text)
    content["page_number"]={
                "raw_text": raw_text,
                "segments" : segments
            }
#     print("\n parse_document_content",content)
#     print("\n parse_document_raw_text",raw_text)
#     print("\n parse_document_segments_",segments)

    return content

def set_json( src):
    
    logger.info("Processing File: %s", src)
    print('src',src)

    document = json.load(open(src))
    if bool(document.get("errorFlag")):
        return False
    print('document',document)
    toc_pages= []
    toc = document.get("TOC")

    if bool(toc.get("isGenerated")):
        toc_pages.extend(toc.get("tocPageNumbers"))

    if dom_model_enabled :
        print('p')
        dom =extract_dom.extract_dom(json_path=src, modelname=dom_model_name)
        num_pages = dom.getNoOfPages()
        content=parse_document_dom(dom)
        logger.info("DOM Model enabled")
    else :
        print('pppp')

        num_pages = document.get("numPages")
        content=parse_document(document.get("documentPages"))
        logger.info("DOM Model disabled")
#     return True,content
    try:
        logger.info("Processing File: %s", src)
        document = json.load(open(src))
        if bool(document.get("errorFlag")):
            return False

        toc_pages= []
        toc = document.get("TOC")
        
        if bool(toc.get("isGenerated")):
            toc_pages.extend(toc.get("tocPageNumbers"))

        if dom_model_enabled :
            dom =extract_dom.extract_dom(json_path=src, modelname=dom_model_name)
            num_pages = dom.getNoOfPages()
            content=parse_document_dom(dom)
            logger.info("DOM Model enabled")
        else :
            num_pages = document.get("numPages")
            content=parse_document(document.get("documentPages"))
            logger.info("DOM Model disabled")
        return True,content

    except Exception as ex:
        return False
    
def set_defs(defs_path):
    logger.info("Setting definitions : %s", defs_path)
    defs = cdefs.run(defs_path)
#     self.defs = defs
    if apply_known_ocr_fixes :
        load_ocr_fix_table()
    return defs


def get_matching_sentence( term, para ):
    if len(para) < 400 :
        return para
        pattern = get_term_pattern( term )
        sentence_list = re.split(r'(?<=[^A-Z])\.\s(?=\D)', para)
        for sentence in sentence_list:
            match = re.findall(pattern, sentence )
            if match:
                return sentence
        return para
    
def extract_question( term, item_def):
    terms = item_def["search"]["terms"]
    questions = item_def["text_extract"]["question"]
    if len(questions )==1:
        return questions [0]
    else:
        term_index = terms.index(term)
        return questions[term_index]
    
def get_context_by_sentence( term, para):
    pattern = get_term_pattern(term)
    matching_sent = []
    sentence_list = re.split(r'(?<=[^A-Z])\.\s(?=\D)', para)
    for sentence in sentence_list:
        match = re.findall(pattern, sentence )
        if match:
            matching_sentence.append(sentence)
        return matching_sentence
    
def extract_from_value(value, text_extract, expects, term, item_def, current_region):
    ans = str(value)
    tokenize_by_sentence = item_def.get("context_by_sentence", False)
    show_context = item_def.get("show_context_for_none", True)
    if text_extract:
        if text_extract["type"] == "SHORT":
            if text_extract["method"] == "QA":
                question = extract_question(term, item_def)
                print('extract_from_value_',value, question, expects, term, item_def, current_region)

                try:
                    if tokenize_by_sentence :
                        value = get_matching_sentence(term, ans)

                    logger.info("Calling local predict {}".format(qa_model_to_use))
                    print('question',question,'value',value)
                    ans=qa_model_extract(question, value)
                    print('questionx',question,'valuex',value)

                    logger.info("Exiting predict of {} ".format(qa_model_to_use))
                    logger.info('{"term" : "%s"}', term)
                    logger.info('{"context":"%s"}', value)
                    logger.info('{"question": "%s"}',question)
                    logger.info('{"answer": %s"}', ans)

                    if ans is None :
                        ans = str(value)
                except Exception as e:
                    pass

    else :
        show_context = item_def.get("show_context_for_none", False )
    
    if expects is None:
        return ans, "search", "text"
    
    keys_patterns = expects ["keys_patterns"] if "keys_patterns" in expects else None
    if keys_patterns is not None and current_region== "keys" and keys_patterns[0] == 'no':
        return ans,"search", "text"
    if ans is None:
        return None
    patterns = expects["patterns"]
    entities = expects["entities"]
    combine_results = expects.get("combine_results", False)
    ignore_text = expects.get("ignore_text", [])
    value_list = []
    if patterns :
        if tokenize_by_sentence :
            sentence_list = get_context_by_sentence(term, ans)
            for pat in patterns:
                for sent in sentence_list :
                    res = re.findall(re.compile(pat, flags=re.IGNORECASE), str(sent))
                    if len(res) != 0:
                        if combine_results :
                            res = list(dict.fromkeys (res))
                            if len(res) == 1 :
                                result = res[0]
                            else :
                                result = ','.join(res[:-1]) + 'and ' + res[-1]
                        else :
                            if type(res[0]) == tuple and len(res[0]) != 0: 
                                result = res[0][0]
                            else :
                                result = res[0]
                        if entities :
                            nlp= spacy_model
                            doc= nlp(result)
                            for ent in doc.ents:
                                if ent.label_ in entities:
                                    return ent, "search", "entity"
                        else:
                            return result, "search", "regex"
    else :
        for pat in patterns:
            res = re.findall(re.compile(pat, flags=re.IGNORECASE), ans)
            if len(res)!= 0:
                if combine_results:
                    res= list(dict.fromkeys (res))

                    if len(res) == 1 :
                        result = res[0]
                    else:
                        result = ','.join(res[:-1]) + 'and' + res[-1]
                else :
                    if type (res[0]) == tuple and len(res[0])!= 0:
                        result = res[0][0]
                    else :
                        result = res[0]
                if entities :
                    nlp = spacy_model
                    doc = nlp(result)
                    for ent in doc.ents:
                        if ent.label_ in entities:
                            return ent, "search","entity"
                else :
                    return result, "search", "regex"

    if entities :
        nlp = spacy_model
        doc= nlp(ans)
        if tokenize_by_sentence :
            for sent in doc.sents :
                pattern = get_term_pattern( term)
                match = re.findall(pattern, str(sent))
                if not match :
                    continue
                for ent in sent.ents:
                    if ent.label in entities:
                        return ent, "search", "entity"
                    else:
                        for ent in doc.ents :
                            if not str(ent).lower().startswith(tuple(ignore_text)) :
                                if ent.label in entities :
                                    if combine_results :
                                        value_list.append( ent )
                                    else :
                                        return ent, "search", "entity"
                        if value_list :
                            return ", ".join(str(value) for value in set(value_list))

    if show_context :
        return ans, "search", "text"
    else :
        return None

def search_text_from_page_and_next( term, page_num, ignore_new_line=False):
    fake_page_count = 100
    page_num= page_num
    pattern=get_term_pattern(term)
    page_and_next_page_raw_text = content[page_num]["raw_text"]
    if ignore_new_line:
        page_and_next_page_raw_text = page_and_next_page_raw_text.replace("\n", " ")
    matches = re.findall(pattern, page_and_next_page_raw_text)

    if not matches:
        next_page_raw_text =""
        if cpage_num + 1 < num_pages:
            cpage_num= cpage_num + 1
            next_page_raw_text = content[cpage_num]["raw_text"]
            ## correct for a c2j fake blank page or with few characters
            if len(next_page_raw_text) < fake_page_count:
                if cpage_num + 1 < num_pages:
                    cpage_num= cpage_num+ 1
                    next_page_raw_text += "\n" + content[cpage_num]["raw_text" ]
        page_and_next_page_raw_text = "\n".join([page_and_next_page_raw_text, next_page_raw_text])
        if ignore_new_line:
            page_and_next_page_raw_text=page_and_next_page_raw_text.replace("\n", " ")
        matches = re.findall(pattern, page_and_next_page_raw_text)
## repeat for third page.
        if not matches:
            next_page_raw_text =""
            if cpage_num + 1 < num_pages:
                cpage_num = cpage_num + 1
                next_page_raw_text = content[cpage_num]["raw_text"]
## correct for a c2j fake blank page or with few characters
                if len(next_page_raw_text)<fake_page_count:
                    if cpage_num + 1 < num_pages:
                        cpage_num= cpage_num + 1
                        next_page_raw_text += "\n" + content[cpage_num]["raw_text"]
            page_and_next_page_raw_text = "\n".join([page_and_next_page_raw_text, next_page_raw_text])
            if ignore_new_line:
                page_and_next_page_raw_text = page_and_next_page_raw_text.replace("\n", " ")
            matches = re.findall(pattern, page_and_next_page_raw_text)
    if not matches:
        return []
    context = matches [0]
    if isinstance(context, tuple):
        context = " ".join(context)
    coordinates = self.estimate_coordinates_for_context_from_text(context, cpage_num)
    match = [{
    "type": "text_from_page_and_next",
    "term": term,
    "paragraph": context,
    "page_num": cpage_num,
    "fromX": coordinates[0],
    "fromY": coordinates [1],
    "toX": coordinates[2],
    "toY": coordinates [3]
    }]
    return match

def search_raw_text( term, raw_text, ignore_new_line):
    pattern = get_term_pattern(term)
    if ignore_new_line :
        clean_text = raw_text.replace("\n", "")
    else :
        clean_text = raw_text
    matches = re.findall(pattern, clean_text)

    if not matches:
        return []
    match = [{
    "type": "row_text",
    "term": term,
    "paragraph": matches[0]
}]
    return match


def search_paragraph( term, paragraph, raw_text):
    pattern = get_term_pattern(term)
    matches = re.findall(pattern, paragraph)
    print("search_paragraph_type",type(term), type(paragraph), type(raw_text))
    if not matches:
        return []
    words = paragraph.split()
    if len(words) < 1:
        print("search_paragraph_type_len_words",type(words), words)

        lines = raw_text.split("\n")
        line_index = None
        if paragraph in lines:
            line_index = lines.index(paragraph)
        if line_index:
            tmp = lines[line_index:line_index+2]
            match = [{
                "type": "paragraph",
                "term": term,
                "paragraph": "\n".join(tmp)
            }]
        else:
            match = [{
            "type": "paragraph",
            "term": term,
            "paragraph": paragraph
            }]
    else:
        match = [{
            "type": "paragraph",
            "term": term,
            "paragraph": paragraph
            }]
    return match


def search_table( term, table, key_values_for_multiple ) :
        matches = []
        pattern = get_term_pattern(term)
        num_rows = len(table)
        for row_index, row in enumerate(table):
            cells = [x for x in row if len(x.rstrip(x.lstrip())) > 0]
            if len(cells) == 2 or len(cells)==3:
                keys_values = []
                key = cells [0]
                if len(cells) == 2 :
                    value = cells[1]
                else :
                    if key_values_for_multiple == "first":
                        value = cells[1]

                    elif key_values_for_multiple == "last":
                        value = cells[2]
                    else :
                        value = "%s|%s"%( cells[1],cells [2] )
                tmp_k = key.split("/")
                tmp_v = value.split("/")
                if len(tmp_k) == len(tmp_v):
                    for idx in range (len(tmp_k)):
                        keys_values.append([tmp_k[idx], tmp_v[idx]])
                
                elif len(tmp_k) > 1 and len(tmp_v) == 1:
                    for idx in range (len(tmp_k)):
                        keys_values.append([tmp_k[idx], tmp_v[0]])

                else:
                    keys_values.append([key, value])

                for key, value in keys_values:
                    match = re.findall(pattern, key)
                    if match:
                        matches.append({
                        "type": "key",
                        "term": term,
                        "key": key,
                        "value": value
                        })
                        continue
                    match = re.findall(pattern, value)
                    if match:
                        matches.append({
                        "type": "value",
                        "term": term,
                        "key" : key,
                        "value": value
                        })
                        continue
            else:
                match = re.findall(pattern, " ".join(cells))
                if not match:
                    continue
                    matches.append({
                    "type": "paragraph",
                    "term": term,
                    "paragraph": " ".join(cells)})
        return match
    
    
def search_single_term(page_num, term,content,search_in_raw_text = False, ignore_new_line =False,
                       search_in_text_from_page_and_next = False, key_values_for_multiple="first"):
    matches = []
#     if page_num not in content:
#         return matches

    if search_in_text_from_page_and_next:
        results = search_text_from_page_and_next(term, page_num, ignore_new_line)
        for result in results:
            result["segment_index"] = 0
            matches.extend(results)
            return matches
        if search_in_raw_text :
            results =  search_raw_text(term,  content[page_num]["raw_text"], ignore_new_line)
            for result in results:
                coordinates= estimate_coordinates_for_context_from_text(result["paragraph"], page_num)
                result["segment_index"] = 0
                result["page_num"]= page_num
                result['fromX']=0
                result['fromY']=0
                result['toX']=0
                result['toY'] = 0
                matches.extend(results)
                return matches
#    for index, segment in enumerate( content[page_num]["segments"]):
    for index, segment in enumerate( content['page_number']["segments"]):
        if "paragraph" in segment:
            results =  search_paragraph(term, segment["paragraph"],  content)

            for result in results:
                result["segment_index"] = index
                result["page_num"] = page_num
                result['fromX'] = segment['fromX']
                result['fromY'] = segment['fromY' ]
                result['toX'] = segment['toX']
                result['toY'] = segment['toY']
            matches.extend (results)
        if "table" in segment:
            results=  search_table(term, segment["table"], key_values_for_multiple)
            for result in results:
                result["segment index"] = index
                result["page_num"]=page_num
                result['fromX' ] = segment['fromX']
                result['fromY'] = segment['from Y']
                result['toX'] = segment['toX']
                result['toY'] = segment['toY']
            matches.extend (results)

    return matches

# Term change to enhance term definitions, to support Lookahead and Lookbehind
# also to enable a more precise targeting of region of the document you like to
# capture as context for QANet or regex search, similar to the functionality of regex pattern sear

def get_term_pattern(term):
    PLA, PLB, NLA, NLB, AA = '(?=', '(?<=', '(?!', '(?<!', '(?:'
    if term.startswith(PLA) or term.startswith(PLB) or term.startswith(NLA) or term.startswith(NLB):
        pattern = re.compile(term, flags=re.IGNORECASE)
    else:
        pattern = re.compile("\\b%s\\b" % term, flags=re.IGNORECASE)
    return pattern

def search_excludes(page_num, exclude):
#     if page_num not in content:
#         return false
    if exclude:
        for exc in exclude:
            pattern = get_term_pattern(exc)
            match = re.findall(pattern, content[page_num]["raw_text"])
            if match:
                return True
    return False

def search_includes ( page_num, include):
#     if page_num not in content:
#         return false
    if include:
        for inc in include:
            pattern = get_term_pattern(inc)
            match = re.findall(pattern, content[page_num]["raw_text"])
            if match:
                return True
    return False


def search_terms(terms, include, exclude, pages_list, content,search_in_raw_text = False,
                 search_in_text_from_page_and_next = False, key_values_for_multiple="first"):
    all_matches = []
    if not pages_list:
        try:
            pages_list=range(num_pages+1)
        except:
            num_pages=0
            pages_list=range(num_pages+1)
        for page_num in pages_list:
            exclude_found = search_excludes(page_num, exclude)
            if exclude_found:
                continue
        for term in terms:
            matches = search_single_term(page_num, term, content,search_in_raw_text, key_values_for_multiple)
            if not matches:
                continue
            context_found = search_includes(page_num, include)
            for match in matches:
                match["context_found"] = context_found
                all_matches.extend(matches)
            return all_matches

def _extract_item(item,content):
    name = item["name"]
    method = item["type"]
    group = item["group"]
    result = {
        "Name": name,
        "Value": None,
        "Type" : None,
        "Method": method,
        "Source": None,
        "Region": None,
        "Page": None,
        "Group": group,
        "Term": None,
        'fromX': None,
        'fromY' : None,
        'toX' : None,
        'toY': None
    }
    pages_list = []
    if "pages" in item and item["pages"] is not None:
        tmp = item["pages"].split("-")
        if len(tmp) == 1:
            pages_list = [int(tmp[0])]
        elif len(tmp)== 2:
            pages_list = range(int(tmp[0]), int(tmp[1]))
    if method == "search":
        terms = item["search"]["terms"]
        include = item["search"]["include"]
        exclude = item["search"]["exclude"]
        regions = item["search"]["regions"]
        key_values_for_multiple =item["search"].get("key_values_for_multiple","first") 
        ignore_new_line = item ["search"].get("ignore_new_line", False )
        expects = item[ "expects"] if "expects" in item else None
        text_extract = item["text_extract"] if "text_extract" in item else None
        matches = search_terms(terms, include, exclude, pages_list,content=content)
    if not matches:
        return result
    matches = sorted(matches, key=lambda x: (-x["context_found"], x["page_num"]))

    if "keys" in regions:
        current_region="keys"
        region_matches =[match for match in matches if match["type"] == "key"]
        for match in region_matches:
            key = match["key"]
            value = match["value"]
            t_extract = dict(text_extract) if text_extract else None
            if t_extract:
                ignore= t_extract["ignore"] if "ignore" in t_extract else None
                if ignore:
                    if "keys" in ignore:
                        t_extract = None
            ret = extract_from_value(" ".join([key, value]), t_extract, expects, match["term"],current_region)
            if ret is not None:
                ans, ans_method, ans_type = ret
                result["Value"]=remove_keyword(name, key, ans)
                result["Method"] = ans_method
                result["Type"]= ans_type
                result["Page"]= match["page_num"]
                result[ "Region"]="key"
                result["Source"]= " ".join([key, value])
                result["Term" ]=match["term"]
                result['fromX'] = match['fromX']
                result['fromY'] = match['fromY']
                result['toX' ]= match['toX']
                result['toY' ] = match['toY']
                return result


    if "values" in regions:
        current_region="values"
        region_matches = [match for match in matches if match["type"] == "value"]
        for match in region_matches:
            key = match[ "key"]
            value = match["value"]
            t_extract = dict(text_extract) if text_extract else None
            if t_extract:
                ignore = t_extract["ignore"] if "ignore" in t_extract else None
                if ignore:
                    if "values" in ignore:
                        t_extract=None
            ret =extract_from_value(value, t_extract, expects, match["term" ], item, current_region)
            if ret is not None:
                ans, ans_method, ans_type = ret
                result["Value"] = remove_keyword(name, key, ans)
                result["Method"] =ans_method
                result["Type"] = ans_type
                result["Page"] = match["page num" ]
                result["Region"] = "values"
                result["Source"] = "".join([key, value])
                result["Term"] = match["term" ]
                result['fromX'] = match['fromX']
                result['fromY'] = match['fromY']
                result['toX'] = match['toX']
                result['toY'] = match['toY']
                return result

    if "paragraphs" in regions:
        current_region="paragraphs"
        region_matches=[match for match in matches if match["type"]=="paragraph"]
        for match in region_matches:
            paragraph = match["paragraph"]
            t_extract = dict(text_extract) if text_extract else None
            if t_extract:
                ignore=t_extract["ignore"] if "ignore" in t_extract else None
                if ignore:
                    if "paragraphs" in ignore:
                        t_extract=None
            ret = extract_from_value(paragraph, t_extract, expects, match["term"], item,current_region)
            if ret is not None:
                ans, ans_method, ans_type = ret
#                 print('namex',name,'matchx', match["term" ],'ansx', ans)
                print('matchx',match)
                result["Value"]= remove_keyword(name, match["term" ], ans)
                result[ "Method"] = ans_method
                result["Type"] = ans_type
                result["Page"]=match["page_num" ]
                result["Region"]= ["paragraph"]
                result["Source"]= ''.join(paragraph)
                result["Term"]=match["term" ]
                result['fromX']=match[ 'fromX']
                result['fromY']=match['fromY' ]
                result['toX'] = match['toX']
                result['toY'] = match[ 'toY']
                return result

    if "raw_text" in regions:
        current_region="raw_text"
        region_matches = [match for match in matches if match["type"]=="raw_text"]
        for match in region_matches:
            paragraph = match["paragraph" ]
            t_extract = dict(text_extract) if text_extract else None
            if t_extract:
                ignore = t_extract["ignore"] if "ignore" in t_extract else None
                if ignore:
                    if "raw_text" in ignore:
                        t_extract = None
            ret = extract_from_value(paragraph, t_extract, expects, match["term"],current_region)
            if ret is not None:
                ans, ans_method, ans_type = ret
                result["Value"] =remove_keyword(name, match["term"], ans)
                result["Method"]= ans_method
                result["Type"] = ans_type
                result["Page" ]= match["page_num" ]
                result["Region"] = current_region
                result["Source"]= paragraph
                result["Term"] =match["term" ]
                result["Term" ] =match["term" ]
                result['fromX'] = match['fromX']
                result['fromY']= match['fromY']
                result['toX'] =match['toX']
                result['toY'] = match['toY']
                return result
            else:
                result["Page"] = match["page_num"]
                result["Region"] =current_region
                result[ "Source"] = paragraph
                result["Term"] = match["term"]
                return result

    if "text_from_page_and_next" in regions :
        current_region="text_from_page_and_next"
        region_matches = [match for match in matches if match["type"] == "text_from_page_and_next"]
        for match in region_matches:
            paragraph = match["paragraph"]
            t_extract = dict(text_extract) if text_extract else None
            if t_extract:
                ignore = t_extract["ignore"] if "ignore" in t_extract else None
                if ignore:
                    if "text_from_page_and_next" in ignore:
                        t_extract=None
            ret = extract_from_value(paragraph, t_extract, expects, match["term"],current_region)
            if ret is not None :
                ans, ans_method, ans_type = ret
                result["Value"] = remove_keyword(name, match["term"], ans)
                result["Method"] = ans_method
                result["Type"] = ans_type
                result["Page"] = match["page_num"]
                result["Region"] = ["paragraph"]
                result["Source"]=paragraph
                result['Term']= match["term" ]
                result['fromX'] = match['fromX']
                result['fromY'] = match['fromY']
                result['toX'] = match['toX']
                result['toY'] = match['toY']
                return result
            else:
                result["Page"] = match["page_num" ]
                result["Region"] = current_region
                result["Source"] = paragraph
                result["Term"] = match["term" ]
                return result



    elif method == "lookup":
        ans_page = None
        terms = item["search"]["terms"]
        include = item ["search"]["include"]
        exclude = item["search"]["exclude"]
        matches = search_terms(terms, include, exclude, pages_list,content=content)
        if matches:
            ans = item["values"][0]
            ans_page = matches[0]["page_num"]
            result['fromX'] = matches[0]['fromX']
            result['fromY'] = matches[0]['fromy']
            result['toX'] = matches [0]['toX']
            result['toY'] = matches[0]['toY']
        else:
            ans = item["values"][1]
        result["Value"] = ans
        result["Page"] = ans_page
        result["Method"] = "lookup"
        return result
    elif method == "regex":
        ans_page = None
        patterns=item["patterns"]
        ret = find_regex_pattern(patterns, pages_list)
        if ret is not None:
            ans_page = ret[0]
            ans = ret[1]
        else:
            ans = None
        result["Value"] =ans
        result["Page"]=ans_page
        result["Method"] = "regex"
        return result
def extract(content, items=[]):
#     defs = defs
#     filters = self.filters
#     if defs is None:
        
#         return None
    data_frame = pd.DataFrame(columns=["Name", "Value", "Type", "Method", "Region", "Source", "Page", "Group","coordinates"])

    for item in items:
#         if len(items) > 0 and item['name'] not in items :
#             continue
        result = _extract_item(item,content=content)
        if result["Value"] :
            if result["Region"] in ["paragraph", "raw_text", "text_from_page_and_next"] :

                cordinates=get_cordinates_for_value_from_context(result["Page"], result["Source"],results["Value"])
                if cordinates == (0, 0, 0, 0):
                    result['Coordinates']= dict({ "fromX": result['fromX'], "fromY": result['fromY'],"toX":result['toX'],"toY":result['toY']})
                else :

                    result['Coordinates']= dict({"fromX": cordinates[0], "fromY":cordinates[1], "toX":cordinates [3] })


            else:
                result['Coordinates']= dict({ "fromX": result['fromX'], "fromY": result['fromY'],"toX":result['toX'],"toY":result['toY']})
        else :
            result["Coordinates"]= dict({"fromX": None, "fromY": None, "toX": None, "toY": None })
            result.pop('fromX')
            result.pop('fromY')
            result.pop('toX')
            result.pop('toY')
        entity_name, def_type =item['name'], item['type']
        if def_type=='search':
            method = "qanet" if item.get("text_extract") else 'regex'
        else:
            method = def_type
#     if not filters or filters.get(entity_name) == method : ## or not filters.get(entity_name)
        data_frame=data_frame.append(result, ignore_index=True)
        if save_results :
            store_results(data_frame)
    return data_frame


#Added 
def extract_from_value(value, text_extract, expects, term, item_def, current_region):
    ans = str(value)
    print('extract_from_value_','value',value,'text_extract',text_extract,'expects',expects,'term',term,'item_def',item_def,'current_region', current_region)

    tokenize_by_sentence = item_def.get("context_by_sentence", False)
    show_context = item_def.get("show_context_for_none", True)
    if text_extract:
        if text_extract["type"] == "SHORT":
            if text_extract["method"] == "QA":
                question = extract_question(term, item_def)
                print('extract_from_value_','value',value,'question',question,'expects',expects,'term',term,'item_def',item_def,'current_region', current_region)

                try:
                    if tokenize_by_sentence :
                        value = get_matching_sentence(term, ans)

                    logger.info("Calling local predict {}".format(qa_model_to_use))
                    ans=qa_model_extract(question, value)
                    print('questionx',question,'valuex',value)

                    logger.info("Exiting predict of {} ".format(qa_model_to_use))
                    logger.info('{"term" : "%s"}', term)
                    logger.info('{"context":"%s"}', value)
                    logger.info('{"question": "%s"}',question)
                    logger.info('{"answer": %s"}', ans)

                    if ans is None :
                        ans = str(value)
                except Exception as e:
                    pass

    else :
        show_context = item_def.get("show_context_for_none", False )
    
    if expects is None:
        return ans, "search", "text"
    
    keys_patterns = expects ["keys_patterns"] if "keys_patterns" in expects else None
    if keys_patterns is not None and current_region== "keys" and keys_patterns[0] == "no":
        return ans,"search", "text"
    if ans is None:
        return None
    patterns = expects["patterns"]
    entities = expects["entities"]
    combine_results = expects.get("combine_results", False)
    ignore_text = expects.get("ignore_text", [])
    value_list = []
    if patterns :
        if tokenize_by_sentence :
            sentence_list = get_context_by_sentence(term, ans)
            for pat in patterns:
                for sent in sentence_list :
                    res = re.findall(re.compile(pat, flags=re.IGNORECASE), str(sent))
                    if len(res) != 0:
                        if combine_results :
                            res = list(dict.fromkeys (res))
                            if len(res) == 1 :
                                result = res[0]
                            else :
                                result = ','.join(res[:-1]) + 'and ' + res[-1]
                        else :
                            if type(res[0]) == tuple and len(res[0]) != 0: 
                                result = res[0][0]
                            else :
                                result = res[0]
                        if entities :
                            nlp= spacy_model
                            doc= nlp(result)
                            for ent in doc.ents:
                                if ent.label_ in entities:
                                    return ent, "search", "entity"
                        else:
                            return result, "search", "regex"
    else :
        for pat in patterns:
            res = re.findall(re.compile(pat, flags=re.IGNORECASE), ans)
            if len(res)!= 0:
                if combine_results:
                    res= list(dict.fromkeys (res))

                    if len(res) == 1 :
                        result = res[0]
                    else:
                        result = ','.join(res[:-1]) + 'and' + res[-1]
                else :
                    if type (res[0]) == tuple and len(res[0])!= 0:
                        result = res[0][0]
                    else :
                        result = res[0]
                if entities :
                    nlp = spacy_model
                    doc = nlp(result)
                    for ent in doc.ents:
                        if ent.label_ in entities:
                            return ent, "search","entity"
                else :
                    return result, "search", "regex"

    if entities :
        nlp = spacy_model
        doc= nlp(ans)
        if tokenize_by_sentence :
            for sent in doc.sents :
                pattern = get_term_pattern( term)
                match = re.findall(pattern, str(sent))
                if not match :
                    continue
                for ent in sent.ents:
                    if ent.label in entities:
                        return ent, "search", "entity"
                    else:
                        for ent in doc.ents :
                            if not str(ent).lower().startswith(tuple(ignore_text)) :
                                if ent.label in entities :
                                    if combine_results :
                                        value_list.append( ent )
                                    else :
                                        return ent, "search", "entity"
                        if value_list :
                            return ", ".join(str(value) for value in set(value_list))

    if show_context :
        return ans, "search", "text"
    else :
        return None
def search_single_term(page_num, term,content,search_in_raw_text = False, ignore_new_line =False,
                       search_in_text_from_page_and_next = False, key_values_for_multiple="first"):
    matches = []
#     if page_num not in content:
#         return matches

    if search_in_text_from_page_and_next:
        results = search_text_from_page_and_next(term, page_num, ignore_new_line)
        for result in results:
            result["segment_index"] = 0
            matches.extend(results)
            return matches
        if search_in_raw_text :
            results =  search_raw_text(term,  content[page_num]["raw_text"], ignore_new_line)
            for result in results:
                print('search_single_term_','results',results)
                coordinates= estimate_coordinates_for_context_from_text(result["paragraph"], page_num)
                result["segment_index"] = 0
                result["page_num"]= page_num
                result['fromX']=0
                result['fromY']=0
                result['toX']=0
                result['toY'] = 0
                matches.extend(results)
                return matches
#    for index, segment in enumerate( content[page_num]["segments"]):
    for index, segment in enumerate( content['page_number']["segments"]):
        print(" content['page_number'segments", content['page_number']["segments"])
        print("indexes",index,'results_paragraph',segment)
        if "paragraph" in segment:
            results =  search_paragraph(term, segment["paragraph"],  content)
            print('search_single_term_paragraph','results',results)
            for result in results:
                result["segment_index"] = index
                result["page_num"] = page_num
                result['fromX'] = segment['fromX']
                result['fromY'] = segment['fromY' ]
                result['toX'] = segment['toX']
                result['toY'] = segment['toY']
            matches.extend (results)
        if "table" in segment:
            print("indexes_table",index,'results_table',segment)
            results=  search_table(term, segment["table"], key_values_for_multiple)
            print('search_single_term_table','results',results)

            for result in results:
                result["segment index"] = index
                result["page_num"]=page_num
                result['fromX' ] = segment['fromX']
                result['fromY'] = segment['fromY']
                result['toX'] = segment['toX']
                result['toY'] = segment['toY']
            matches.extend (results)

    return matches

def search_table( term, table, key_values_for_multiple ) :

    matches = []
    pattern = get_term_pattern(term)
    num_rows = len(table)
    for row_index, row in enumerate(table):
        print("search_table_row_x",row,len(row)) 

        cells = [x for x in row if len(x.rstrip().lstrip())> 0]
        print("search_table_cells_x",cells,len(cells)) 
        if len(cells) == 2 or len(cells)==3:
            keys_values = []
            key = cells [0]
            if len(cells) == 2 :
                value = cells[1]
            else :
                if key_values_for_multiple == "first":
                    value = cells[1]

                elif key_values_for_multiple == "last":
                    value = cells[2]
                else :
                    value = "%s|%s"%( cells[1],cells [2] )
            print("search_table_cells_x_k",key)
            print("search_table_cells_x_v",value)
            tmp_k = key.split("/")
            tmp_v = value.split("/")
            print("search_table_cells_x__",tmp_k,tmp_v)

            if len(tmp_k) == len(tmp_v):
                for idx in range (len(tmp_k)):
                    keys_values.append([tmp_k[idx], tmp_v[idx]])

            elif len(tmp_k) > 1 and len(tmp_v) == 1:
                for idx in range (len(tmp_k)):
                    keys_values.append([tmp_k[idx], tmp_v[0]])
            else:
                keys_values.append([key, value])
            print("search_table_cells_x__x",keys_values)

            for key, value in keys_values:
                match = re.findall(pattern, key)
                print("search_table_cells_x__y",match,matches)

                if match:
                    matches.append({
                    "type": "key",
                    "term": term,
                    "key": key,
                    "value": value
                    })
                    continue
                match = re.findall(pattern, value)
                if match:
                    matches.append({
                    "type": "value",
                    "term": term,
                    "key" : key,
                    "value": value
                    })
                    continue
                print("search_table_cells_x__z",match,matches)

        else:
            match = re.findall(pattern, " ".join(cells))
            if not match:
                continue
                matches.append({
                "type": "paragraph",
                "term": term,
                "paragraph": " ".join(cells)})
    return matches


def _extract_item(item,content):
    print("_extract_item_content_",content)

    name = item["name"]
    method = item["type"]
    group = item["group"]
    result = {
        "Name": name,
        "Value": None,
        "Type" : None,
        "Method": method,
        "Source": None,
        "Region": None,
        "Page": None,
        "Group": group,
        "Term": None,
        'fromX': None,
        'fromY' : None,
        'toX' : None,
        'toY': None
    }
    pages_list = []
    if "pages" in item and item["pages"] is not None:
        tmp = item["pages"].split("-")
        if len(tmp) == 1:
            pages_list = [int(tmp[0])]
        elif len(tmp)== 2:
            pages_list = range(int(tmp[0]), int(tmp[1]))
    if method == "search":
        print('pages_list_',pages_list)
        terms = item["search"]["terms"]
        include = item["search"]["include"]
        exclude = item["search"]["exclude"]
        regions = item["search"]["regions"]
        key_values_for_multiple =item["search"].get("key_values_for_multiple","first") 
        ignore_new_line = item ["search"].get("ignore_new_line", False )
        expects = item[ "expects"] if "expects" in item else None
        text_extract = item["text_extract"] if "text_extract" in item else None
        matches = search_terms(terms, include, exclude, pages_list,content=content)
        print('matchesx',matches)
    if not matches:
        return result
    matches = sorted(matches, key=lambda x: (-x["context_found"], x["page_num"]))

    if "keys" in regions:
        current_region="keys"
        region_matches =[match for match in matches if match["type"] == "key"]
        for match in region_matches:
            key = match["key"]
            value = match["value"]
            t_extract = dict(text_extract) if text_extract else None
            if t_extract:
                ignore= t_extract["ignore"] if "ignore" in t_extract else None
                if ignore:
                    if "keys" in ignore:
                        t_extract = None
            ret = extract_from_value(" ".join([key, value]), t_extract, expects, match["term"],item,current_region)
            if ret is not None:
                ans, ans_method, ans_type = ret
                result["Value"]=remove_keyword(name, key, ans)
                result["Method"] = ans_method
                result["Type"]= ans_type
                result["Page"]= match["page_num"]
                result[ "Region"]="key"
                result["Source"]= " ".join([key, value])
                result["Term" ]=match["term"]
                result['fromX'] = match['fromX']
                result['fromY'] = match['fromY']
                result['toX' ]= match['toX']
                result['toY' ] = match['toY']
                return result


    if "values" in regions:
        current_region="values"
        region_matches = [match for match in matches if match["type"] == "value"]
        for match in region_matches:
            key = match[ "key"]
            value = match["value"]
            t_extract = dict(text_extract) if text_extract else None
            if t_extract:
                ignore = t_extract["ignore"] if "ignore" in t_extract else None
                if ignore:
                    if "values" in ignore:
                        t_extract=None
            ret =extract_from_value(value, t_extract, expects, match["term" ], item, current_region)
            if ret is not None:
                ans, ans_method, ans_type = ret
                result["Value"] = remove_keyword(name, key, ans)
                result["Method"] =ans_method
                result["Type"] = ans_type
                result["Page"] = match["page num" ]
                result["Region"] = "values"
                result["Source"] = "".join([key, value])
                result["Term"] = match["term" ]
                result['fromX'] = match['fromX']
                result['fromY'] = match['fromY']
                result['toX'] = match['toX']
                result['toY'] = match['toY']
                return result

    if "paragraphs" in regions:
        current_region="paragraphs"
        print('para_matches',matches)
        region_matches=[match for match in matches if match["type"]=="paragraph"]
        for match in region_matches:
            paragraph = match["paragraph"]
            t_extract = dict(text_extract) if text_extract else None
            if t_extract:
                ignore=t_extract["ignore"] if "ignore" in t_extract else None
                if ignore:
                    if "paragraphs" in ignore:
                        t_extract=None
            ret = extract_from_value(paragraph, t_extract, expects, match["term"], item,current_region)
            if ret is not None:
                ans, ans_method, ans_type = ret
#                 print('namex',name,'matchx', match["term" ],'ansx', ans)
                print('matchx',match)
                result["Value"]= remove_keyword(name, match["term" ], ans)
                result[ "Method"] = ans_method
                result["Type"] = ans_type
                result["Page"]=match["page_num" ]
                result["Region"]= ["paragraph"]
                result["Source"]= ''.join(paragraph)
                result["Term"]=match["term" ]
                result['fromX']=match[ 'fromX']
                result['fromY']=match['fromY' ]
                result['toX'] = match['toX']
                result['toY'] = match[ 'toY']
                return result

    if "raw_text" in regions:
        current_region="raw_text"
        region_matches = [match for match in matches if match["type"]=="raw_text"]
        for match in region_matches:
            paragraph = match["paragraph" ]
            t_extract = dict(text_extract) if text_extract else None
            if t_extract:
                ignore = t_extract["ignore"] if "ignore" in t_extract else None
                if ignore:
                    if "raw_text" in ignore:
                        t_extract = None
            ret = extract_from_value(paragraph, t_extract, expects, match["term"],current_region)
            if ret is not None:
                ans, ans_method, ans_type = ret
                result["Value"] =remove_keyword(name, match["term"], ans)
                result["Method"]= ans_method
                result["Type"] = ans_type
                result["Page" ]= match["page_num" ]
                result["Region"] = current_region
                result["Source"]= paragraph
                result["Term"] =match["term" ]
                result["Term" ] =match["term" ]
                result['fromX'] = match['fromX']
                result['fromY']= match['fromY']
                result['toX'] =match['toX']
                result['toY'] = match['toY']
                return result
            else:
                result["Page"] = match["page_num"]
                result["Region"] =current_region
                result[ "Source"] = paragraph
                result["Term"] = match["term"]
                return result

    if "text_from_page_and_next" in regions :
        current_region="text_from_page_and_next"
        region_matches = [match for match in matches if match["type"] == "text_from_page_and_next"]
        for match in region_matches:
            paragraph = match["paragraph"]
            t_extract = dict(text_extract) if text_extract else None
            if t_extract:
                ignore = t_extract["ignore"] if "ignore" in t_extract else None
                if ignore:
                    if "text_from_page_and_next" in ignore:
                        t_extract=None
            ret = extract_from_value(paragraph, t_extract, expects, match["term"],current_region)
            if ret is not None :
                ans, ans_method, ans_type = ret
                result["Value"] = remove_keyword(name, match["term"], ans)
                result["Method"] = ans_method
                result["Type"] = ans_type
                result["Page"] = match["page_num"]
                result["Region"] = ["paragraph"]
                result["Source"]=paragraph
                result['Term']= match["term" ]
                result['fromX'] = match['fromX']
                result['fromY'] = match['fromY']
                result['toX'] = match['toX']
                result['toY'] = match['toY']
                return result
            else:
                result["Page"] = match["page_num" ]
                result["Region"] = current_region
                result["Source"] = paragraph
                result["Term"] = match["term" ]
                return result



    elif method == "lookup":
        ans_page = None
        terms = item["search"]["terms"]
        include = item ["search"]["include"]
        exclude = item["search"]["exclude"]
        matches = search_terms(terms, include, exclude, pages_list,content=content)
        if matches:
            ans = item["values"][0]
            ans_page = matches[0]["page_num"]
            result['fromX'] = matches[0]['fromX']
            result['fromY'] = matches[0]['fromy']
            result['toX'] = matches [0]['toX']
            result['toY'] = matches[0]['toY']
        else:
            ans = item["values"][1]
        result["Value"] = ans
        result["Page"] = ans_page
        result["Method"] = "lookup"
        return result
    elif method == "regex":
        ans_page = None
        patterns=item["patterns"]
        ret = find_regex_pattern(patterns, pages_list)
        if ret is not None:
            ans_page = ret[0]
            ans = ret[1]
        else:
            ans = None
        result["Value"] =ans
        result["Page"]=ans_page
        result["Method"] = "regex"
        return result
    
    
def extract(content, items=[]):
#     defs = defs
#     filters = self.filters
#     if defs is None:
        
#         return None
    data_frame = pd.DataFrame(columns=["Name", "Value", "Type", "Method", "Region", "Source", "Page", "Group","coordinates"])

    for item in items:
#         if len(items) > 0 and item['name'] not in items :
#             continue
        print("extract_content_",content,"extract_content_item",item)
        result = _extract_item(item,content=content)
        if result["Value"] :
            if result["Region"] in ["paragraph", "raw_text", "text_from_page_and_next"] :

                cordinates=get_cordinates_for_value_from_context(result["Page"], result["Source"],results["Value"])
                if cordinates == (0, 0, 0, 0):
                    result['Coordinates']= dict({ "fromX": result['fromX'], "fromY": result['fromY'],"toX":result['toX'],"toY":result['toY']})
                else :

                    result['Coordinates']= dict({"fromX": cordinates[0], "fromY":cordinates[1], "toX":cordinates [3] })


            else:
                result['Coordinates']= dict({ "fromX": result['fromX'], "fromY": result['fromY'],"toX":result['toX'],"toY":result['toY']})
        else :
            result["Coordinates"]= dict({"fromX": None, "fromY": None, "toX": None, "toY": None })
            result.pop('fromX')
            result.pop('fromY')
            result.pop('toX')
            result.pop('toY')
        entity_name, def_type =item['name'], item['type']
        if def_type=='search':
            method = "qanet" if item.get("text_extract") else 'regex'
        else:
            method = def_type
#     if not filters or filters.get(entity_name) == method : ## or not filters.get(entity_name)
        data_frame=data_frame.append(result, ignore_index=True)
        if save_results :
            store_results(data_frame)
    return data_frame
