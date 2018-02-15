#!/usr/bin/python3

import urllib.request

from bs4 import BeautifulSoup
import csv
from datetime import datetime
import os.path
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# specify the url
url = []
data2 = []
original_data = []
new_data = []


def initialize_array():
    with open('links.csv', newline='') as csv_file:
        reader = csv.reader(csv_file)
        for line in reader:
            url.append(''.join(line))
        csv_file.close()


def read_original_data():
    if os.path.exists('index.csv'):
        with open('index.csv', newline='') as csv_file:
            reader = csv.reader(csv_file)
            for line in reader:
                original_data.append(','.join(line))
            csv_file.close()


def write_file():
    existed = False
    if os.path.exists('index.csv'):
        existed = True
    with open('index.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        # The for loop
        counter = 0
        for name, sub2 in data2:
            if existed:
                sub1 = original_data[counter]
                counter += 1
                sub1 = str(sub1)
                index1 = sub1.find(",")
                index2 = sub1.find(",", index1+1)
                sub11 = sub1[index1+1:index1+(index2-index1)]
                if sub11 != sub2:
                    new_data.append((str(sub1[:index1]), sub2))
            else:
                new_data.append((str(name), sub2))
            writer.writerow([name, sub2, datetime.now()])
        csv_file.close()
    # print(sub)
    # print("***********************************************")


def push_message():
    fromaddr = 'saran@nilal.com'
    toaddrs = 'saran@nilal.com'

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "New Chapter Available"
    msg['From'] = "SaranFrom"  # like name
    msg['To'] = "SaranTo"
    txt = ""
    for urlname, chapter in new_data:
        txt += urlname + "\n " + chapter + "\n"
    body = MIMEText(txt)
    msg.attach(body)

    username = 'saran@nilal.com'
    password = 'here'
    server = smtplib.SMTP_SSL('smtp.googlemail.com', 465)
    server.login(username, password)
    server.sendmail(fromaddr, toaddrs, msg.as_string())
    server.quit()

initialize_array()
read_original_data()

for pg in url:
    req = urllib.request.Request(pg, headers={'User-Agent': 'Mozilla/5.0'})
    page = urllib.request.urlopen(req).read()
    # parse the html using beautiful soap and store in variable `soup`
    soup = BeautifulSoup(page, "html.parser")
    soupu = soup.encode('utf-8','replace')

    tables = soup.findAll("table", { "id" : "myTable" })
    rows = tables[0].find_all('tr')
    row = rows[1]
    data = row.find_all("td")
    data = str(data)
    startI = int((data.find("rel=\"nofollow\">")))
    endI = int(data.find("</a>", startI+1))
    diff = int(startI+(endI-startI))
    sub = data[startI+15:diff]
    data2.append((pg, sub))

write_file()

if len(new_data) > 0:
    push_message()
