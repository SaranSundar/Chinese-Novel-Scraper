import pandas as pd
import pickle
import os.path
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

links = []
chapters = []
linksAndChapters = []
oldChapterList = []


def readLinks():
    global links
    with open('links.txt', 'r') as f:
        for line in f:
            links.append(line.strip())


def readChapters():
    global links
    global chapters
    for i in range(len(links)):
        name = "websites/index.html"
        if i > 0:
            name += "." + str(i)
        tables = pd.read_html(name)
        chapters.append(tables[1].Release.values[0])


def updateToLatestChapters():
    global links
    global chapters
    global linksAndChapters
    startingIndex = len("http://www.novelupdates.com/series/")
    for i in range(len(links)):
        link = links[i]
        link = link[startingIndex:-1]
        link = link.replace("-", " ")
        link = link.title()
        chapter = chapters[i]
        chapter = chapter.split('c')
        chapter = chapter[1]
        # print(link + " c" + chapter)
        linksAndChapters.append(link + " c" + chapter)


def writeLatestChapters():
    global linksAndChapters
    with open('latest_chapters', 'wb') as fp:
        pickle.dump(linksAndChapters, fp)


def readLastChapters():
    global oldChapterList
    if os.path.exists('latest_chapters'):
        with open('latest_chapters', 'rb') as fp:
            oldChapterList = pickle.load(fp)
    # print(oldChapterList)


def createEmailMessage():
    txt = ""
    if len(linksAndChapters) != len(oldChapterList):
        txt = "\n".join(linksAndChapters)
    else:
        for i in range(len(linksAndChapters)):
            newChapter = linksAndChapters[i]
            oldChapter = oldChapterList[i]
            if newChapter != oldChapter:
                txt += newChapter + "\n"
    if len(txt) > 0:
        emailUpdatedChapters(txt)


def emailUpdatedChapters(txt):
    global linksAndChapters
    global oldChapterList
    fromaddr = 'saran@nilal.com'
    toaddrs = 'saran@nilal.com'

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "New Chapter(s) Available"
    msg['From'] = "SaranFrom"  # like name
    msg['To'] = "SaranTo"

    body = MIMEText(txt)
    msg.attach(body)

    username = 'saran@nilal.com'
    password = 'here'
    server = smtplib.SMTP_SSL('smtp.googlemail.com', 465)
    server.login(username, password)
    server.sendmail(fromaddr, toaddrs, msg.as_string())
    server.quit()


def main():
    readLastChapters()
    readLinks()
    readChapters()
    updateToLatestChapters()
    writeLatestChapters()
    print("Starting email")
    createEmailMessage()
    print("Done...")

main()

# #!/bin/bash
# rm -rf websites
# rm -rf wget-log
# wget -b --reject '*.js,*.css,*.ico,*.txt,*.gif,*.jpg,*.jpeg,*.png,*.mp3,*.pdf,*.tgz,*.flv,*.avi,*.mpeg,*.iso' --$
# sudo python3 download-chapters.sh
