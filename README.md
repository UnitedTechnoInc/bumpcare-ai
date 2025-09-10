# 🤰 BumpCare AI – Smart Care, Smart Pregnancy

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)  
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green.svg)  
![SQL](https://img.shields.io/badge/Database-SQL-lightgrey.svg)  
![License](https://img.shields.io/badge/License-MIT-yellow.svg)  
![Status](https://img.shields.io/badge/Status-Prototype-orange.svg)  

![Logo](Logo.png)

**BumpCare AI** is an **AI-powered pregnancy care assistant** built for **doctors and nurses**.  
It provides instant trimester summaries, risk identification, medication class suggestions, and evidence-based recommendations by leveraging **gpt-oss-20b**.  

Developed by **United Techno**.  

---

## 📚 Table of Contents
- [Problem Statement](#-problem-statement)
- [Solution](#-solution--bumpcare-ai)
- [Key Aspects of the Solution](#-key-aspects-of-the-solution)
- [Mockup UI Screens](#-mockup-ui-screens)
- [System Architecture](#-system-architecture)
- [Data Flow](#-data-flow)
- [RAG & Model Details](#-rag--model-details)
- [Data Model](#-data-model)
- [Security & Compliance](#-security--compliance)
- [Ethical Considerations](#-ethical-considerations)
- [Setup Instructions](#-setup-instructions)
- [Future Roadmap](#-future-roadmap)
- [Known Limitations](#-known-limitations)
- [Submission Video](#-submission-video)
- [Team](#-team)
- [Tagline](#-tagline)
- [License](#-license)

---

## 🚩 Problem Statement

Pregnancy care is one of the **most critical and high-risk** areas in healthcare. Doctors and nurses face daily challenges during outpatient consultations:

- **High Patient Volume & Time Pressure**  
  Doctors see dozens of pregnant patients every day, each with complex medical histories, lab reports, and scan results. Reviewing everything manually in limited consultation time increases the risk of oversight.  

- **Fragmented Data Across Reports**  
  Patient information is spread across lab sheets, ultrasound reports, blood pressure logs, and medical records. Consolidating this manually is inefficient and error-prone.  

- **Missed Risk Detection**  
  Conditions such as pre-eclampsia, gestational diabetes, fetal growth restriction, thyroid imbalance, and anemia require early detection. Failure to identify these risks on time may lead to severe complications for mother and baby.  

- **Cognitive Overload for Doctors**  
  Doctors must interpret multiple results while making clinical judgments quickly. Nurses assisting in assessments may lack the time or expertise to interpret results fully.  

- **Lack of Real-time Evidence Support**  
  Doctors often cannot access the latest research papers or clinical guidelines during consultations, making it harder to provide evidence-backed care consistently.  

➡️ These gaps directly affect **maternal safety, fetal development, and quality of care**.  

---

## 💡 Solution – BumpCare AI

BumpCare AI is designed to bridge these gaps by acting as a **doctor’s daily AI assistant**. Using patient IDs linked to hospital records, the system automatically generates textual trimester summaries, risk predictions, and safe recommendations.  

---

## ✨ Key Aspects of the Solution

- **Automated Patient Summaries**  
  - Provides trimester status, vitals, lab test interpretations, and fetal growth details.  
  - Consolidates fragmented records into a single, structured view.  

- **Risk Detection & Alerts**  
  - AI flags early signs of pre-eclampsia, gestational diabetes, fetal growth restriction, thyroid disorders, and anemia.  
  - Trend-based alerts highlight worsening conditions (e.g., rising BP, falling Hb).  

- **AI-Generated Recommendations**  
  - Suggests generic medication classes (iron, folic acid, calcium, omega-3, levothyroxine).  
  - Provides food & nutrition guidance, safe trimester exercises, and lifestyle precautions.  
  - Outputs are textual, clear, and doctor-friendly.  

- **Case Similarity Analysis**  
  - Compares current patients with past cases stored in the database.  
  - Offers insights on how similar cases were monitored and managed.  

- **Evidence-Based Medicine**  
  - Retrieves and links to research papers and medical ontology.  
  - Ensures all AI suggestions are backed by trusted medical sources.  

- **Doctor Workflow Support**  
  - Doctors save time by reviewing AI summaries instead of raw reports.  
  - Nurses receive guidance on nutrition, exercise, and lifestyle recommendations.  

- **Nutrition & Exercise Guidance**  
  - Trimester-specific recommendations: iron-rich foods, calcium and folate support.  
  - Safe physical activities such as light yoga, walking, and stretching.  
  - Advice on hydration, sleep hygiene, and avoiding restricted foods/activities.  

---

## 🖥️ Mockup UI Screens

- Login Page  
- Doctor Portal  
- AI Assistant Chat  

---

## 🏗️ System Architecture

1. **High-Level Overview** 

![Architecture](Architecture.png)

2. **Components**  

| Component   | Tech         | Responsibilities |
|-------------|-------------|------------------|
| Frontend    | HTML/CSS/JS | Login, Patient ID input, textual AI outputs |
| Backend     | FastAPI/Flask | Auth, patient record aggregation, orchestrates AI |
| AI Models   | gpt-oss-20b | Summaries, risk reasoning, safe recs, citations |
| Patient DB  | SQL         | Stores patient visits, labs, history |
| Vector Store| FAISS       | Research, ontology, similar cases |
| Security    | DB-Based Auth | Role-based access |  

---

## 🔄 Data Flow

**Request → Response lifecycle:**  

1. Doctor/Nurse logs in and enters Patient ID.  
2. Backend authenticates, fetches records from SQL DB, and retrieves embeddings from FAISS.  
3. AI model generates summaries, risks, and safe recs (with safety guards).  
4. Backend consolidates and delivers structured summary to the portal.  

📌 Flow: Portal → Backend → Database/Vector Store → AI → Backend → Portal  

---

## 📊 RAG & Model Details

- **Embeddings**: `all-MiniLM-L6-v2`  
- **Precomputed embeddings** stored in `index.pkl` for efficient similarity search.  
- **Models**: `gpt-oss-20b` for fast responses.  
- **Safety Guards**: no branded drugs, value-range validation, unsafe meds filter.  

---

## 🗄️ Data Model

Minimal schema:  

```
patients(id, name, dob, gravida, history, conditions)
visits(id, patient_id, gestational_week, trimester, bp_sys, bp_dia, weight)
labs(id, patient_id, visit_id, test_name, value, unit)
scans(id, patient_id, visit_id, finding, efw, fetal_hr, placenta_position)
cases(id, patient_id, phenotype_vector, outcome)
```

---

## 🔐 Security & Compliance

- **DB-Auth** for access control.  
- **Privacy-first**: Synthesized patient data prepared for demos and testing.  

---

## ⚖️ Ethical Considerations

- **Doctor-in-the-loop** → AI supports, doctors decide.  
- **Non-branded recommendations** → Only generic medication classes.  
- **Transparency** → All AI outputs link to evidence/research.  
- **Privacy** → Patient data anonymized and securely handled.  

---

## ⚙️ Setup Instructions

Run BumpCare AI locally with these steps:

```bash
# Clone repo
git clone https://github.com/unitedtechno/bumpcare-ai.git
cd bumpcare-ai

# Install dependencies
pip install -r requirements.txt

# Run backend
python app.py
```

Access at: [http://127.0.0.1:5000/chat](http://127.0.0.1:5000/chat)  
Test with sample patient IDs from `/sample_data/patients.json`  

---

## 🛠️ Future Roadmap

- **Integration with multiple hospitals** → Expand deployment to connect with a network of hospitals.  
- **EHR/EMR Sync** → Support bidirectional sync with hospital EHR/EMR systems so patient summaries, risks, and AI suggestions are automatically stored in official records.  
- **Interoperability Standards** → Adopt HL7 FHIR / SNOMED CT to ensure data portability across healthcare systems.  
- **Postpartum Care** → Extend BumpCare beyond pregnancy into postpartum mother and infant health.  
- **Wearable Integration** → Ingest real-time vitals (BP cuffs, glucose monitors, smartwatches) for continuous risk monitoring.  
- **Multilingual Support** → Enable region-specific languages to support rural doctors and patients.  
- **Mobile Companion App** → Lightweight mobile tool for nurses and field healthcare workers.  

---

## ⚠️ Known Limitations

- **Doctor-in-the-loop required** → BumpCare AI is a decision-support tool, not a replacement for clinical judgment. All outputs must be validated by a healthcare professional.  
- **Research freshness** → Recommendations depend on how frequently medical guidelines and research papers are ingested into the vector store. Delays may reduce evidence currency.  
- **Data dependency** → The system’s accuracy relies on completeness and quality of patient records (labs, scans, vitals). Missing data may affect risk assessment.  
- **EHR/EMR integration scope** → Current implementation is hospital-specific. Cross-hospital interoperability (FHIR/HL7) is part of the future roadmap, not fully implemented yet.  
- **Language limitations** → Presently supports English only; multilingual expansion is planned.  
- **Edge cases in pregnancy** → Rare complications (e.g., multiple gestation anomalies, rare genetic syndromes) may not be covered fully by the AI assistant.  

---

## 🎥 Submission Video

Demo video (≤ 3 minutes) showcasing:  
- **Doctor login**  
- **Patient ID entry**  
- **AI-generated summary & risk detection**  
- **Recommendations** (medications, food, exercise)  
- **Research link outputs**  

---

## 👩‍💻 Team – United Techno (AI & Healthcare Innovation)

- **Ramesh Hariharan**  
- **Vigneshwaran Neelakandan**  
- **Gayathri Gunasekar**  

🔗 [United Techno Website](https://www.unitedtechno.com/)  

---

## ✨ Tagline

**BumpCare AI = Faster Reviews. Smarter Care. Safer Pregnancy.**  

---

## 📜 License

## 📜 License

This project is licensed under the **Apache License 2.0** – see the [LICENSE](LICENSE) file for details.

