
import os
import streamlit as st
import base64
import shutil
import json
import requests
import pandas as pd
import time

# st.set_page_config(layout="wide")
# st.set_page_config(
#     page_title="Gyani",
#     page_icon="chart_with_upwards_trend",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )
# @st.cache
# st.set_page_config(layout="wide")

# interact with FastAPI endpoint
backend = "http://127.0.0.1:5000/process_doc"
# dst='C:/Users/vikas.bhadouria/Documents/Gyani_AI/Gyani_Demo_VM_v1.1/Python/projects/Kapitus'

def process(Input_name,output_path, server_url: str):
    
    payload = json.dumps({
      "input": Input_name,
      "output": output_path
    })
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", server_url, headers=headers, data=payload)
    response_output_path=os.path.join(output_path,Input_name[:-4])
    response_output_file=os.path.join(dst,response_output_path,Input_name[:-4]+' definition_'+Input_name[:-4]+'.xlsx')
                          
    return response,response_output_file




def _max_width_():
    max_width_str = f'max-width: 960px';

    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>
    """,
        unsafe_allow_html=True,
    ) 

# m = st.markdown("""
# <style>
# div.stButton > button:first-child {
#     background-color: rgb(204, 49, 49);
# }
# </style>""", unsafe_allow_html=True)

def convert_df(df):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')
    
def main():


    _max_width_()

    st.subheader('Document AI : An integrated Platform as a Service(iPaaS)')

  #  st.image(os.path.join('Images','banner_1.jpg'), use_column_width  = True)
#     st.markdown("<h1 style='text-align: center; color: white;'>Time to become a comic book character</h1>", unsafe_allow_html=True)

    st.markdown("<h2 style='text-align: center; color:black;'>Document AI : Smart Document Processing</h2>", unsafe_allow_html=True)
#     with st.expander("Configuration Option"):
#         st.write("**Autoprocess** With the help  of Our Solution,Get all the information your document hold.")
#     output_path = st.sidebar.text_input('Output Path ','Output ')

    menu = ["AI Based  Language Model"]
    st.sidebar.header('Model Selection')
    choice = st.sidebar.selectbox('Choose your extract model?', menu)
    
    output_path = st.sidebar.text_input('Output Path','Output')

    # Create the Home page
    if choice == "AI Based  Language Model":
#         st.sidebar.header('Configuration')
        st.write("Upload a document and see the structured data extracted. ")

        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>', unsafe_allow_html=True)

        st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)

        choose=st.radio("Select Document Type",("General","Forms/Invoice","Text Only","Tabular"))
        uploaded_file = st.file_uploader('Upload your Document here',type=['PDF','Doc'])
        if uploaded_file is not None:
            if st.button("Load"):
            #Saving upload                                       
                with open(os.path.join("fileDir",uploaded_file.name),"wb") as f:
                    f.write((uploaded_file).getbuffer())
                    uploaded_filed_address=os.path.join("fileDir",uploaded_file.name)
                    f.close()
                    st.success("File Saved")
                shutil.copyfile(os.path.join("fileDir",uploaded_file.name), os.path.join(dst,"fileDir",uploaded_file.name))
                st.success('File Loaded Successfully!')

#                         import subprocess
#                         subprocess.run(["scp", FILE, "USER@SERVER:PATH"])

                file_details = {"Name":uploaded_file.name, "Type":uploaded_file.type,
                                "Size":uploaded_file.size}
                file_details_df=pd.DataFrame(file_details,index=list(range(1)))
                st.markdown("<h4 style='text-align: center; color:black;'>File Details</h4>", unsafe_allow_html=True)
                st.table(file_details_df)

                if uploaded_file.type == "text/plain":
                    st.warning('Error in Loading File, Kindly retry With PDF file.')

#                     Read as string (decode bytes to string)
                    raw_text = str(uploaded_file.read(),"utf-8")
                    st.text(raw_text)
                
                elif uploaded_file.type == "application/pdf":
                    with st.spinner('Wait for it...'):
                        time.sleep(2)
                    st.success('Done!')
                    
                    try:
                        st.success('Done!')
