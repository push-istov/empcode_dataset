from pyppeteer_stealth import stealth
from pyppeteer import launch
import pyppeteer
from bs4 import BeautifulSoup
import json
import ijson
import asyncio
import signal
import sys
import time
import os
import random

loginurl = 'https://codeforces.com/enter'
codetesturl = 'https://codeforces.com/contest/2018/submission/285418011'

username = "rythmtheif"
password = "anto!#$"

# username = "kadampushkar8@gmail.com"
# password = "ramenT-T3#8&!"

cookies_file = "cookies.json"

global_write_object = None

# Paths for files
SUBMISSION_IDS_FILE = './sample_data/submission_ids_and_handles_results.json'
OUTPUT_FILE = './sample_data/codes_dataset.json'
RESUME_FILE = './data/resume_code_2026.json'

async def bypass_cloudflare(url, browser, page):
    await stealth(page)  # Apply stealth mode to avoid detection
    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    )
    await page.goto(url, timeout=60000)
    await page.waitForSelector('body', timeout=60000)
    content = await page.content()
    return content

async def navtopage(url, browser, page):
    try:
        await page.goto(url, timeout=60000)
        # await page.waitForNavigation()
        await page.waitForSelector('body', timeout=60000)
        await asyncio.sleep(4.5)
        content = await page.content()
    except(TimeoutError, pyppeteer.errors.PageError):
        content = None
        raise TimeoutError
    return content

async def login(url, browser, page):
    await page.waitForSelector('input[id="handleOrEmail"]', visible=True)
    await page.type('input[id="handleOrEmail"]', username)
    print("login: Entered username as {}".format(username))

    await page.waitForSelector('input[name="password"]', visible=True)
    await page.type('input[name="password"]', password)
    print("login: Entered password as {}".format(password))

    await page.waitForSelector('input[type="submit"]', visible=True)
    await page.click('input[type="submit"]')
    print("login: Submit complete")

    await page.waitForNavigation(timeout=60000)
    await page.waitForSelector('body', timeout=60000)
    content = await page.content()
    loginerror = await page.querySelector('span[class="error for__password"]')
    if (loginerror):
        print("Login Error Occured")
    else:
        print("Login successful")
        cookies = await page.cookies()
        # print("Cookies:\n{}...".format(cookies[:500]))
        with open(cookies_file, 'w') as f:
            json.dump(cookies, f)
        print(f"Cookies saved to {cookies_file}")
    return content

def prettifyandWrite(contents, filepath):
    soup = BeautifulSoup(contents, 'html.parser')
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(soup.prettify())
    file.close()

def append_to_json_file(new_object, file_path):
    with open(file_path, 'r+', encoding='utf-8') as f:
        # Seek to the end of the file and check the size
        f.seek(0, 2)  # Move to the end of the file
        file_size = f.tell()
        
        # Check if the file is empty or not a valid JSON array
        if file_size == 0:
            print("File is empty or not a valid JSON array.")
            f.write("[]")
            file_size = f.tell()
        
        # Move to the second-to-last character
        f.seek(file_size - 1)  # -2 to skip the last ']'
        
        # Check if we are in a valid position and the last character is a closing bracket
        last_char = f.read(1)
        if last_char == ']':
            # The array is already complete, so we can safely add a new item
            # We move back one character to overwrite the last closing bracket
            f.seek(file_size - 1)
            
            # Write a comma (if there are items already in the array)
            if (file_size > 2):
                f.write(',')
            
            # Write the new object (in JSON format)
            json.dump(new_object, f)
            
            # Close the JSON array with a closing bracket
            f.write(']')
            print(f"Appended new object to {file_path}")
        else:
            print(last_char)
            print("The file does not end with a valid JSON array. Ensure the file is correctly formatted.")
            return

def getSource(contents, filepath):
    soup = BeautifulSoup(contents, 'html.parser')
    oltag = soup.find(attrs={"class":"linenums"})
    with open(filepath, 'w', encoding='utf-8') as fin:
        for litag in oltag.find_all("li"):
            for spantag in litag.find_all("span"):
                print(spantag.get_text(), end="")
                fin.writelines(spantag.get_text())
            print()
            fin.writelines("\n")
    fin.close()

def returnSource(contents):
    soup = BeautifulSoup(contents, 'html.parser')
    oltag = soup.find(attrs={"class":"linenums"})
    code_ext = ""
    if oltag is None:
        print("Error: Code block with class 'linenums' not found in the page content.")
        return None  # Return an empty string or handle it as needed
    for litag in oltag.find_all("li"):
        for spantag in litag.find_all("span"):
            # print(spantag.get_text(), end="")
            code_ext += spantag.get_text()
        # print()
        code_ext += "\n"
    return code_ext

def load_resume_data():
    """Load resume data if it exists, otherwise start fresh."""
    try:
        with open(RESUME_FILE, 'r', encoding='utf-8') as file:
            resume_data = json.load(file)
            return resume_data.get('submission_id', None), resume_data.get('current_handle', None)
    except (FileNotFoundError, json.JSONDecodeError):
        return None, None  # Default values to start fresh

