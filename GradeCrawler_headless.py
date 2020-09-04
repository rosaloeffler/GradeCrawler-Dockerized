#!/usr/bin/env python
import json
import configparser
import smtplib
import ssl # important for execution outside conda prompt
from datetime import datetime
from socket import gaierror
from time import sleep
from email.message import EmailMessage
from selenium.webdriver.support.ui import Select
from selenium import webdriver


#-------------------------------------------------------------------------------
#                                   INFO
#-------------------------------------------------------------------------------
# Simple Grade Crawler for DHGE SelfService
# Version: 1.0
#
#   Setup:
#       1. Extract script and Firefoxdriver (geckodriver) in the same diretory
#               Firefox-Driver: https://github.com/mozilla/geckodriver/releases
#       2. Install selenium with "pip install selenium"
#   How to use:
#       1. Configurate the script at section CONFIG
#       2. Start the script with py GradeCrawler.py
#       -> To exit close terminal/cmd or press strg+c
#
#   -> Script create data at first run, check grades in terminal! Later the
#      script sends notification mails if new grades detected
#
# Attention! This crawler use Firefox as Seleniumdriver, but Chrome can be
# used too.
#   Chromedriver download:
#       https://chromedriver.chromium.org/downloads
#   Config:
#       Search for line "driver = webdriver.Firefox()" and edit it to
#       "driver = webdriver.Chrome()"
#
# Copyright by Kr3b5


#-------------------------------------------------------------------------------
#                                   LOAD-CONFIG
#-------------------------------------------------------------------------------

# load config-file, used instead of json because ini-file allows comments
config = configparser.ConfigParser()
config.read("./configcrawler.ini")

# Credentials DHGE-Service
url_dhge = config["URLCREDENTIALS"]["url_dhge"]
matnr = config["URLCREDENTIALS"]["matnr"]
passw = config["URLCREDENTIALS"]["passw"]

# grades of which semesters
# loaded as json because of support for data formats other than str
semesters = json.loads(config["PREFERENCES"]["semesters"])

#first part of filename
fileprefix = config["PREFERENCES"]["fileprefix"]

# Delay Check / Online Time
delay = int(config["PREFERENCES"]["delay"])    #1min = 60, minimum 6*loop_delay
start_time = int(config["PREFERENCES"]["start_time"])
end_time = int(config["PREFERENCES"]["end_time"])

# Features
want_Mail = config.getboolean("MAILSETTINGS","want_mail")

# SMTP Server (Mail)
port = int(config["MAILSETTINGS"]["port"])
smtp_server = config["MAILSETTINGS"]["smtp_server"]
login = config["MAILSETTINGS"]["login"]
mailpassw = config["MAILSETTINGS"]["password"]

# Mail config
sender = config["MAILSETTINGS"]["sender"]
subject = config["MAILSETTINGS"]["subject"]
# loaded as json because of support for data formats other than str
receivers = json.loads(config["MAILSETTINGS"]["receivers"])

#-------------------------------------------------------------------------------
#                   DEV-CONFIG - activate only for Dev
#-------------------------------------------------------------------------------

#url_dhge = "http://localhost/noten.php"
dev_mode_view = 0 # 0 = off | 1 = on - without front Page, only grade view
dev_mode_mail = 0 # 0 = off | 1 = on - no credetials for Debug Mail Server

#===============================================================================

#-------------------------------------------------------------------------------
#                   Skript - dont touch a running system
#-------------------------------------------------------------------------------

def main():
    """Banner, Infinte loop and function calls"""
    print("   _____               _         _____                    _           ")
    print("  / ____|             | |       / ____|                  | |          ")
    print(" | |  __ _ __ __ _  __| | ___  | |     _ __ __ ___      _| | ___ _ __ ")
    print(" | | |_ | '__/ _` |/ _` |/ _ \\ | |    | '__/ _` \\ \\ /\\ / / |/ _ \\ '__|")
    print(" | |__| | | | (_| | (_| |  __/ | |____| | | (_| |\\ V  V /| |  __/ |   ")
    print("  \\_____|_|  \\__,_|\\__,_|\\___|  \\_____|_|  \\__,_| \\_/\\_/ |_|\\___|_|   ")
    print("                                                   Copyright by Kr3b5\n")
    printcmd("Starting... \n")

    idle_print = 1
    loop_delay = 10 # just to slow down

    while True:
        this_hour = datetime.now().hour
        #check if time is in range -> reduce traffic
        if is_online(this_hour):
            for semester in semesters:
                # set filesuffix
                filesuffix = str(semester) + ".txt"
                # get web content
                html_source = get_content(semester)
                #get grade list from html_source
                grade_list = get_grade(html_source)
                #get old grade list
                old_grade_list = get_list(filesuffix)
                #compare both for new grades
                compare(grade_list, old_grade_list, filesuffix)
                #reduce output idle
                idle_print = 1
                sleep(loop_delay)
        else:
            if idle_print == 1:
                printcmd(f"> Idle - next check:{start_time}:00\n")
                idle_print = 0
        sleep(delay)