#                         with open(uploaded_filed_address,"rb") as f:
#                             base64_pdf = base64.b64encode(f.read()).decode('utf-8')
#                         pdf_display = f'<iframe style="zoom:0.71;"  src="data:application/pdf;base64,{base64_pdf}" width=100% height="500" type="application/pdf"></iframe>'   
#                         st.markdown(pdf_display, unsafe_allow_html=True)
                    except:
                        st.write("None")
                else : 
                    st.warning('Error in Loading File, Kindly retry after some time.')




            if st.button("Extract"):
                try:
                    #                 """### gif from local file"""
#                 file_ = open(os.path.join('Images','Banner_1.gif'), "rb")
#                 contents = file_.read()
#                 data_url = base64.b64encode(contents).decode("utf-8")
#                 file_.close()

#                 st.markdown(
#                     f'<img src="data:image/gif;base64,{data_url}" alt="banner gif">',
#                     unsafe_allow_html=True,
#                 )



                    response,response_output_file=process(uploaded_file.name,output_path,backend)

    #                 # create progress bar
    #                 my_bar = st.progress(0)
    #                 # progress bar continues to complete from 0 to 100
    #                 for percent_complete in range(100):
    #                     time.sleep(0.1)
    #                     my_bar.progress(percent_complete + 1)
                    response_text=response.text
                    result=pd.read_excel(response_output_file,index_col=0)
                    result=result[["Name","Value","Page"]]
                    result.columns=["Entity","Value","Page"]
                    result = result.dropna(subset=['Value'])
                    result = result.reset_index(drop=True)
                    result["Page"]=result.Page.astype(int)+1
                    result=result.astype(str)

                    st.table(result)
                    result.to_excel(os.path.join("Results",uploaded_file.name)+'.xlsx')



                    result_df = convert_df(result)

                    if st.download_button(label="Download Results",
                         data=result_df,
                         file_name=uploaded_file.name+'.csv',
                         mime='text/csv',):
                        st.write('Thanks for downloading!')

    #                 """### gif from local file"""
    #                 file_ = open(os.path.join('Images','Banner_1.gif'), "rb")
    #                 contents = file_.read()
    #                 data_url = base64.b64encode(contents).decode("utf-8")
    #                 file_.close()

    #                 st.markdown(
    #                     f'<img src="data:image/gif;base64,{data_url}" alt="banner gif">',
    #                     unsafe_allow_html=True,
    #                 )


                except:
            
                    try:
                        response_output_path=os.path.join(output_path,uploaded_file.name[:-4])
                        response_output_file=os.path.join(dst,response_output_path,uploaded_file.name[:-4]+' definition_'+uploaded_file.name[:-4]+'.xlsx')
                        result=pd.read_excel(response_output_file,index_col=0)
                        result=result[["Name","Value","Page"]]
                        result.columns=["Entity","Value","Page"]
                        result = result.dropna(subset=["Entity","Value","Page"])
                        result = result.reset_index(drop=True)

                        result["Page"]=result["Page"].astype(int)+1
                        result=result.astype(str)

                        st.table(result)
                        result.to_excel(os.path.join("Results",uploaded_file.name)+'.xlsx')
                    except:

                        response_output_path=os.path.join(output_path,uploaded_file.name[:-4])
                        response_output_file=os.path.join(dst,response_output_path,uploaded_file.name[:-4]+' definition'+'.xlsx')

                        result=pd.read_excel(response_output_file,index_col=0)
                        result=result[["Name","Value","Page"]]
                        result.columns=["Entity","Value","Page"]
                        result = result.dropna(subset=["Entity","Value","Page"])
                        result = result.reset_index(drop=True)

                        result["Page"]=result["Page"].astype(int)+1
                        result=result.astype(str)

                        st.table(result)
                        result.to_excel(os.path.join("Results",uploaded_file.name)+'.xlsx')



                    result_df = convert_df(result)

                    if st.download_button(label="Download Results",
                         data=result_df,
                         file_name=uploaded_file.name+'.csv',
                         mime='text/csv',):
                        st.write('Thanks for downloading!')


#     elif choice == 'AI Based  Version':


if __name__ == '__main__':
    main()