def save_resume_data(submission_id, current_handle):
    """Save current progress to resume.json."""
    resume_data = {
        "submission_id": submission_id,
        "current_handle": current_handle
    }
    with open(RESUME_FILE, 'w', encoding='utf-8') as file:
        json.dump(resume_data, file, indent=4)

def restore_resume_data(current_handle):
    last_object = None  # Initialize last_object to None
    try:
        with open(OUTPUT_FILE, 'r+', encoding='utf-8') as op_file:
            resume_check = json.load(op_file)
            for row_data in resume_check:
                if row_data["handle"] == current_handle:
                    last_object = row_data
                    del row_data
            # last_object = resume_check[-1]
            # del resume_check[-1]
    except(FileNotFoundError, json.JSONDecodeError):
        return None
    return last_object

def signal_handler(sig, frame):
    """Handle interruption signal (Ctrl+C) to save progress."""
    print("\nProcess interrupted. Saving progress...")
    append_to_json_file(global_write_object, OUTPUT_FILE)
    print("Write complete")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

async def main():
    browser = await launch(headless=True, args=['--no-sandbox'])
    page = await browser.newPage()
    if os.path.exists(cookies_file):
            print("Cookies Found: Attempting to login with Cookies...")
            with open(cookies_file, 'r') as f:
                cookies = json.load(f)
                try:
                    await page.setCookie(*cookies)
                    test_contents = await navtopage(codetesturl, browser, page)
                    test_soup = BeautifulSoup(test_contents, 'html.parser')
                    oltag = test_soup.find(attrs={"class":"linenums"})
                    if oltag is None:
                        raise TimeoutError
                    print("Success...")
                except(TimeoutError):
                    print("Timed out logging in...")
                    await browser.close()
                    browser = await launch(headless=True, args=['--no-sandbox'])
                    page = await browser.newPage()
                    contents = await bypass_cloudflare(loginurl, browser, page)
                    logincontent = await login(loginurl, browser, page)
    else:
        contents = await bypass_cloudflare(loginurl, browser, page)
        logincontent = await login(loginurl, browser, page)
    
    try:
        with open(SUBMISSION_IDS_FILE, 'r', encoding='utf-8') as sub_id_file:
            data = json.load(sub_id_file)
    except(FileNotFoundError, json.decoder.JSONDecodeError):
        print("Submissions file empty")
        return
    
    submission_id, current_handle = load_resume_data()
    write_object = restore_resume_data(current_handle)
    global_write_object = write_object
    for handle in data:
        if not current_handle:
            current_handle = handle
        if not (handle == current_handle):
            continue
        if not write_object:
            write_object = {"handle": handle, "submission_list":[]}
            global_write_object = write_object
        for submission in data[handle]:
            if not submission_id:
                submission_id = submission['id']
            if not (submission_id == submission['id']):
                continue
            
            sub_id = submission['id']
            contest_id = submission['contestId']
            row_data = submission
            submission_url = 'https://codeforces.com/contest/' + str(contest_id) + '/submission/' + str(sub_id)


            # with open('./data/resume_code_2026.json', 'w', encoding='utf-8') as resume_file:
            #     json.dump(row_data, resume_file)
            save_resume_data(sub_id, handle)
            print("SCRAPING: " + handle + " --> "+ submission_url)
            i=10
            while(i >= 0):
                try:
                    contents = await navtopage(codetesturl, browser, page)
                except(TimeoutError) as e:
                    # with open(OUTPUT_FILE, 'a', encoding='utf-8') as op_file:
                    #     json.dump(write_object, op_file)
                    append_to_json_file(write_object, OUTPUT_FILE)
                    print("Write complete")
                    print("Timeout encountered saving and quitting")
                    return
                print("SUCCESS: " + handle + " --> "+ submission_url)
                code_extract = returnSource(contents)
                if not code_extract:
                    print(f"Empty page, retrying {handle} --> ({i}) more times.. {submission_url}")
                    i-=1
                else:
                    break
            if not code_extract:
                append_to_json_file(write_object, OUTPUT_FILE)
                print("Write complete")
                print("Empty page returned saving and quitting")
                return
            # print("LE CODE: " + code_extract)

            row_data["code"] = code_extract
            write_object["submission_list"].append(row_data)
            global_write_object = write_object
            submission_id = None
        # with open(OUTPUT_FILE, 'a', encoding='utf-8') as op_file:
        #     json.dump(write_object, op_file)
        append_to_json_file(write_object, OUTPUT_FILE)
        print("Write complete")
        write_object = None
        current_handle = None
        time.sleep(random.uniform(2, 4.5))

    await browser.close()
    # prettifyandWrite(contents, 'op.txt')
    prettifyandWrite(logincontent, 'loginlog.txt')

asyncio.get_event_loop().run_until_complete(main())
