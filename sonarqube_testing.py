import json
import os
import requests
import time
from pathlib import Path

# Configuration - Update these with your project and SonarQube details
SONARQUBE_URL = "http://localhost:9000"
SONARQUBE_TOKEN = "sqp_2a0cd2a8ffb969bb03e637af9d6d6a71b3d6a3b7"
PROJECT_KEY = "emp_dataset"

# File paths
input_json_file = "./sample_data/codes_dataset.json"
output_json_file = "./sample_data/sonarqube_analysis_results.json"

# Function to analyze code with SonarQube
def analyze_with_sonarqube(code_snippet, filename):
    # Create a temporary file with the code snippet
    temp_file = f"{filename}.cpp"
    with open(temp_file, 'w') as f:
        f.write(code_snippet)
    
    # Run SonarScanner on the temporary file
    os.system(f"sonar-scanner -Dsonar.projectKey={PROJECT_KEY} -Dsonar.sources=. -Dsonar.host.url={SONARQUBE_URL} -Dsonar.login={SONARQUBE_TOKEN}")
    
    # Clean up the temporary file
    os.remove(temp_file)
    
    # Wait for SonarQube to finish analysis
    time.sleep(5)
    
    # Fetch the analysis results from SonarQube
    response = requests.get(f"{SONARQUBE_URL}/api/issues/search?componentKeys={PROJECT_KEY}", auth=(SONARQUBE_TOKEN, ""))
    if response.status_code == 200:
        return response.json()  # Return the analysis results as JSON
    else:
        print("Failed to retrieve analysis from SonarQube.")
        return {}

# Main processing function
def process_json(input_file, output_file):
    # Read the input JSON
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    # Prepare output data
    results = {"handle": data["handle"], "submission_analysis": []}
    
    # Process each submission
    for submission in data["submission_list"]:
        code_snippet = submission.get("code", "")
        filename = f"submission_{submission['id']}"
        
        # Analyze code with SonarQube and get results
        analysis_results = analyze_with_sonarqube(code_snippet, filename)
        
        # Append the SonarQube results to each submission entry
        submission_result = {
            "id": submission["id"],
            "contestId": submission["contestId"],
            "problem": submission["problem"],
            "analysis": analysis_results
        }
        results["submission_analysis"].append(submission_result)
    
    # Write the output JSON
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=4)

# Run the processing function
process_json(input_json_file, output_json_file)
