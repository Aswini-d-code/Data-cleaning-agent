# AI-Powered Data Quality & Analytics Platform

A robust web application designed for automated data preprocessing and conversational data intelligence. This platform enables users to transform raw, messy datasets into analysis-ready assets through a streamlined, AI-integrated workflow.

## 🛠️ Core Functionalities
* **Automated Quality Assessment:** Real-time generation of data health metrics, including completeness scores and redundancy checks.
* **One-Click Preprocessing:** Systematic removal of null values and duplicate records with an integrated export engine.
* **Conversational Intelligence:** A natural language interface powered by Gemini 1.5 Flash, allowing users to query data structures and insights via text and voice.

## 🏗️ Technical Architecture
* **UI Framework:** Streamlit (Python-based)
* **Data Processing:** Pandas
* **LLM Integration:** Google Generative AI (Gemini SDK)
* **Multimodal Output:** Web Speech API for real-time text-to-speech synthesis.

## 🚀 Deployment Instructions
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Configure `GEMINI_API_KEY` in your environment secrets.
4. Run the application: `streamlit run app.py`.

## 🛡️ Data Privacy
The application processes data within the local session state. No user data is persisted on the server, ensuring privacy and compliance with standard data handling protocols.