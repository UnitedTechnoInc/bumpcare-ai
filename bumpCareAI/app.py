from flask import Flask, render_template, request, jsonify, redirect, url_for
import pyodbc
import torch
from langchain import PromptTemplate, LLMChain
from langchain_community.llms import Ollama
from datetime import datetime
from zoneinfo import ZoneInfo
import re
import faiss
import pickle
import warnings
import json
import os
import pandas as pd

warnings.filterwarnings("ignore")

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')

# MSSQL connection functions
server = "your server details here"
database = "your database details here"

def connect_to_mssql(server="your server details here", database="your database details here"):
    try:
        conn_str = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            f"SERVER={server};"
            f"DATABASE={database};"
            "Trusted_Connection=yes;"
        )
        conn = pyodbc.connect(conn_str)
        return conn
    except Exception as e:
        return None
    

session_history = []
def get_doctor_summary(rows,patient_num):
    """Generate clinical summary using GPT-OSS model"""

    global session_history
    # DB connection and query
    conn = connect_to_mssql(server="your server details here", database="your database details here")
    if not conn:
        return "Database connection failed"
        
    query = """
    SELECT TOP 50
        t2.PatientID,
        t2.*,
        t3.*
    FROM [dbo].[Patient_data2_trimester2] t2
    FULL OUTER JOIN [dbo].[Patient_data_trimester3] t3
        ON t2.PatientID = t3.PatientID
    WHERE (t2.ultrasoundfindings NOT LIKE '%normal%' OR t2.ultrasoundfindings IS NULL)
      AND (t3.ultrasoundfindings NOT LIKE '%normal%' OR t3.ultrasoundfindings IS NULL);
    """

    df = pd.read_sql(query, conn)
    data = df.to_string(index=False)
    conn.close()

    # Initialize LLM model
    llm = Ollama(model="gpt-oss:20b", base_url="http://127.0.0.1:11434")
    patient_number = patient_num
    # Convert rows to readable format
    patient_data = ""
    #if isinstance(rows, (list, tuple)) and len(rows) > 0:
    with open("index.pkl", "rb") as f:
        documents = pickle.load(f)
    if isinstance(rows, dict):
        try:
            for idx, row in enumerate(rows, start=1):
                patient_data += f"Record {idx}: {str(row)}\n"
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            patient_data = rows
        except Exception as e:
            pass

        prompt_template = PromptTemplate(
        input_variables=["patient_data","patient_number","documents"],
        template="""
        You are an AI doctor assistant.
        The doctor has provided patient data across all trimesters.

        patient id:
        {patient_number}

        You are an AI doctor assistant. Based on the following patient data:

        {patient_data}
    clinical reference {documents}

        Please generate the output in this structured format with clear line breaks:
         1. Current Summary:  
         Always include trimester-wise details (3rd) explicitly in the summary by referring {patient_data} and include the weeks, and if data is missing, clearly state it
        <your analysis here>
       

    2. AI Clinical Risk:  
        1. Patient-specific risk factors identified from {patient_data}.  
        2. Risk patterns compared with medical research or studies.  
        3. Potential complications based on condition progression.  
        4. Preventive measures to reduce these risks.  
        5. Clinical action plan summarizing next steps.  

    3. AI Suggestion:  
        1. Lifestyle modifications for better health outcomes.  
        2. Monitoring or diagnostic tests to consider.  
        3. Preventive care recommendations.  
        4. Possible follow-up requirements.  
        5. Supportive advice for long-term well-being.  

    4. AI Medication:  
        1. Suggested medication categories (not brand-specific).  
        2. Dosage or frequency guidelines (general, not prescriptive).  
        3. Monitoring needed for medication safety.  
        4. Contraindications or precautions.  
        5. Notes on adherence and compliance.  

    5. AI Diet:  
        1. Foods to prioritize for current health needs.  
        2. Foods to limit or avoid due to risks.  
        3. Balanced diet recommendations.  
        4. Hydration and nutrient intake tips.  
        5. Example daily food pattern.  
        
    6. Clinical Research Evidence :
        Search and give the reference paper link from this: 
        https://www.nature.com/articles/d41586-025-00959-7
        https://pmc.ncbi.nlm.nih.gov/articles/PMC7122255/?utm_source=chatgpt.com
        https://foodandnutritionresearch.net/index.php/fnr/article/view/3676
        https://bmcpregnancychildbirth.biomedcentral.com/articles?utm_source=chatgpt.com
        https://foodandnutritionresearch.net/index.php/fnr/article/view/3676
        https://www.ncbi.nlm.nih.gov/books/NBK555485/
        https://www.sciencedirect.com/science/article/pii/S2589537023004418

        When creating the above summary structured summary:
            1. Do NOT use star (*) symbols in your output. Use hyphens (-) or numbers instead.
            2. Each section heading (e.g., Current Summary, AI Clinical Risk, AI Suggestion, AI Medication,AI Diet) must contain a maximum of 5 concise bullet points.
            3. Avoid repeating points or long explanations. Each bullet should be clear, short, and useful.
            4. Dont use any symbols and stricty use numbers for points
            5. Keep the response readable and professional.
            6. Output must be plain text only. Do not use HTML, Markdown, Bootstrap, or any other markup—just display text.            
         """
        )  

        formatting_prompt = PromptTemplate(
        input_variables=["summary","timestamp"],
        template = """
           
			The {summary} is my output generated from LLM . I want this {summary} to be modified in a presentable
            bootstrap format and text size  14px. you need to provide the answer and the answer must be in bootstrap.
            Answer the user question as only in correct bootstrap format from the {summary} and don't add 'alert alert-success' in bootstrap code and keep the font-size:15px:
			You are an AI assistant. Return the output ONLY in valid HTML using Bootstrap 5. Do not include explanations, comments, or any text outside the HTML code.

                Follow these rules strictly:
                1. Wrap each section in <div class="card mb-3">.
                2. Inside each card, add <div class="card-body" style="font-size:15px;">.
                3. Use <h5 class="card-title"> for the section heading.
                4. Use an ordered list <ol> with exactly 5 concise <li> points.
                5. Do NOT include Bootstrap alert classes (like "alert alert-success").
                6. Do NOT include any inline CSS other than "font-size:15px;" inside card-body.
                7. Do NOT add comments or extra text outside the HTML structure.
                8. Should provide the reference paper access link in <a <a href='globally search url link and give here' target='_blank' rel='noopener noreferrer'>.
                9. Should not strictly add anything like this before or  after the response ```html or ``` .
                10. I need all the response in Bootstrap Tabs with Tab links.
                11. Make sure data-bs-target and aria-controls are unique because multiples tabs will be generated, example data-bs-target="#home_qbr".
                12. Each tab id, data-bs-target, and aria-controls must strictly include the timestamp {timestamp}. Do NOT use generic ids like "tab-summary" or "tab-suggestions". Always format them as tab-{timestamp}-summary, tab-{timestamp}-risk, tab-{timestamp}-suggestions, tab-{timestamp}-medication, tab-{timestamp}-food",tab-{timestamp}-referencelink".
                13. If there exists any danger or emergency situation for the patient, highlight that word or phrase with <span style="color:red; font-weight:bold;">"disease word"</span>.
                14. If there exists any safe, normal, or non-emergency situation for the patient, highlight that word or phrase with <span style="color:green; font-weight:bold;">"medically fit or no issues in health word"</span>.

                Format:
<ul class="nav nav-tabs" id="myTab" role="tablist">
  <li class="nav-item" role="presentation">
    <button class="nav-link active" id="tab-{timestamp}-summary-tab" data-bs-toggle="tab" data-bs-target="#tab-{timestamp}-summary" type="button" role="tab" aria-controls="tab-{timestamp}-summary" aria-selected="true">Current Summary</button>
  </li>
  <li class="nav-item" role="presentation">
    <button class="nav-link" id="tab-{timestamp}-risk-tab" data-bs-toggle="tab" data-bs-target="#tab-{timestamp}-risk" type="button" role="tab" aria-controls="tab-{timestamp}-risk" aria-selected="false">AI Clinical Risk</button>
  </li>
  <li class="nav-item" role="presentation">
    <button class="nav-link" id="tab-{timestamp}-suggestions-tab" data-bs-toggle="tab" data-bs-target="#tab-{timestamp}-suggestions" type="button" role="tab" aria-controls="tab-{timestamp}-suggestions" aria-selected="false">AI Suggestion</button>
  </li>
  <li class="nav-item" role="presentation">
    <button class="nav-link" id="tab-{timestamp}-medication-tab" data-bs-toggle="tab" data-bs-target="#tab-{timestamp}-medication" type="button" role="tab" aria-controls="tab-{timestamp}-medication" aria-selected="false">AI Medication</button>
  </li>
  <li class="nav-item" role="presentation">
    <button class="nav-link" id="tab-{timestamp}-food-tab" data-bs-toggle="tab" data-bs-target="#tab-{timestamp}-food" type="button" role="tab" aria-controls="tab-{timestamp}-food" aria-selected="false">AI Diet</button>
  </li>
<li class="nav-item" role="presentation">
  <button class="nav-link" 
          id="tab-{timestamp}-referencelink-tab" 
          data-bs-toggle="tab" 
          data-bs-target="#tab-{timestamp}-referencelink" 
          type="button" role="tab" 
          aria-controls="tab-{timestamp}-referencelink" 
          aria-selected="false">
    Clinical Research Evidence
  </button>
</li>

</ul>      
            """
        )
        chain = LLMChain(llm=llm, prompt=prompt_template)
        # First summary generation
        summary = chain.run(patient_data=patient_data, patient_number=patient_number, documents=documents)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        formatting_chain = LLMChain(llm=llm, prompt=formatting_prompt)
        summary = formatting_chain.run(summary=summary, timestamp=timestamp)
        summary  =  re.sub(r"^```html\s*|\s*```$", "", summary, flags=re.MULTILINE)

        user_input = patient_number

    else:

        patient_data=rows
        session_history = session_history
        prompt_template = PromptTemplate(
        input_variables=["patient_data","data","session_history","documents"],
        template="""
        You are an AI doctor assistant.
        The following input contains general patient-related questions or concerns asked by the user:

        User Questions / Input:
        {patient_data}

        You are an AI doctor assistant. Based on the above user input and the provided patient records:

        {data}
        previous chat history:
        {session_history}
    clinical document: {documents}
        Please generate the output in this structured format with clear line breaks and refer previous chat history:

        1. Summary:  
            - Provide a detailed information or concerns from the user input and data.  

        2. AI Clinical Risk:  
            - Provide a research-backed recommendation strictly related to the user input {patient_data}.  
            - Include at least one credible research link or medical article for reference.  
            - Provide an overall clinical risk assessment relevant to the user’s input and patient data.  
            - Mention specific patient IDs from the records (e.g., Patient ID 4, Patient ID 67) who experienced similar complications and briefly explain recovery as examples.  
            - Include at least one credible web link (e.g., Google search link or research article) supporting the recommendation. Keep it concise and professional.  

        4. Clinical Research Evidence:  
            - Provide clear, practical, and concise suggestions based on the context.

        5. Reference link:
        Search and give the reference paper link from this: 
        https://www.nature.com/articles/d41586-025-00959-7
        https://pmc.ncbi.nlm.nih.gov/articles/PMC7122255/?utm_source=chatgpt.com
        https://foodandnutritionresearch.net/index.php/fnr/article/view/3676
        https://bmcpregnancychildbirth.biomedcentral.com/articles?utm_source=chatgpt.com
        https://foodandnutritionresearch.net/index.php/fnr/article/view/3676
        https://www.ncbi.nlm.nih.gov/books/NBK555485/
        https://www.sciencedirect.com/science/article/pii/S2589537023004418
        
        Formatting Rules:
        1. Do NOT use star (*) symbols in your output. Use hyphens (-) or numbers instead.
        2. Each section heading (Summary, AI Clinical Risk, AI Suggestions) must contain a maximum of 5 concise points.
        3. Avoid repeating points or long explanations. Each point should be short, clear, and useful.
        4. Only use numbers for list items, no other symbols.
        5. Keep the tone professional and easy to understand.
        6. Output must be plain text only. Do not use HTML, Markdown, Bootstrap, or any other markup.

        """
    )

    # Main Chain
        chain = LLMChain(llm=llm, prompt=prompt_template)
        start_time = datetime.now(ZoneInfo("Asia/Kolkata"))

        # First summary generation
        summary = chain.run(patient_data=patient_data, data=data, session_history = session_history,documents=documents)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        end_time = datetime.now(ZoneInfo("Asia/Kolkata"))
        session_history.append(f"user:{rows}, response:{summary}")

        formatting_prompt = PromptTemplate(
            input_variables=["summary","timestamp"],
            template = """
            
                The {summary} is my output generated from LLM . I want this {summary} to be modified in a presentable
                bootstrap format and text size  14px and you should not trim the LLM Inputs and points and show all the content and information, you need to provide the answer and the answer must be in bootstrap.
                Answer the user question as only in correct bootstrap format from the {summary} and don't add 'alert alert-success' in bootstrap code and keep the font-size:15px:
                You are an AI assistant. Return the output ONLY in valid HTML using Bootstrap 5. Do not include explanations, comments, or any text outside the HTML code.

                    Follow these rules strictly:
                    1. Wrap each section in <div class="card mb-3">.
                    2. Inside each card, add <div class="card-body" style="font-size:15px;">.
                    3. Use <h5 class="card-title"> for the section heading.
                    4. Use an ordered list <ol> with exactly 5 concise <li> points.
                    5. Do NOT include Bootstrap alert classes (like "alert alert-success").
                    6. Do NOT include any inline CSS other than "font-size:15px;" inside card-body.
                    7. Do NOT add comments or extra text outside the HTML structure.
                    8. Should provide the reference paper access link in <a href='globally search link and give here' target='_blank' rel='noopener noreferrer'>.
                    9. Should not strictly add anything like this before or  after the response ```html or ``` .
                    10. I need all the response in Bootstrap Tabs with Tab links.
                    11. Make sure data-bs-target and aria-controls are unique because multiples tabs will be generated, example data-bs-target="#home_qbr".
                    12. Each tab id, data-bs-target, and aria-controls must strictly include the timestamp {timestamp}. Do NOT use generic ids like "tab-summary" or "tab-suggestions". Always format them as tab-{timestamp}-summary, tab-{timestamp}-research, tab-{timestamp}-suggestions,tab-{timestamp}-referencelink.
                    13. ***MUST*** If there exists any danger or emergency situation for the patient, highlight that word or phrase with <span style="color:red; font-weight:bold;">"disease name"</span>.
                    14. ***MUST*** If there exists any safe, normal, or non-emergency situation for the patient, highlight that word or phrase with <span style="color:green; font-weight:bold;">medically fit or no issues in health word"</span>.
                    15. If there exisits any patient ID in the {summary} make it bold and black color (example: "patient ID 4")   <li style="font-weight: bold; color: black;">Patient ID</li>.
                    Example:
    <ul class="nav nav-tabs" id="myTab" role="tablist">
    <li class="nav-item" role="presentation">
        <button class="nav-link active" id="tab-{timestamp}-summary-tab" data-bs-toggle="tab" data-bs-target="#tab-{timestamp}-summary" type="button" role="tab" aria-controls="tab-{timestamp}-summary" aria-selected="true">Summary</button>
    </li>
    <li class="nav-item" role="presentation">
        <button class="nav-link" id="tab-{timestamp}-research-tab" data-bs-toggle="tab" data-bs-target="#tab-{timestamp}-research" type="button" role="tab" aria-controls="tab-{timestamp}-research" aria-selected="false">AI Clinical Risk</button>
    </li>
    <li class="nav-item" role="presentation">
        <button class="nav-link" id="tab-{timestamp}-suggestions-tab" data-bs-toggle="tab" data-bs-target="#tab-{timestamp}-suggestions" type="button" role="tab" aria-controls="tab-{timestamp}-suggestions" aria-selected="false">AI Suggestion</button>
    </li>
<li class="nav-item" role="presentation">
  <button class="nav-link" 
          id="tab-{timestamp}-referencelink-tab" 
          data-bs-toggle="tab" 
          data-bs-target="#tab-{timestamp}-referencelink" 
          type="button" role="tab" 
          aria-controls="tab-{timestamp}-referencelink" 
          aria-selected="false">
    Clinical Research Evidence
  </button>
</li>
    </ul>                      
                """
            )
        
        formatting_chain = LLMChain(llm=llm, prompt=formatting_prompt)
        summary = formatting_chain.run(summary=summary, timestamp=timestamp)
        user_input = rows
    session_history.append(f"user:{user_input}, response:{summary}")
    return summary

