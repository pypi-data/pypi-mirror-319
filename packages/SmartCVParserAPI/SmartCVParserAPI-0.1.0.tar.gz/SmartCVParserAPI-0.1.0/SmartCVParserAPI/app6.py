import os
import csv
from flask import Flask, render_template, request, jsonify, send_from_directory
import re
import base64
import google.generativeai as genai
import json
import markdown
from PyPDF2 import PdfReader
app = Flask(__name__)

# Define file upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configure Google Generative AI with API key
genai.configure(api_key="AIzaSyBQqmwqkX3Oc1fhomRHMOZ737rPZI_wapE") #replace Your Api Key

# Function to parse the response
def parse_response(response_text):
    # Define regex patterns for fields
    patterns = {
        "Name": r"\*\*Name:\*\* (.*?)\n",
        "Email": r"\*\*Email:\*\* (.*?)\n",
        "Phone": r"\*\*Phone Number:\*\* (.*?)\n",
        "Education": r"\*\*Education:\*\*\n(.*?)\n\n",
        "Skills": r"\*\*Skills:\*\*\n(.*?)\n\n",
        "Projects": r"\*\*Projects:\*\*\n(.*?)\n\n",
        "Experience": r"\*\*Experience:\*\*\n(.*?)\n\n"
    }

    # Extract details into a dictionary

    details = {key: "Nil" for key in patterns}  # Default value for all keys
    for key, pattern in patterns.items():
        match = re.search(pattern, response_text, re.DOTALL)
        if match:
            extracted = match.group(1).strip()
            if key in ["Education", "Skills", "Projects", "Experience"]:
                extracted = extracted.replace("\n", " ").replace("*", "").strip()
            details[key] = extracted
    
    return details


# Function to extract resume data using Gemini API
def extract_with_gemini(file_path):
    try:
        # Read the file and encode it in base64
        with open(file_path, "rb") as file:
            doc_data = base64.standard_b64encode(file.read()).decode("utf-8")

        # Prepare the model request
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = "Extract the following details from the resume: Name, Email, Phone Number, Education, Skills, Projects, Experience."
        response = model.generate_content([{'mime_type': 'application/pdf', 'data': doc_data}, prompt])
        parsed_details = parse_response(response.candidates[0].content.parts[0].text)
        
        return parsed_details
    except Exception as e:
        print(f"Error using Gemini API: {e}")
        return ""
    
def process_folder(folder_path):
    extracted_data_list = []  # List to store extracted data from all resumes
    mechanical_data_list = []
    
    try:
        # Get all PDF files from the folder
        for filename in os.listdir(folder_path):
            if filename.lower().endswith('.pdf'):
                file_path = os.path.join(folder_path, filename)
                
                # Check the number of pages in the PDF
                try:
                    with open(file_path, 'rb') as file:
                        reader = PdfReader(file)
                        page_count = len(reader.pages)

                        # If the PDF has more than 3 pages, skip this file
                        if page_count > 3:
                            print(f"Skipping {filename} (more than 3 pages)")
                            continue  # Skip the current file and move to the next one
                except Exception as e:
                    print(f"Error reading {filename}: {e}")
                    continue  # Skip to the next file if error occurs
                
                # Extract resume details using Gemini API
                extracted_data = extract_with_gemini(file_path)
                
                # If data is extracted, append it to the list
                if extracted_data:
                    extracted_data['File'] = filename  # Adding filename to the extracted data
                    extracted_data_list.append(extracted_data)
                    # Filter for mechanical background
                    print(extracted_data.get("Skills", ""))
                    mechanical_skills = ["AutoCAD", "SolidWorks", "CATIA", "ANSYS", "MATLAB","FEA analysis", "CAD"]
                    if "Mechanical" in extracted_data.get("Education", "") or "Mechanical" in extracted_data.get("Experience", ""):
                        print("Found 'Mechanical' in Education or Experience")
                        
                        # Check for specific mechanical skills in the 'Skills' field
                        found_skills = [skill for skill in mechanical_skills if skill in extracted_data.get("Skills", "")]
                        
                        if found_skills:
                            print(f"Mechanical skills found: {', '.join(found_skills)}")
                        else:
                            print("No specific mechanical skills found")
                        
                        # Add data to the mechanical_data_list if conditions are satisfied
                        mechanical_data_list.append(extracted_data)

                else:
                    print(f"Failed to extract data from {filename}")
    except Exception as e:
        print(f"Error processing folder: {e}")
    return extracted_data_list, mechanical_data_list

