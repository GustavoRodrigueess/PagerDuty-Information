import sys
import json
import requests
from datetime import datetime, timedelta

# This box returned inside an empty function, if there is a return field inside an empty function.
def key_exist(text: str): 
    if log_entries["log_entry"]["channel"]["details"] == None:
        pass
    else:
        incident[text] = log_entries ["log_entry"]["channel"]["details"].get(text, "")

# The replace function will do the same as "key_exist" but if there are escape characters, it will replace them with normal characters, as the escaped ones break the worksheet.
def replace(text: str):
    if log_entries["log_entry"]["channel"]["details"] == None:
        pass
    elif text in log_entries["log_entry"]["channel"]["details"]:
        text = log_entries["log_entry"]["channel"]["details"][text]
        text = text.replace('\n','')
        text = text.replace('\r','')
        text = text.replace(',',' ')
        incident[text] = text

token = input("Enter the token: ")

date = int(input("Enter how many days ago you want to check: "))

yesterday = datetime.now() - timedelta(date)
d = datetime.strftime(yesterday, '%Y-%m-%d')

offset = 0
url = "https://api.pagerduty.com/incidents"
filename = "pagerduty.csv"

headers = {
    "Content-Type": "application/json",
    "Accept": "application/vnd.pagerduty+json;version=2",
    "Authorization": "Token token=" + token
}

content = []
ids = []

if not token or token == "":
    print("The token was filled in incorrectly :(")
    sys.exit()

print("Looking for incidents...")

while True:

    querystring = {"limit":"100","offset":str(offset),"total":"true","sort_by":"created_at:desc","since":d}
    response = requests.request("GET", url, headers=headers, params=querystring)
    incidents = response.json()

    for i in incidents['incidents']:

        incident = {}
        key_log_entries = {}

        if i["incident_number"] in ids:
            continue

        ids.append(i["incident_number"])
        incident["incident_number"] = i["incident_number"]
        incident["title"] = i["title"].replace('\n', '\\n')
        incident["description"] = i["description"].replace('\n', '\\n')
        incident["created_at"] = i["created_at"]
        incident["status"] = i["status"]
        incident["summary"] = i["summary"].replace('\n', '\\n')
        incident["type"] = i["type"]
        incident["urgency"] = i["urgency"]
        incident["service-summary"] = i["service"]["summary"].replace('\n', '\\n')
        key_log_entries["first_trigger_log_entry-id"] = i["first_trigger_log_entry"]["id"].replace('\n', '\\n')

        # Esta nova URL (newurl) serve para fazer uma nova chamada de API para retorno do "show details"
        newurl = f"https://api.pagerduty.com/log_entries/{key_log_entries['first_trigger_log_entry-id']}?include[]=channels"

        logresponse = requests.request("GET", newurl, headers=headers)
        log_entries = logresponse.json()
        
        if "channel" in log_entries["log_entry"].keys():

            key_exist("Event date")

            key_exist("Event host")

            key_exist("Event host ip")

            key_exist("Event tags")

            key_exist("Event time")

            key_exist("Trigger opdata")

            key_exist("check_id")

            key_exist("check_name")

            key_exist("hostname")

            key_exist("long_description")

            key_exist("tags")

            key_exist("Total Records")

            key_exist("uptime_173")

            key_exist("uptime_174")

            key_exist("avg")

            replace("Trigger description")

            print(f'Producing incident number statistics: {incident["incident_number"]}')
        
        content.append(incident)

    offset += 1

    if not incidents["more"]:
        break

print("Generated file [ {} ]".format(filename))
f = open(filename, "w")

f.write("incident_number, title, description, created_at, status, summary, type, urgency, service-summary, Event date, Event host, Event host ip, Event tags, Event time, Trigger opdata, check_id, check_name, hostname, long_description, tags, Total Records, uptime_173, uptime_174, avg, Trigger description\n")
for i, val in enumerate(content):
    f.write("{}\n".format(','.join(map(str, list(val.values())))))
f.close()