def is_online(time):
    """Check whether within polling-hours"""
    if( time >= start_time and time < end_time ):
        return True
    else:
        return False


def get_content(sem):
    """get html-content, return as string"""
    coptions = webdriver.ChromeOptions()
    coptions.add_argument("headless") # for servers
    coptions.add_argument('no-sandbox') # maybe not secure, but inevitable ?
    driver = webdriver.Chrome(options=coptions)
    driver.get(url_dhge)

    if dev_mode_view == 0:
        username = driver.find_element_by_name("matrnr")
        username.clear()
        username.send_keys(matnr)
        password = driver.find_element_by_name("passw")
        password.clear()
        password.send_keys(passw)
        select_element = Select(driver.find_element_by_name("sem"))
        select_element.select_by_value(str(sem))
        driver.find_element_by_xpath("//input[@value='Notenauskunft (Bildschirm)']").click()

    html_source = driver.page_source
    driver.quit()

    return html_source

def get_grade( html_source ):
    """pick grades from html-content"""
    grade_list = []

    s1 = html_source.split("<tr>")
    for i in range(9):
        del s1[0]

    anz = 0
    for i in range(len(s1)):
        if s1[i] == "<td colspan=\"9\"><hr></td></tr>":
            anz = i

    for i in range(anz):
        s2 = s1[i].split("<td align=\"left\">")
        fach = s2[1].split("</td>")
        fach = fach[0]
        note = s2[1].split("<td align=\"center\">")
        note = note[1].split("                           </td>")
        note = note[0]
        if note.endswith('</td>'):
            note = note[:-5]
        grade_list.append(fach)
        grade_list.append(note)

    return grade_list


def write_file(grade_list, suffix):
    """write grade file for comparison later"""
    with open(fileprefix + suffix, 'w') as f:
        for item in grade_list:
            f.write("%s\n" % item)


def get_list(suffix):
    """return list of known grades from file"""
    try:
        return [line.rstrip('\n') for line in open(fileprefix + suffix, 'r')]
    except FileNotFoundError:
        return "[]"


def compare(grade_list, old_grade_list, suffix):
    """compare lists of old and new grades, print results, call send_mail"""
    printcmd("Semester: " + suffix[:1])
    if isinstance(old_grade_list, str):
        printcmd("First init run!")
        write_file(grade_list, suffix)
        printcmd("Gradelist (new):")
        printcmd(grade_list)
        print("")
    elif grade_list == old_grade_list:
        printcmd("No new grades available!")
        printcmd("Gradelist (old|new):")
        printcmd(old_grade_list)
        print("")
    else:
        printcmd("New grades available!")
        write_file(grade_list, suffix)
        printcmd("Gradelist (old|new):")
        printcmd(old_grade_list)
        printcmd(grade_list)
        print("")
        if want_Mail:
            send_mail(grade_list, suffix)


def send_mail(grade_list, suffix):
    """send emails if new grades are fetched"""
    for receiver, sendgrades in receivers.items():
        print(f"> Send mail to {receiver}...")
        msg = EmailMessage()
        msg['From'] = sender
        msg['To'] = receiver
        msg['Subject'] = subject
        mcontent = "Semester: " + suffix[:1]
        if sendgrades:
            mcontent += "\n" + str(grade_list)
        else:
            mcontent += "\nGrades are top-secret ;-)!"
        msg.set_content(mcontent)
        try:
            with smtplib.SMTP(smtp_server, port) as server:
                if dev_mode_mail == 0:
                    server.starttls() ####
                    server.login(login, mailpassw)
                server.send_message(msg) ####
        except (gaierror, ConnectionRefusedError):
            printcmd('Failed to connect to the server. Bad connection settings?')
        except smtplib.SMTPServerDisconnected:
            printcmd('Failed to connect to the server. Wrong user/password?')
        except smtplib.SMTPException as e:
            printcmd('SMTP error occurred: ' + str(e))
        else:
            printcmd('Success')
        print("")

def printcmd(s):
    """print statements with timestamp"""
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("[%b %d %y %H:%M:%S]")
    print(f"{timestampStr} {s}" )


if __name__ == '__main__':
    main()
