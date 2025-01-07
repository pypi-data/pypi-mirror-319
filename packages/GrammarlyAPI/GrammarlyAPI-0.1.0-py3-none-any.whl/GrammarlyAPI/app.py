import os
import base64
import re
import pandas as pd
from flask import Flask, render_template, request, send_file
import google.generativeai as genai

# Initialize Flask app
app = Flask(__name__)

# Configure the Gemini API with your API key
genai.configure(api_key="AIzaSyBQqmwqkX3Oc1fhomRHMOZ737rPZI_wapE")
model = genai.GenerativeModel("gemini-1.5-flash")

# Folder to save uploaded files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def check_grammar(file_path):
    """Send the content of the file to the Gemini API for grammar checking."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    
    # Read and encode the file
    with open(file_path, "rb") as doc_file:
        doc_data = base64.standard_b64encode(doc_file.read()).decode("utf-8")
    # Define the prompt
    prompt = "Analyze the given sentences for grammatical correctness and formality. If the sentence is correct and formal, return it as is. If it contains grammatical errors or formality issues, return both the original sentence and the corrected sentence along with a brief explanation of what was corrected (e.g., grammar fix, verb change, formality improvements)"
    
    try:
        print("data",type(doc_data))
        response = model.generate_content([{'mime_type': 'text/csv', 'data': doc_data}, prompt])
        print("response",response)
        return response
    except Exception as e:
        raise RuntimeError(f"Error calling the Gemini API: {e}")

def extract_corrections(response):
    """Extract original, corrected sentences, and explanations from the API response."""
    if not response:
        raise ValueError("Empty response received from the API.")
    if hasattr(response, '_result') and response._result:
        candidates = response._result.candidates if response._result else []
        
        if candidates:
            content = candidates[0].content if candidates[0] else {}
            parts = content.parts if content else []
            
            if parts:
                text = ''.join(part.text for part in parts)
                # Regex to extract original, corrected sentences, and explanations
                pattern = r"\*\*Original:\*\*\s*(.*?)\n\s*\*\*Corrected:\*\*\s*(.*?)\s*\(.*?\)"
                corrections = re.findall(pattern, text)
                explanations = re.findall(r"\*\*Corrected:\*\*\s.*\((.*?)\)", text)
                
                if corrections:
                    return [
                        {'Original Sentence': orig.strip(), 
                         'Corrected Sentence': corr.strip(),
                         'Explanation': expl.strip() if expl else ""}
                        for (orig, corr), expl in zip(corrections, explanations)
                    ]
    
    raise ValueError("No valid text content found in the response.")

# Other functions (check_grammar, extract_corrections, etc.) remain unchanged.

def process_file(file_path):
    """Process the uploaded file, check grammar, and update the DataFrame."""
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path,encoding='ISO-8859-1')
        elif file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path,encoding='ISO-8859-1')
        elif file_path.endswith('.txt'):
            with open(file_path, 'r',encoding='utf-8') as f:
                file_text = f.read()
            df = pd.DataFrame(file_text.splitlines(), columns=['Original_Text'])
        else:
            raise ValueError("Unsupported file format. Use .csv, .xlsx, or .txt")
    except Exception as e:
        print(f"Error in file processing: {e}")

    try:
        response = check_grammar(file_path)
    except Exception as e:
        raise RuntimeError(f"Error in grammar checking: {e}")
    
    try:
        corrections = extract_corrections(response)
    except Exception as e:
        raise RuntimeError(f"Error extracting corrections: {e}")
    
    df['Corrected Sentence'] = ''
    for i, correction in enumerate(corrections):
        if i < len(df):
            df.at[i, 'Corrected Sentence'] = correction['Corrected Sentence']

    

    df = df[['Original_Text', 'Corrected Sentence']]
    output_file = file_path.replace('.csv', '_corrected.csv').replace('.txt', '_corrected.csv').replace('.xlsx', '_corrected.xlsx')
    
    if output_file.endswith('.csv'):
        df.to_csv(output_file, index=False)
    else:
        df.to_excel(output_file, index=False)
    
    print("before html",df)
    return output_file, df  # Return file path and df

@app.route("/")
def index():
    return render_template("index.html", df=None)

@app.route("/check_grammar", methods=["POST"])
def check_grammar_endpoint():
    if 'file' not in request.files:
        return render_template("index.html", error="No file uploaded", df=None)
    
    file = request.files['file']
    if file.filename == '':
        return render_template("index.html", error="No selected file", df=None)

    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        try:
            output_file, df = process_file(file_path)
            print(output_file)
            print(df)
            return render_template("index.html", df=df.to_dict(orient='records'), file_url=output_file)
        except Exception as e:
            return render_template("index.html", error=str(e), df=None)

@app.route("/download_file/<filename>")
def download_file(filename):
    return send_file(filename, as_attachment=True)

def main():
    """Entry point for the app."""
    app.run(debug=True)

if __name__ == "__main__":
    main()
