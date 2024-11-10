import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup
import json

def prettifyandRead(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
    file.close()
    return soup

async def main():
    soup = prettifyandRead('op.txt')
    oltag = soup.find(attrs={"class":"linenums"})
    srccode = ""
    with open("fin.txt", 'w', encoding='utf-8') as fin:
        for litag in oltag.find_all("li"):
            for spantag in litag.find_all("span"):
                # print(spantag.get_text(), end="")
                srccode += spantag.get_text()
                # fin.writelines(spantag.get_text())
            # print()
            srccode += "\n"
            # fin.writelines("\n")
        
    fin.close()
    print(srccode)
    with open('fin2.json', 'w', encoding='utf-8') as f:
            json.dump(srccode, f)
    f.close()

asyncio.get_event_loop().run_until_complete(main())
