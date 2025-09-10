BumpCare AI – Smart Care, Smart Pregnancy
BumpCare AI is an AI-powered pregnancy care assistant built for doctors and nurses. It provides instant trimester summaries, risk identification, medication class suggestions, and evidence-based recommendations by leveraging gpt-oss model 20b.
Developed by United Techno.
Problem Statement
Pregnancy care is one of the most critical and high-risk areas in healthcare. Doctors and nurses face daily challenges when dealing with outpatient consultations:
High Patient Volume & Time Pressure


Doctors see dozens of pregnant patients every day, each with complex medical histories, lab reports, and scan results.
Reviewing everything manually in limited consultation time increases the risk of oversight.


Fragmented Data Across Reports


Patient information is spread across lab sheets, ultrasound reports, blood pressure logs, and medical records.
Consolidating this manually is inefficient and error-prone.


Missed Risk Detection


Conditions such as pre-eclampsia, gestational diabetes, fetal growth restriction, thyroid imbalance, and anemia require early detection.
Failure to identify these risks on time may lead to severe complications for mother and baby.


Cognitive Overload for Doctors 
Doctors must interpret multiple results while making clinical judgments quickly.
Nurses assisting in assessments may lack the time or expertise to interpret results fully.


Lack of Real-time Evidence Support


Doctors often cannot access the latest research papers or clinical guidelines during consultations.
This makes it harder to provide evidence-backed care consistently.


These gaps — time pressure, fragmented data, missed risks, cognitive overload, and lack of research integration — directly affect maternal safety, fetal development, and quality of care.
Solution – BumpCare AI
BumpCare AI is designed to bridge these gaps by acting as a doctor’s daily AI assistant. Using patient IDs linked to hospital records, the system automatically generates textual trimester summaries, risk predictions, and safe recommendations.
Key aspects of the solution:
Automated Patient Summaries


Provides trimester status, vitals, lab test interpretations, and fetal growth details.
Consolidates fragmented records into a single, structured view.


Risk Detection & Alerts


AI flags early signs of pre-eclampsia, gestational diabetes, fetal growth restriction, thyroid disorders, and anemia.
Trend-based alerts highlight worsening conditions (e.g., rising BP, falling Hb).


AI-Generated Recommendations


Suggests generic medication classes (iron, folic acid, calcium, omega-3, levothyroxine).
Provides food & nutrition guidance, safe trimester exercises, and lifestyle precautions.
Outputs are textual, clear, and doctor-friendly.


Case Similarity Analysis


Compares current patients with past cases stored in the database.
Offers insights on how similar cases were monitored and managed.


Evidence-Based Medicine


Retrieves and links to research papers and medical ontology.
Ensures all AI suggestions are backed by trusted medical sources.


Doctor & Nurse Workflow Support


Doctors save time by reviewing AI summaries instead of raw reports.
Nurses can use the tool for pre-consultation assessment, enabling efficient teamwork.


This makes pregnancy care safer, faster, and more consistent — while keeping the doctor in control of final decisions.
Key Features
Patient Summary: Gestational age, history, trimester data, labs, scans.
AI Risk Recommendations: Detects maternal & fetal risks early.
AI Medication Suggestions (Non-Branded): Safe supplement classes only.
Food & Lifestyle Guidance: Nutrition, trimester-safe exercises, and precautions.
Case Similarity Insights: Compares with past patients having similar conditions.
Research Integration: Evidence links from vectorized medical papers & ontology.
Secure Access: Role-based login for doctors & nurses.


Mockup UI Screens
Login Page
Doctor Portal
AI Assistant Chat



System Architecture
1) High-Level Overview




2) Components
Component
Tech
Responsibilities
Frontend
HTML/CSS/JS
Login, Patient ID input, textual AI outputs
Backend
FastAPI/Flask
Auth, patient record aggregation, orchestrates AI
AI Models
gpt-oss-20b
Summaries, risk reasoning, safe recs, citations
Patient DB
SQL
Stores patient visits, labs, history
Vector Store
FAISS
Research, ontology, similar cases
Security
DB-Based Auth
Role-based access 

3) Data Flow (Request → Response)


4) RAG & Model Details
Embeddings: all-MiniLM-L6-v2
Models:
gpt-oss-20b → fast responses
Safety Guards: no branded drugs, value-range validation, unsafe meds filter


5) Data Model (Minimal Example)
patients(id, name, dob, gravida, history, conditions)
visits(id, patient_id, gestational_week, trimester, bp_sys, bp_dia, weight)
labs(id, patient_id, visit_id, test_name, value, unit)
scans(id, patient_id, visit_id, finding, efw, fetal_hr, placenta_position)
cases(id, patient_id, phenotype_vector, outcome)
6) Security & Compliance
Data:DB-Auth (access control)
Privacy: Prepared Synthesized data for the patients.

Ethical Considerations
Doctor-in-the-loop: AI supports, doctors decide.
Non-branded recommendations: Only generic medication classes.
Transparency: All AI outputs link to evidence/research.
Privacy: Patient data anonymized and handled securely.


Setup Instructions

# Clone repo
git clone https://github.com/unitedtechno/bumpcare-ai.git
cd bumpcare-ai

# Install dependencies
pip install -r requirements.txt

# Run backend
python app.py

Access at: http://127.0.0.1:5000/chat
Test with sample patient IDs from /sample_data/patients.json

Future Roadmap
Integration with multiple hospitals → Expand deployment to connect with a network of hospitals.


EHR/EMR Sync → Support bidirectional sync with hospital EHR/EMR systems so patient summaries, risks, and AI suggestions are automatically stored in official records.


Interoperability Standards → Adopt HL7 FHIR / SNOMED CT to ensure data portability across healthcare systems.


Postpartum Care → Extend BumpCare beyond pregnancy into postpartum mother and infant health.


Wearable Integration → Ingest real-time vitals (BP cuffs, glucose monitors, smartwatches) for continuous risk monitoring.


Multilingual Support → Enable region-specific languages to support rural doctors and patients.


Mobile Companion App → Lightweight mobile tool for nurses and field healthcare workers.
Known Limitations
Doctor-in-the-loop required → BumpCare AI is a decision-support tool, not a replacement for clinical judgment. All outputs must be validated by a healthcare professional.


Research freshness → Recommendations depend on how frequently medical guidelines and research papers are ingested into the vector store. Delays may reduce evidence currency.


Data dependency → The system’s accuracy relies on completeness and quality of patient records (labs, scans, vitals). Missing data may affect risk assessment.


EHR/EMR integration scope → Current implementation is hospital-specific. Cross-hospital interoperability (FHIR/HL7) is part of future roadmap, not fully implemented yet.


Language limitations → Presently supports English only; multilingual expansion is planned.


Edge cases in pregnancy → Rare complications (e.g., multiple gestation anomalies, rare genetic syndromes) may not be covered fully by the AI assistant.


Submission Video
Demo video (≤ 3 minutes) showing:
Doctor login
Patient ID entry
AI summary & risks
Recommendations (meds, food, exercise)
Research link output



Team
United Techno – AI & Healthcare Innovation Team
Ramesh Hariharan
Vigneshwaran Neelakandan
Gayathri Gunasekar
Link: https://www.unitedtechno.com/


BumpCare AI = Faster Reviews. Smarter Care. Safer Pregnancy.
