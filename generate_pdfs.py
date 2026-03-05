import os
try:
    from fpdf import FPDF
except ImportError:
    print("fpdf not installed.")
    exit(1)

def create_pdf(filename, title, content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=title, ln=1, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=content)
    pdf.output(filename)

# 1. Company Policies
policies_text = """
COMPANY POLICIES DOCUMENT

1. TERMINATION POLICY
All vendor contracts must include a termination for convenience clause allowing the company to terminate the agreement with no more than 30 days prior written notice.

2. LIABILITY POLICY
The maximum liability cap for any vendor engagement shall not exceed $1,000,000 USD.

3. DATA PRIVACY POLICY
Any vendor handling company or customer data must ensure that all data is encrypted both in transit and at rest using AES-256 encryption or stronger.
"""

# 2. Target Contract
contract_text = """
VENDOR SERVICES AGREEMENT

This Agreement is entered into by and between Vendor and Company.

1. TERMINATION
This Agreement may be terminated by either party for convenience, provided that the terminating party provides at least 15 days prior written notice.

2. LIABILITY
Under no circumstances shall Vendor's total aggregate liability arising out of or related to this Agreement exceed the sum of $1,000,000 USD.

3. DATA HANDLING
Vendor agrees to implement reasonable security measures to protect data. Data will be encrypted during transit across public networks.
"""

if __name__ == "__main__":
    os.makedirs('test_data', exist_ok=True)
    create_pdf("test_data/policies.pdf", "Company Legal Policies", policies_text)
    create_pdf("test_data/contract.pdf", "Vendor Contract 2026", contract_text)
    print("Test PDFs generated successfully.")
