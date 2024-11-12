import requests
import json
import time
import signal
import sys

CONTEST_ID = 2026
CONTEST_STANDINGS_FILE = f'./data/{CONTEST_ID}conteststandings.json'
RESUME_FILE = './data/resume.json'
RESULTS_FILE = './data/submission_ids_results.json'
API_BASE = "https://codeforces.com/api/"

def load_resume_data():
    """Load resume data if it exists, otherwise start fresh."""
    try:
        with open(RESUME_FILE, 'r', encoding='utf-8') as file:
            resume_data = json.load(file)
            return resume_data.get('contest_id', None), resume_data.get('row_index', 0), resume_data.get('current_handle', None)
    except (FileNotFoundError, json.JSONDecodeError):
        return None, 0, None  # Default values to start fresh

def save_resume_data(contest_id, row_index, current_handle):
    """Save current progress to resume.json."""
    resume_data = {
        "contest_id": contest_id,
        "row_index": row_index,
        "current_handle": current_handle
    }
    with open(RESUME_FILE, 'w', encoding='utf-8') as file:
        json.dump(resume_data, file, indent=4)

def save_results(handle, submissions):
    """Append submissions to results.json."""
    try:
        with open(RESULTS_FILE, 'r+', encoding='utf-8') as file:
            try:
                results = json.load(file)
            except json.JSONDecodeError:
                results = {}
            results[handle] = submissions
            file.seek(0)  # Move to start of the file to overwrite
            json.dump(results, file, indent=4)
            file.truncate()
    except FileNotFoundError:
        with open(RESULTS_FILE, 'w', encoding='utf-8') as file:
            json.dump({handle: submissions}, file, indent=4)

def fetch_submissions(contest_id, handle):
    """Fetch all submissions of a user (handle) for a specific contest."""
    url = f"{API_BASE}contest.status?contestId={contest_id}&handle={handle}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == "OK":
            return data['result']
    return []

def signal_handler(sig, frame):
    """Handle interruption signal (Ctrl+C) to save progress."""
    print("\nProcess interrupted. Saving progress...")
    sys.exit(0)

# Register signal handler for graceful exit on Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

def main():
    # Load contest standings
    with open(CONTEST_STANDINGS_FILE, 'r', encoding='utf-8') as file:
        standings = json.load(file)

    # Extract handlerows to iterate through handles
    handlerows = standings['rows']
    total_handles = len(handlerows)

    # Load the resume data if exists
    contest_id, row_index, current_handle = load_resume_data()
    if contest_id != CONTEST_ID:
        row_index, current_handle = 0, None  # Reset if contest ID does not match

    # Iterate over each handle in the standings
    for index in range(row_index, total_handles):
        handle = handlerows[index]['party']['members'][0]['handle']

        # Skip already processed handles
        if current_handle and handle != current_handle:
            continue
        
        print(f"Processing handle: {handle} (Contest ID: {CONTEST_ID}, Row: {index})")

        # Fetch submissions for the handle
        submissions = fetch_submissions(CONTEST_ID, handle)
        save_results(handle, submissions)  # Save submissions to results.json

        # Update resume point after each handle
        save_resume_data(CONTEST_ID, index, handle)
        current_handle = None  # Reset current handle after processing
        
        # Calculate and display progress
        progress_percentage = ((index + 1) / total_handles) * 100
        print(f"Progress: {progress_percentage:.2f}% completed")

        # Throttle API requests
        time.sleep(1)  # Adjust as necessary to respect API rate limits

    print("All handles processed.")

if __name__ == "__main__":
    main()
