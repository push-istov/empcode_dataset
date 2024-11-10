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

async def main():
    browser = await launch(headless=True, args=['--no-sandbox'])
    page = await browser.newPage()
    contents = await bypass_cloudflare(loginurl, browser, page)
    logincontent = await login(loginurl, browser, page)
    contents = await navtopage(codetesturl, browser, page)
    await browser.close()
    prettifyandWrite(contents, 'op.txt')
    prettifyandWrite(logincontent, 'loginlog.txt')

asyncio.get_event_loop().run_until_complete(main())