# Routes
@app.route('/')
def login():
    return render_template('index.html')

@app.route('/landing')
def landing():
    return render_template('landingpage.html')

@app.route('/chat')
def chat():
    return render_template('chatbot.html')

@app.route('/process_patient', methods=['POST'])
def handle_patient_query():
    data = request.json
    patient_id = None
    if request.method == 'POST':
        patient_id =  data.get('patient_input')

        # Query MSSQL
        conn = connect_to_mssql(server="your server details here", database="your database details here")
        cursor = conn.cursor()  
        
        if conn is None:
            return "Database connection failed", 500

        if str(patient_id).isdigit():
            conn = connect_to_mssql(server="your server details here", database="your database details here")
            cursor = conn.cursor()  

            if conn is None:
                return None

            cursor = conn.cursor()
            cursor.execute("""
                SELECT *
                FROM [dbo].[Patient_data_trimester1] AS t1
                JOIN [dbo].[Patient_data2_trimester2] AS t2 ON t1.PatientID = t2.PatientID
                JOIN [dbo].[Patient_data_trimester3] AS t3 ON t1.PatientID = t3.PatientID
                WHERE t1.PatientID = ?
            """, (patient_id,))

            row = cursor.fetchone()
            columns = [column[0] for column in cursor.description]
            if row:
                rows = dict(zip(columns, row))
            
            result = get_doctor_summary(rows,patient_id)
        else:
            rows = patient_id
            patient_id = ""
            result = get_doctor_summary(rows,patient_id)
    return jsonify({"summary": result})

@app.route('/login', methods=['POST'])
def handle_login():
    # Simple login handling - redirect to landing page
    return redirect(url_for('landing'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)