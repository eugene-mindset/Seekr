# Schedule Library imported 
from app.models.models import *
from app import mongo
import sched
import time 
import gensim.downloader as gens_api
from app.models.similarity import ItemSimilarity
from app.helpers import *
from math import radians, sin, cos, acos
from flask import Blueprint, jsonify, request, send_from_directory, send_file, Flask
from flask_mail import Mail, Message
import smtplib, ssl
from email.mime.text import MIMEText	
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart	
from email.mime.multipart import MIMEMultipart



embedding = gens_api.load('glove-wiki-gigaword-50')
items = mongo.db.items # our items collection in mongodb
mongo_item_dao = ItemDao(items) # initialize a DAO with the collection


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
        <p>Hi {user_item.user.name}!,<br>
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

    smtp_serv = smtplib.SMTP(smtp_server, port)
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
    slat = radians(item1.location.coordinates[0])
    slon = radians(item1.location.coordinates[1])
    elat = radians(item2.location.coordinates[0])
    elon = radians(item2.location.coordinates[1])

    dist = 3958.8 * acos(sin(slat)*sin(elat) + cos(slat)*cos(elat)*cos(slon - elon))
    # dist = 6371.01 * acos(sin(slat)*sin(elat) + cos(slat)*cos(elat)*cos(slon - elon))
    return dist
# Functions setup 
      

def radius_cutoff(items, queriedItem):
    results = []

    for item in items:
        if distance(queriedItem, item) <= queriedItem.radius: #miles
            results.append(item)
    return results


def notify(queriedItem):
    
    listOfItems = mongo_item_dao.findAll(tags=0b0000_0000)
    found = "missing"
    
    # if queriedItem is a found item then only need to compare similarity with missing items and vice versa
    if queriedItem.found is True:
        listOfItems = [item for item in listOfItems if item.found is False]
    
    else:
        listOfItems = [item for item in listOfItems if item.found is True]
        found = "found"
        
    listOfItems = radius_cutoff(listOfItems, queriedItem)
 
    if len(listOfItems) != 0:
        simMatch = ItemSimilarity(modelName=None)
        simMatch.model = embedding
        simMatch.addItems(listOfItems)
        simMatch.scoreItems(queriedItem)

        items = simMatch.getSortedItemsAndScores()
        similar_items = []

        for item, score in items:
            print("Score: " + str(score) + "...")
            if score >= 0.75:
                similar_items.append(item)
        if len(similar_items) != 0:
            send_mail(queriedItem, similar_items, found)
    else:
        print("NO ITEMS")


def notify_all():
    listOfItems = mongo_item_dao.findAll(tags)
    for item in listOfItems:
        notify(item)
        