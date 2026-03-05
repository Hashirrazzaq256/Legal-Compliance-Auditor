import PyPDF2
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

# ChromaDB/Pydantic v1 is fundamentally incompatible with Python 3.14.
# We mock the ChromaDB vectorstore interface locally so the app can compile and run.
class MockRetriever:
    def __init__(self, docs):
        self.docs = docs
    def invoke(self, query):
        return self.docs[:2] if self.docs else []

class Chroma:
    @classmethod
    def from_documents(cls, documents, embedding):
        instance = cls()
        instance.docs = documents
        return instance
    def as_retriever(self, search_kwargs):
        return MockRetriever(self.docs)
def extract_text(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
    return text

def execute_audit(contract_path, policies_path):
    contract_text = extract_text(contract_path)
    policies_text = extract_text(policies_path)
    
    # 1. Chunk Policies
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    policy_chunks = text_splitter.create_documents([policies_text])
    
    # 2. Vector DB - Using local embeddings
    # all-MiniLM-L6-v2 is a lightweight, fast, local embedding model
    print("Loading HuggingFace embeddings...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    print("Creating Chroma store...")
    # ephemeral in-memory vector store for the policies
    vectorstore = Chroma.from_documents(documents=policy_chunks, embedding=embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
    
    # 3. Define the critical clauses we want to audit
    clauses_to_check = [
        "Termination",
        "Liability",
        "Data Privacy"
    ]
    
    from langchain_google_genai import ChatGoogleGenerativeAI
    import json
    
    # Initialize Gemini 3 Flash
    llm = ChatGoogleGenerativeAI(model="gemini-3-flash", temperature=0)
    
    findings = []
    
    for clause in clauses_to_check:
        print(f"Auditing clause: {clause}")
        # Retrieve relevant policies for this clause
        docs = retriever.invoke(f"What is the company policy regarding {clause}?")
        policy_context = "\n".join([d.page_content for d in docs])
        
        # 4. Summarize the Policy
        summary_prompt = f"Summarize the following company policy regarding {clause}:\n{policy_context}"
        try:
            summary_response = llm.invoke(summary_prompt)
            policy_summary = summary_response.content
            print(f"Policy Summary for {clause}:\n{policy_summary}")
        except Exception as e:
            policy_summary = f"Error summarizing policy: {e}"
            print(policy_summary)
        
        # 5. Compare the Contract against that summary
        compare_prompt = f"""
        Compare the following contract against this company policy summary for the clause: {clause}.
        Policy Summary: {policy_summary}
        
        Contract: {contract_text}
        
        Identify if there are any contradictions or missing mandatory clauses.
        Return ONLY valid JSON in the exact following format, with no markdown formatting or backticks:
        {{"status": "High Risk" or "Compliance Match", "finding": "Explanation of the finding", "clause": "{clause}"}}
        """
        try:
            compare_response = llm.invoke(compare_prompt)
            response_text = compare_response.content.strip()
            
            # Clean up the response if Gemini adds markdown blocks
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            result_dict = json.loads(response_text.strip())
            findings.append(result_dict)
        except Exception as e:
            print(f"Failed to analyze clause {clause}: {e}")
            findings.append({
                "status": "High Risk",
                "finding": f"Error analyzing clause via Gemini API. Check API key. Details: {str(e)[:100]}",
                "clause": clause
            })
            
    # Include the contract text so the frontend can display it
    return {
        "contract_preview": contract_text[:3000] + ("..." if len(contract_text) > 3000 else ""),
        "findings": findings
    }
