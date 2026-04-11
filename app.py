import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from rag_agent import execute_audit

load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def is_pdf_file(uploaded_file):
    if not uploaded_file or not uploaded_file.filename:
        return False
    return uploaded_file.filename.lower().endswith('.pdf')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/audit', methods=['POST'])
def audit_contract():
    contract_file = request.files.get('contract')
    policies_file = request.files.get('policies')
    has_contract = bool(contract_file and contract_file.filename)
    has_policies = bool(policies_file and policies_file.filename)
    
    # Fallback to test data if files aren't provided (for automated demo recording)
    if not has_contract and not has_policies:
        contract_path = 'test_data/contract.pdf'
        policies_path = 'test_data/policies.pdf'
        cleanup = False
    else:
        if not has_contract or not has_policies:
            return jsonify({'error': 'Please upload both contract and policies PDFs.'}), 400
        if not is_pdf_file(contract_file) or not is_pdf_file(policies_file):
            return jsonify({'error': 'Only PDF files are supported.'}), 400
        contract_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(contract_file.filename))
        policies_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(policies_file.filename))
        contract_file.save(contract_path)
        policies_file.save(policies_path)
        cleanup = True
    
    try:
        # Run the RAG workflow
        results = execute_audit(contract_path, policies_path)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Cleanup only if we actually saved uploaded files
        if cleanup:
            if os.path.exists(contract_path):
                os.remove(contract_path)
            if os.path.exists(policies_path):
                os.remove(policies_path)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
