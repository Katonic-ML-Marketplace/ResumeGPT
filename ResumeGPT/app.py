import streamlit as st
import streamlit_ext as ste
import os
import hydralit_components as hc
from PIL import Image
import base64
import io
from streamlit_option_menu import option_menu
import pandas as pd
from io import BytesIO

from OCR_Reader import CVsReader
from ChatGPT_Pipeline import CVsInfoExtractor
import sys

im = Image.open('../image/collabera_digital.ico')



st.set_page_config(
    page_title='ResumeGPT', 
    page_icon = im,  
    initial_sidebar_state = 'auto'
)

with st.sidebar:
        selected = option_menu(
            menu_title = "Main Menu",
            options = ["About the App","ResumeGPT","FAQ"])

if selected == "ResumeGPT":
    st.markdown(
            """
            <style>
                [data-testid="stSidebarNav"] {
                    background-image: url(data:image/png;base64,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);
                    background-repeat: no-repeat;
                    padding-top: 120px;
                    background-position: 20px 20px;
                }
                [data-testid="stSidebarNav"]::before {
                    margin-left: 20px;
                    margin-top: 10px;
                    font-size: 30px;
                    position: relative;
                    top: 100px;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )

    IFRAME = '<iframe src="https://ghbtns.com/github-btn.html?user=Katonic-ML-Marketplace&repo=ResumeGPT&count=true&size=large" frameborder="0" scrolling="0" width="170" height="30" title="GitHub"></iframe>'

    st.markdown(
        f"""
        # ResumeGPT {IFRAME}
        """,
        unsafe_allow_html=True,
    )

    #cvs_directory_path_arg, openai_api_key_arg, desired_positions_arg = sys.argv[1], sys.argv[2], sys.argv[3].split(",")

    cvs_directory_path_arg = "../CVs"

    if not os.getenv("OPENAI_API_KEY"):
        openai_api_key_arg = st.text_input(
            "Enter your OpenAI API Key: [(click here to obtain a new key if you do not have one)](https://platform.openai.com/account/api-keys)",
            type="password",
        )
    else:
        openai_api_key = os.getenv("OPENAI_API_KEY")


    def download_sample_pdf():
        with open("../sample_cvs/Software-Engineer.pdf", "rb") as file:
            contents = file.read()
            b64 = base64.b64encode(contents).decode()
            href = f'<a href="data:application/pdf;base64,{b64}" download="Software-Engineer.pdf">Download Sample PDF</a>'
            st.markdown(href, unsafe_allow_html=True)

    download_sample_pdf()
    uploaded_file = st.file_uploader('Choose single or multiple .pdf files', type="pdf",accept_multiple_files=True)
    for i in uploaded_file:
        with open(os.path.join("../CVs",i.name),"wb") as f:
            f.write(i.getbuffer())

   

    

    desired_positions_arg = st.text_input(
        "Enter the desired_position for which you're extracting your resume e.g. Software Engineer, Data Scientist, Data Analyst, Data Engineer"
    )

    if st.button("Extract Resume"):
        try:
            with st.spinner("Processing... This may take a while⏳"):
                #st.write("fetching required files")


                desired_positions = [position.strip() for position in desired_positions_arg.split(",")]
                #st.write("Splitting the desired positions into a list and removing any leading or trailing whitespace")
                #st.write(desired_positions)

                cvs_reader = CVsReader(cvs_directory_path = cvs_directory_path_arg)

                cvs_content_df = cvs_reader.read_cv()


                cvs_info_extractor = CVsInfoExtractor(cvs_df = cvs_content_df, openai_api_key = openai_api_key_arg, desired_positions = desired_positions)
                st.write("It takes as an argument the dataframe returned by the read_cv method of the CVsReader instance and the desired positions in a list.")
                st.write(cvs_info_extractor)
                st.write("---")

                extract_cv_info_dfs = cvs_info_extractor.extract_cv_info()
                st.write("This method presumably returns a list of dataframes, each dataframe corresponding to the extracted information from each CV.")

                # Assuming you have the extracted CV data in a Pandas DataFrame called extracted_data_df
                # Convert the DataFrame to Excel format and store it in the resume_bytes variable
                #resume_bytes = extracted_data_df.to_excel(index=False, encoding="utf-8", engine="openpyxl")

        

                col1, col2, col3 = st.columns(3)
                cvs_content = cvs_content_df.to_csv(index=False)
                csv_content_bytes = io.BytesIO(cvs_content.encode())

                try:
                    with col1:
                        btn = ste.download_button(
                            label="Download PDF Content.csv",
                            data=csv_content_bytes,
                            file_name="resume_content.csv",
                            mime="text/csv",
                        )
                except Exception as e:
                    st.write(e)

                csv_extracted_content = extract_cv_info_dfs.to_csv(index=False)
                csv_bytes = io.BytesIO(csv_extracted_content.encode())

                try:
                    with col2:
                        btn = ste.download_button(
                            label="Download Extracted_CV.csv",
                            data=csv_bytes,
                            file_name="extracted_resumes.csv",
                            mime="text/csv",
                        )
                except Exception as e:
                    st.write(e)
                
                excel_file = BytesIO()
                with pd.ExcelWriter(excel_file, engine="xlsxwriter", mode="xlsx") as writer:
                    extract_cv_info_dfs.to_excel(writer, index=False)
                
                excel_file.seek(0)
                excel_bytes = excel_file.getvalue()
                # excel_file = pd.ExcelWriter("resume.xlsx", engine="xlsxwriter").get_contents()
                # excel_bytes = excel_file.getvalue()
                # xlsx_extracted_content = extract_cv_info_dfs.to_excel(excel_file,index=False)
                # xlsx_bytes = io.BytesIO(xlsx_extracted_content.encode())

                try:
                    with col3:
                        btn = ste.download_button(
                            label="Download Extracted_CV.xlsx",
                            data=excel_bytes,
                            file_name="resume.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        )
                except Exception as e:
                    st.write(e)

        except OpenAIError as e:
            st.error(e._message) 
        

if selected == "About the App":
    st.markdown("## About ResumeGPT")
    st.markdown("ResumeGPT is an app that helps streamline the hiring process by extracting and organizing key information from CVs and resumes. It offers the following benefits:")

    st.markdown("1. **Identify qualified candidates:** ResumeGPT extracts important details such as skills, experience, and education from CVs and resumes. This helps hiring managers identify candidates who meet the job requirements.")
    
    st.markdown("2. **Compare candidates:** ResumeGPT organizes candidate data in a structured format, allowing hiring managers to easily compare candidates based on skills, experience, and education. This facilitates a side-by-side evaluation of candidates.")
    
    st.markdown("3. **Make informed hiring decisions:** ResumeGPT provides a comprehensive overview of each candidate, enabling hiring managers to make informed decisions. By having access to key information, such as skills and experience, hiring managers can select the best candidate for the job.")
    
    st.markdown("By leveraging the capabilities of ResumeGPT, hiring managers can streamline the candidate evaluation process and make more effective hiring decisions.")

if selected == "FAQ":
    faq_data = {
    "How does ResumeGPT extract information from CVs and resumes?": "ResumeGPT utilizes natural language processing techniques to analyze the text and extract key details such as skills, experience, and education.",
    "Can ResumeGPT handle different file formats for CVs and resumes?": "ResumeGPT only supports pdf format.",
    "What information does ResumeGPT organize and present for each candidate?": "ResumeGPT organizes candidate data in a structured format, including skills, experience, and education. It provides a comprehensive overview of each candidate's qualifications.",
    "How does ResumeGPT help in comparing candidates?": "ResumeGPT allows hiring managers to compare candidates based on their skills, experience, and education. It provides a side-by-side evaluation of candidates, making it easier to assess their suitability for the job.",
    "Can ResumeGPT handle multiple CVs and resumes at once?": "Yes, ResumeGPT supports processing multiple CVs and resumes simultaneously. It can efficiently handle a large number of documents to streamline the hiring process.",
    "Is ResumeGPT customizable to match specific job requirements?": "Yes, ResumeGPT can be configured to extract and prioritize specific skills, qualifications, or keywords based on the job requirements. This customization helps tailor the evaluation process to the specific needs of the hiring team.",
    "How accurate is ResumeGPT in extracting and organizing information?": "ResumeGPT utilizes advanced language models and natural language processing techniques to achieve high accuracy in extracting and organizing information. However, it's important to review and validate the extracted data to ensure its accuracy.",
    "Is the data processed by ResumeGPT secure and confidential?":"Yes, ResumeGPT takes data security and confidentiality seriously. All CVs and resumes processed by the app are treated with strict confidentiality and are not shared with any third parties."
    }
    # Display the FAQ section
    st.subheader("Frequently Asked Questions")

    # Iterate over the FAQ data and create expandable sections
    for question, answer in faq_data.items():
        with st.expander(question):
            st.write(answer)
