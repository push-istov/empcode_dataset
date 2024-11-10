import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup

async def main():
    browser = await launch(headless=True)  # Launch headless browser
    page = await browser.newPage()

    # Navigate to the website
    await page.goto('https://codeforces.com/enter')

    # Wait for the JavaScript to execute (optional)
    await page.waitForSelector('body')

    # Get the rendered HTML after JavaScript has run
    content = await page.content()
    soup = BeautifulSoup(content, 'html.parser')
    print(soup.prettify())
    # print(content)

    with open('op.txt', 'a') as file:
        file.write(soup.prettify())
    file.close()
    # Close the browser
    await browser.close()

# Run the async function
asyncio.get_event_loop().run_until_complete(main())
