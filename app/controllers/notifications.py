from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import math

from smtplib import SMTP

from flask import Blueprint, jsonify, request, send_from_directory, send_file, Flask
from app import mongo
from app.helpers import *
from app.models.models import User, UserDao

users = mongo.db.users  # our items collection in mongodb
mongo_user_dao = UserDao(users)  # initialize a DAO with the collection


def sendMail(user_item, similar_items, found, matching):
    
    for similar_item in similar_items:
        
        if similar_item.email not in matching:
            print("will not send email")
            continue
        print("will send email")
        sender_email = "seekr.oose@gmail.com"
        password = "Seekroose!"

        port = 587  # For starttls
        smtp_server = "smtp.gmail.com"
        message = MIMEMultipart("alternative")
        message["Subject"] = f"Seekr Team: a similar item was added!"
        message["From"] = sender_email
        message["To"] = similar_item.email
        
        # Create the plain-text and HTML version of your message
        text = """\
        Hi {similar_item.username}!
        You recently added: {similar_item.name} on {similar_item.timestamp}.
        An item was added that was similar to what you're looking for! {found}: {user_item.name}
        """
        status = ""
        other = ""
        if similar_item.found: 
            status = "found" 
            other = "lost"
        else:
            status = "lost"
            other = "found"
        html = f"""\
        <html>
        <body>
            <p>Hi {similar_item.username}!<br>
            You recently posted a {status} {similar_item.name}.
            <br>Someone named {user_item.username} posted something you may be looking for!
            <br>Here are the details:
            <br>
            <br>Item Name: {other} {user_item.name}
            <br>Description: {user_item.desc}
            <br>
            <br>Note: You received this email because you selected to receive email updates if similar items to your postings are added. 
            <br>You can change this setting in your User Info tab.
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
            smtp_serv.sendmail(
                sender_email, similar_item.email, message.as_string())
            # print("email sent")
        except Exception as e:
            print(e)

        smtp_serv.quit()


def distance(item1, item2):
    """Haversine formula for computing distance between two locations on the 
    surface of the earth, in feet.
    """
    lat1 = item1.location.coordinates[1]
    lon1 = item1.location.coordinates[0]
    lat2 = item2.location.coordinates[1]
    lon2 = item2.location.coordinates[0]

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)

    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2.0) ** 2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    dist = 2.0902e7*c

    return dist


def radiusCutOff(items, queriedItem):
    results = []

    for item in items:
        if distance(queriedItem, item) <= queriedItem.radius:
            results.append(item)
    return results


def getSimItems(queriedItem, simMatch):
    # get right string to return
    found = 'found' if queriedItem.found == True else 'missing'

    # if no items, return
    if len(simMatch.itemScores) == 0:
        print("NO ITEMS")
        return [], ''

    listOfItems = radiusCutOff(simMatch.getSortedItems(), queriedItem)

    if len(listOfItems) == 0:
        return[], ''

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
        if imageMatch(queriedItem, item) < 35:  # Under 35 key point matches
            similar_items.remove(item)

    return similar_items, found
