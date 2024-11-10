import requests
from bs4 import BeautifulSoup

cookies = {
    'X-User-Sha1': '',
    'cf_clearance': 'E_PBoAbtEgg61Vb5V3C7HWKUeM_5Bu_Sz268j00X_Ik-1729493781-1.2.1.1-rrVM66MxXvHTmnnyN0H6xCozm1XkQ7cfFT2Le2gErKDadtn2O.qX4NNWJMkTibuNsu.66U0J0J.Kt4SdudDAGyMfuVqKXiAbSI8Y7XJmdEkd6Hnx6gQVUH.baq5OmV4jQ_GNQjX_SZOvKmi054Unhi4Zr1i4GHBrnn8.YAKxZwGJDOTMvw1rK8BcdDbs1xMo6DiDKAgkqc5ePVn3YvIOOoyVbjwH1uzkIPJZ73IsvBLQ21FZC8RBL1JfVCka2de0T1abXRmZ5pIgh44lSVMihlzwQBg.49vRr_6OQ4HChaZ6xDVHspoYBBVvb0vhxVUn2TWf4_Fmgy9FCZq9w7V_pw',
    'JSESSIONID': '10E317ED32602811B35F53D39DAEC592',
    'lastOnlineTimeUpdaterInvocation': '1726893403539',
    '39ce7': 'CFWpzmNQ',
    'evercookie_etag': 'y4gresqh0dvbe0vei8',
    'evercookie_cache': 'y4gresqh0dvbe0vei8',
    'evercookie_png': 'y4gresqh0dvbe0vei8',
    '70a7c28f3de': 'y4gresqh0dvbe0vei8',
    'pow': '7f88b1659b923902b3743a51e10b72e15f570fd2',
    'X-User': '',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'Connection': 'keep-alive',
    # 'Cookie': 'X-User-Sha1=; cf_clearance=E_PBoAbtEgg61Vb5V3C7HWKUeM_5Bu_Sz268j00X_Ik-1729493781-1.2.1.1-rrVM66MxXvHTmnnyN0H6xCozm1XkQ7cfFT2Le2gErKDadtn2O.qX4NNWJMkTibuNsu.66U0J0J.Kt4SdudDAGyMfuVqKXiAbSI8Y7XJmdEkd6Hnx6gQVUH.baq5OmV4jQ_GNQjX_SZOvKmi054Unhi4Zr1i4GHBrnn8.YAKxZwGJDOTMvw1rK8BcdDbs1xMo6DiDKAgkqc5ePVn3YvIOOoyVbjwH1uzkIPJZ73IsvBLQ21FZC8RBL1JfVCka2de0T1abXRmZ5pIgh44lSVMihlzwQBg.49vRr_6OQ4HChaZ6xDVHspoYBBVvb0vhxVUn2TWf4_Fmgy9FCZq9w7V_pw; JSESSIONID=10E317ED32602811B35F53D39DAEC592; lastOnlineTimeUpdaterInvocation=1726893403539; 39ce7=CFWpzmNQ; evercookie_etag=y4gresqh0dvbe0vei8; evercookie_cache=y4gresqh0dvbe0vei8; evercookie_png=y4gresqh0dvbe0vei8; 70a7c28f3de=y4gresqh0dvbe0vei8; pow=7f88b1659b923902b3743a51e10b72e15f570fd2; X-User=',
    'Sec-GPC': '1',
    'Priority': 'u=0, i',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}

response = requests.get('https://codeforces.com/enter', cookies=cookies, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
print(soup.prettify())