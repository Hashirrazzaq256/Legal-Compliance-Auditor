# Legal Compliance Auditor ⚖️

An AI-powered web application that automates the review of legal contracts against company policies. Built with Python, Flask, LangChain, and Google's Gemini 3 Flash.

## Overview
The Legal Compliance Auditor acts as an intelligent assistant for legal teams. It ingests a target Vendor Contract and cross-references it against your internal Company Policies. Using a local Retrieval-Augmented Generation (RAG) architecture and the Gemini 3 Flash LLM, it extracts key clauses, compares requirements, and instantly flags high-risk discrepancies or compliance matches.

## Key Features
*   **Dual-Pane Dashboard:** A beautiful glassmorphism-styled UI built with Tailwind CSS that displays the original contract alongside the real-time AI audit report.
*   **Intelligent Cross-Referencing:** Extracts policy clauses and queries the target contract to detect missing mandatory stipulations or contradictory terms.
*   **Local Vector Store:** Uses `sentence-transformers` (`all-MiniLM-L6-v2`) and ChromaDB to chunk and index policy documents locally, ensuring blazing fast lookups.
*   **Gemini 3 Flash Integration:** Leverages Google's extremely fast LLM to summarize complex policy contexts and perform precise semantic comparisons.
*   **Automated Risk Flagging:** Automatically categorizes findings into 🔴 **High Risk** (e.g., 15-day termination instead of required 30-day) or 🟢 **Compliance Match**.

## Tech Stack
*   **Backend:** Python 3, Flask, Werkzeug
*   **AI/RAG:** LangChain, PyPDF2, ChromaDB, HuggingFace Embeddings
*   **LLM:** Google Generative AI (Gemini 3 Flash)
*   **Frontend:** HTML5, Vanilla JavaScript, Tailwind CSS (via CDN)

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Hashirrazzaq256/Legal-Compliance-Auditor.git
   cd Legal-Compliance-Auditor
   ```

2. **Create a Virtual Environment (Optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Create a `.env` file in the root directory and add your Google API Key:
   ```env
   GOOGLE_API_KEY="your_api_key_here"
   ```

5. **Generate Test Data (Optional):**
   Want to test the application immediately? Run the included script to generate dummy PDFs:
   ```bash
   python generate_pdfs.py
   ```

6. **Run the Application:**
   ```bash
   python app.py
   ```
   Navigate to `http://127.0.0.1:5000` in your browser.

## Usage
1. Open the web interface.
2. Upload the `Target Contract (PDF)` you wish to review.
3. Upload your standard `Company Policies Reference (PDF)`.
4. Click **Audit Contract**.
5. The LangChain agent will extract the text, build the vector store, and stream the cross-referenced audit report to the UI!

*(Note: If no files are uploaded, the application will automatically fallback to the local `/test_data` PDFs for simple demonstration purposes).*
