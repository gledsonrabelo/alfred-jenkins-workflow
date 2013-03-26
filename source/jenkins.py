"""
Creator:    Jeroen Seegers
Homepage:   http://jeroenseegers.com
Repository: https://github.com/jeroenseegers/alfred-jenkins-workflow
Twitter:    https://twitter.com/RevellNL
Version:    0.1 (26-03-2013)
"""

import re
import sys
import urllib
import socket
import json

from Feedback import Feedback
from xml.dom import minidom

# Set the timeout to 5 seconds
socket.setdefaulttimeout(5)

CONFIGURED_URL = ""

def execute(query):
    """Execute the desired command

    Keyword arguments:
    query   -- The query entered by the user

    """
    words = query.split()
    action = words[0]
    words.pop(0)
    terms = " ".join(words)

    if action == "status":
        return get_status(terms)
    else:
        feedback = Feedback()
        feedback.add_item("status {query}", "Get the status for builds corresponding with {query}", "", "no", "status")
        return feedback

def get_status(terms=""):
    """Retrieve the current status of the jobs matching the given terms

    Keyword arguments:
    terms       -- The terms entered by the user (default is "")

    """
    feedback = Feedback()
    data = get_data_from_url()

    if data != None:
        if "jobs" in data and len(data["jobs"]) > 0:
            search_regex = re.compile(terms, re.IGNORECASE)
            for job in data["jobs"]:
                if re.search(search_regex, job["name"]) != None:
                    title = job["name"]
                    feedback.add_item(title, "", job["url"], "yes", "", "images/"+job["color"]+".png")
        else:
            feedback.add_item("No results found", "I'm sorry, I failed to find what you were looking for", "", "no")
    else:
        feedback.add_item("An error occured", "It seems I made a mistake somewhere, please forgive me", "", "no")

    return feedback

def get_data_from_url(url=""):
    """Retrieve data from the configured or given URL

    Keyword arguments
    url     -- A custom URL (default is "")

    """
    returnData = ""

    if url == "":
        url = CONFIGURED_URL

    try:
        request = urllib.urlopen(url+"/api/json")
        if request.getcode() == 200:
            response = request.read()
            returnData = json.loads(response)
        else:
            returnData = None
    except IOError as e:
        returnData = None

    return returnData

def set_url(url):
    """Set the global URL to use

    Keyword arguments
    url     -- A custom URL

    """
    global CONFIGURED_URL
    CONFIGURED_URL = url
    return
