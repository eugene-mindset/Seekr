from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import math

from smtplib import SMTP

from flask import Blueprint, jsonify, request, send_from_directory, send_file, Flask

from app.helpers import *



def send_mail(user_item, similar_items, found):
    sender_email = "seekr.oose@gmail.com"
    password = "Seekroose!"

    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    message = MIMEMultipart("alternative")
    message["Subject"] = f"Seekr Team: We found a Similar Items for You"
    message["From"] = sender_email
    message["To"] = user_item.user.email

    # Create the plain-text and HTML version of your message
    text = """\
    Hi,
    How are you?
    Real Python has many great tutorials:
    www.realpython.com"""
    html = f"""\
    <html>
    <body>
        <p>Hi {user_item.user.name}!<br>
        You recently added: {user_item.name}.
        <br>Here are some similar {found} items: {similar_items}
        </p>
    </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    smtp_serv = SMTP(smtp_server, port)
    smtp_serv.ehlo()
    smtp_serv.starttls()
    smtp_serv.ehlo()
    smtp_serv.login(sender_email, password)
    try:
        smtp_serv.sendmail(sender_email, user_item.user.email, message.as_string())
        print("email sent")
    except Exception as e:
        print(e)

    smtp_serv.quit()


def distance(item1, item2):
    slat = math.radians(item1.location.coordinates[0])
    slon = math.radians(item1.location.coordinates[1])
    elat = math.radians(item2.location.coordinates[0])
    elon = math.radians(item2.location.coordinates[1])

    dist = 3958.8 * math.acos(math.sin(slat)*math.sin(elat)
        + math.cos(slat)*math.cos(elat)*math.cos(slon - elon))
    # dist = 6371.01 * acos(sin(slat)*sin(elat) + cos(slat)*cos(elat)*cos(slon - elon))
    return dist


def radius_cutoff(items, queriedItem):
    results = []

    for item in items:
        if distance(queriedItem, item) <= queriedItem.radius: #miles
            results.append(item)
    return results


def notify(queriedItem, simMatch):
    # get right string to return
    found = 'found' if queriedItem.found == True else 'missing'

    # if no items, return
    if len(simMatch.itemScores) == 0:
        print("NO ITEMS")
        return

    print(simMatch.getSortedItems())
    listOfItems = radius_cutoff(simMatch.getSortedItems(), queriedItem)
    simMatch.clearItems()
    simMatch.addItems(listOfItems)
    simMatch.scoreItems(queriedItem)

    items = simMatch.getSortedItems(getScores=True)
    similar_items = []

    for item, score in items:
        print("Score: " + str(score) + "...")
        if score >= 0.5:
            similar_items.append(item)

    for item in similar_items:
        if imageMatch(queriedItem, item) < 35: #Under 35 key point matches
            similar_items.remove(item)

    if len(similar_items) != 0:
        send_mail(queriedItem, similar_items, found)
