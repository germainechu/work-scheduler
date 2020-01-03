from subprocess import check_output
import argparse
import requests
import json
import time
import datetime
from ics import Calendar, Event


def toEvent(begindate, enddate):
    begindate += datetime.timedelta(hours=7)
    enddate += datetime.timedelta(hours=7)
    beginstr = begindate.strftime("%Y-%m-%d %H:%M:%S")
    endstr = enddate.strftime("%Y-%m-%d %H:%M:%S")
    event = Event()
    event.name = "Fairmont PacRim Work"
    event.begin = beginstr
    event.end = endstr
#    print(event.begin)
#    print(event.end)
    return event
    
#event = toEvent(datetime.datetime(2019, 10, 20, 9), datetime.datetime(2019, 10, 20, 16))
#print(event)

parser = argparse.ArgumentParser(description="Convert Brian's PDF calendar to ics!")
parser.add_argument('pdfpath', metavar='PDF')

args = parser.parse_args()

files = {
    'source_file': ('brian.pdf', open('brian.pdf', 'rb')),
    'target_format': (None, 'csv'),
}

url = "https://sandbox.zamzar.com/v1/"
api_key = "55d1a013a8264cf82d6c6216bd6371d5c1277bcf"

response = requests.post(url + "jobs", files=files, auth=(api_key, ''))

res = json.loads(response.content)
print(res)
job_id = res["id"]

while True:
    res = json.loads(requests.get(url + "jobs/" + str(job_id), auth=(api_key, '')).content)
    if res["status"] == "successful":
        target_id = res["target_files"][0]["id"]
        break
    time.sleep(1)

csv = requests.get(url + "files/" + str(target_id) + "/content", auth=(api_key, '')).content

rows = list(map(lambda x: x.decode(), csv.splitlines()))
rows = list(map(lambda x: x.split(','), rows))

months = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "June": "06", "July": "07", "Aug": "08", "Sept": "09", "Oct": "10", "Nov": "11", "Dec": "12"}

year = datetime.datetime.now().year
dates = list(map(lambda x: str(year) + "-" + months[x.split('-')[1]] + "-" + x.split('-')[0], rows[1][1:]))

invalid_timeslot = ["OFF", "N/A", "VAC", "REQ"]
invalid_name = ["HOUSEMEN","Servers","Part Time","Casual"]


for row in rows[2:]:
    name = row[0]
    if name != "BRIAN": continue
    if name in invalid_name: continue
    cal = Calendar()
    print(name)
    for j, timeslot in enumerate(row[1:]):
        if timeslot in invalid_timeslot or ":" not in timeslot: continue
        print(timeslot)
        startslot = timeslot.split("-")[0].strip()
        endslot = timeslot.split("-")[1].strip().split(" ")[0]
        beginhour = int(startslot.split(":")[0])
        beginminute = int(startslot.split(":")[1])
        begindate = datetime.datetime(year, int(dates[j].split("-")[1]), int(dates[j].split("-")[2]), beginhour, beginminute)

        endhour = int(endslot.split(":")[0])
        endminute = int(endslot.split(":")[1])


        if endhour < begindate.hour:
            hourdelta = 24 - begindate.hour + endhour
        else:
            hourdelta = endhour - begindate.hour

        minutedelta = endminute - begindate.minute

        if minutedelta < 0:
            hourdelta -= 1
            minutedelta += 60

        delta = datetime.timedelta(hours=hourdelta, minutes=minutedelta)
        event = toEvent(begindate, begindate+delta)
        cal.events.add(event)

    with open("ics/" + name + "-pacrim.ics", "w") as schedule_file:
        schedule_file.writelines(cal)