def export_to_csv(data_list, filename, folder='uploads'):
    print("\n\ndata:\t ",data_list)

    os.makedirs(folder, exist_ok=True)
    csv_file_path = os.path.join(folder, filename)
    normalized_csv_file_path = os.path.normpath(csv_file_path).replace("\\", "/")
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["File", "Name", "Email", "Phone", "Education", "Skills", "Projects", "Experience"])
        for data in data_list:
            writer.writerow([data.get("File", "Nil"),
                             data.get("Name", "Nil"),
                             data.get("Email", "Nil"),
                             data.get("Phone", "Nil"),
                             data.get("Education", "Nil"),
                             data.get("Skills", "Nil"),
                             data.get("Projects", "Nil"),
                             data.get("Experience", "Nil")])


    return normalized_csv_file_path ,data


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        resume_file = request.files.get('resume')
        folder_url = request.form.get('folder_url')

        if resume_file:
            # Handle single resume file (same as before)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename)
            resume_file.save(file_path)

            if resume_file.filename.lower().endswith('.pdf'):
                try:
                    # Check the number of pages in the uploaded PDF
                    with open(file_path, 'rb') as file:
                        reader = PdfReader(file)
                        page_count = len(reader.pages)

                        if page_count > 3:
                            os.remove(file_path)
                            error_message = "Please upload a resume with less than 3 pages."
                            return render_template('index.html', error=error_message)
                except Exception as e:
                    os.remove(file_path)
                    error_message = f"Error reading the PDF file: {e}"
                    return render_template('index.html', error=error_message)

            extracted_data = extract_with_gemini(file_path)
            if not extracted_data:
                os.remove(file_path)
                error_message = "Failed to extract data from the resume. Please try again."
                return render_template('index.html', error=error_message)
            
            csv_filename_all = "all_extracted_resume_data.csv"
            csv_file_path_all , data= export_to_csv([extracted_data], csv_filename_all)
            # Export Mechanical Resume Data (if applicable)
            csv_filename_mechanical = None
            if "Mechanical" in extracted_data.get("Education", "") or "Mechanical" in extracted_data.get("Experience", ""):
                csv_filename_mechanical = "mechanical_extracted_resume_data.csv"
                csv_file_path_mechanical,data = export_to_csv([extracted_data], csv_filename_mechanical)
            return render_template('index.html', details=data,csv_filename=csv_filename_all, csv_filename_mechanical=csv_filename_mechanical)

        elif folder_url:
            # If folder URL is provided, process all resumes in the folder
            folder_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_url)
            extracted_data_list, mechanical_data_list = process_folder(folder_path)

            if not extracted_data_list:
                error_message = "No valid resumes found in the folder or failed to extract data."
                return render_template('index.html', error=error_message)

            # Export All Resumes Data
            csv_filename_all = "all_extracted_resumes_data.csv"
            csv_file_path_all ,data= export_to_csv(extracted_data_list, csv_filename_all)

            # Export Only Mechanical Resumes Data
            if mechanical_data_list:
                csv_filename_mechanical = None
                csv_filename_mechanical = "mechanical_extracted_resumes_data.csv"
                csv_file_path_mechanical,data = export_to_csv(mechanical_data_list, csv_filename_mechanical)    


            return render_template('index.html', details=data, csv_filename=csv_filename_all, csv_filename_mechanical=csv_filename_mechanical )

    return render_template('index.html')


# Function to interact with Gemini API
def interact_with_gemini(csv_file_path, prompt):
    try:
        # Read the previously generated CSV
        with open(csv_file_path, 'rb') as file:
            doc_data = base64.standard_b64encode(file.read()).decode("utf-8")
        
        # Prepare the model request
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Send the document data and prompt to the model
        response = model.generate_content([{'mime_type': 'text/csv', 'data': doc_data}, prompt])
        return response.text
    except Exception as e:
        return str(e)

# Additional helper functions for formatting
def format_response_text(response_text):
    if "- " in response_text:
        lines = response_text.splitlines()
        formatted = "<ul>" + "".join(f"<li>{line.strip('- ')}</li>" for line in lines if line) + "</ul>"
    else:
        formatted = f"<p>{response_text}</p>"
    return formatted

def format_json_response(response_text):
    try:
        parsed_json = json.loads(response_text)
        return f"<pre>{json.dumps(parsed_json, indent=4)}</pre>"
    except json.JSONDecodeError:
        return response_text

def format_markdown_output(response_text):
    return markdown.markdown(response_text)
    
@app.route("/interact", methods=["GET", "POST"])
def interact():
    output = None
    if request.method == "POST":
        prompt = request.form.get('prompt')
        if 'mechanical' in prompt.lower():
            csv_file_path = os.path.join('uploads', 'mechanical_extracted_resumes_data.csv')
        else:
            csv_file_path = os.path.join('uploads', 'all_extracted_resumes_data.csv')
                
        # Interact with Gemini
        try:
            raw_output = interact_with_gemini(csv_file_path, prompt)
            # Check the type of response and format accordingly
            if raw_output.startswith("{") or raw_output.startswith("["):  # JSON
                output = format_json_response(raw_output)
            elif "**" in raw_output or "_" in raw_output:  # Markdown
                output = format_markdown_output(raw_output)
            else:  # Plain text
                output = format_response_text(raw_output)
        except Exception as e:
            return jsonify({'error': f'Error generating response: {str(e)}'}), 500

    return render_template("interact.html", output=output)

def main():
    app.run(debug=True)

if __name__ == "__main__":
    main()
    
