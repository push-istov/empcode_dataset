from pyppeteer_stealth import stealth
from pyppeteer import launch
from bs4 import BeautifulSoup
import json
import asyncio

loginurl = 'https://codeforces.com/enter'
codetesturl = 'https://codeforces.com/contest/2018/submission/285418011'

username = "rythmtheif"
password = "anto!#$"
cookies_file = "cookies.json"

# Paths for files
SUBMISSION_IDS_FILE = './sample_data/submission_ids_and_handles_results.json'
OUTPUT_FILE = './sample_data/codes_dataset.json'
RESUME_FILE = './data/resume_code_2026.json'

async def bypass_cloudflare(url, browser, page):
    await stealth(page)  # Apply stealth mode to avoid detection
    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    )
    await page.goto(url)
    await page.waitForSelector('body', timeout=60000)
    content = await page.content()
    return content

async def navtopage(url, browser, page):
    await page.goto(url)
    # await page.waitForNavigation()
    await page.waitForSelector('body', timeout=60000)
    content = await page.content()
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

    await page.waitForNavigation()
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
    for litag in oltag.find_all("li"):
        for spantag in litag.find_all("span"):
            print(spantag.get_text(), end="")
            code_ext += spantag.get_text()
        print()
        code_ext += "\n"
    return code_ext

def load_resume_data():
    """Load resume data if it exists, otherwise start fresh."""
    try:
        with open(RESUME_FILE, 'r', encoding='utf-8') as file:
            resume_data = json.load(file)
            return resume_data.get('submission_id', None), resume_data.get('current_handle', None)
    except (FileNotFoundError, json.JSONDecodeError):
        return None, 0, None  # Default values to start fresh

def save_resume_data(submission_id, current_handle):
    """Save current progress to resume.json."""
    resume_data = {
        "submission_id": submission_id,
        "current_handle": current_handle
    }
    with open(RESUME_FILE, 'w', encoding='utf-8') as file:
        json.dump(resume_data, file, indent=4)

async def main():
    browser = await launch(headless=True, args=['--no-sandbox'])
    page = await browser.newPage()
    contents = await bypass_cloudflare(loginurl, browser, page)
    logincontent = await login(loginurl, browser, page)
    
    try:
        with open(SUBMISSION_IDS_FILE, 'r', encoding='utf-8') as sub_id_file:
            data = json.load(sub_id_file)
        if not contest_line:
            raise FileNotFoundError("Submissions list empty")
    except(FileNotFoundError, json.decoder.JSONDecodeError):
        print("Submissions file empty")
        return

    submission_id, current_handle = load_resume_data()
    for handle in data:
        if not current_handle:
            current_handle = handle
        if not (handle == current_handle):
            continue
        write_object = {"handle": handle, "submission_list":[]}
        for submission in data[handle]:
            if not submission_id:
                submission_id = submission['id']
            if not (submission_id == submission['id']):
                continue
            sub_id = submission['id']
            contest_id = submission['contestId']
            row_data = submission
            submission_url = 'https://codeforces.com/contest/' + str(contest_id) + '/submission/' + str(sub_id)

            with open('./data/resume_code_2026.json', 'w', encoding='utf-8') as resume_file:
                json.dump(row_data, resume_file)
            print("SCRAPING: " + submission_url)
            
            contents = await navtopage(codetesturl, browser, page)
            code_extract = returnSource(contents)
            print("LE CODE: " + code_extract)

            row_data["code"] = code_extract
            write_object["submission_list"].append(row_data)
            
        
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as op_file:
            json.dump(write_object, op_file)
            print("Write complete")
        break

    await browser.close()
    # prettifyandWrite(contents, 'op.txt')
    prettifyandWrite(logincontent, 'loginlog.txt')

asyncio.get_event_loop().run_until_complete(main())
