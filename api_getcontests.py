import requests
import json

# res = requests.get("https://codeforces.com/api/contest.list")
# jsonResponse = res.json()
# print(jsonResponse['result'])

# with open('contestlist.json', 'w', encoding='utf-8') as contestlist:
#     json.dump(jsonResponse['result'], contestlist)
try:
    with open('./data/contestlist.json', 'r', encoding='utf-8') as contestlist:
        data = json.load(contestlist)
    if not data:
        print("Contest file empty: Building Contest File...")
        raise FileNotFoundError("Contest file empty")
except(FileNotFoundError, json.decoder.JSONDecodeError):
    res = requests.get("https://codeforces.com/api/contest.list")
    jsonResponse = res.json()
    # print(jsonResponse['result'])

    with open('./data/contestlist.json', 'w', encoding='utf-8') as contestlist:
        json.dump(jsonResponse['result'], contestlist, indent=4)
    data = jsonResponse['result']

# for line in data:
#     with open('./data/resume_contest.json', 'w', encoding='utf-8') as resfile:
#         json.dump(line, resfile)
#     print(line)
#     break

try:
    with open('./data/resume_contest.json', 'r', encoding='utf-8') as resfile:
        contest_line = json.load(resfile)
    if not contest_line:
        raise FileNotFoundError("Resume file empty")
except(FileNotFoundError, json.decoder.JSONDecodeError):
    line = data[0]
    with open('./data/resume_contest.json', 'w', encoding='utf-8') as resfile:
        json.dump(line, resfile, indent=4)
        contest_line = line
    print(line)

if contest_line['phase'] != 'FINISHED':
    for line in data:
        if line['phase'] == 'FINISHED':
            with open('./data/resume_contest.json', 'w', encoding='utf-8') as resfile:
                json.dump(line, resfile, indent=4)
            # print(line)
            break
    contest_line = line
    print("--> NOW SCRAPING: \n\t" + str(contest_line))
else:
    print("--> RESUMING: \n\t" + str(contest_line))


try:
    with open('./data/'+str(contest_line['id'])+'conteststandings.json', 'r', encoding='utf-8') as conteststandings:
        standingsdata = json.load(conteststandings)
    print('--> Contest ' + str(contest_line['id']) + " standings found...")
except(FileNotFoundError, json.decoder.JSONDecodeError):
    print('--> Contest ' + str(contest_line['id']) + " standings not found: Creating new...")
    standingsres = requests.get("https://codeforces.com/api/contest.standings?contestId="+str(contest_line['id'])+"&from=1")
    standingsjsonResponse = standingsres.json()
    with open('./data/'+str(contest_line['id'])+'conteststandings.json', 'w', encoding='utf-8') as conteststandings:
        json.dump(standingsjsonResponse['result'], conteststandings, indent=4)
    standingsdata = standingsjsonResponse['result']
print('\t'+str(standingsdata['contest']))
# print(standingsjsonResponse['result'])


with open('./data/'+str(contest_line['id'])+'conteststandings.json', 'r', encoding='utf-8') as conteststandings:
        standingsdata = json.load(conteststandings)
handlerows = standingsdata['rows']
