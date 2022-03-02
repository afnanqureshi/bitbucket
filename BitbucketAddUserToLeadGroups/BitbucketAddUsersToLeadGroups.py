#!/usr/bin/env python

'''
    This code adds a user to all the leads group in Bitbucket.
    Change the 'user' variable to the user id that you want to add to the lead groups.
    __author__ = "Mohd Afnan Qureshi"
    __maintainer__ = "Mohd Afnan Qureshi"
    __email__ = "md.afnan1995@gmail.com"
    __status__ = "Production"
'''


import requests
from urllib3.exceptions import InsecureRequestWarning
import re
import os

# Global variable declaration
BitbucketURL = "https://bitbucket.com/"
AddUsersAPI = "rest/api/1.0/admin/groups/add-users"
GroupsAPI = "rest/api/1.0/admin/groups"
token = os.getenv('token')
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic ' + token
}


# Method to get all the lead groups in Bitbucket
def getGroups():
    last_page = False
    start = 0
    limit = 250
    groups = []
    count = 0

    while not last_page:
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        response = requests.request("GET", BitbucketURL + GroupsAPI + '?limit=' + str(limit) + "&start=" + str(start),
                                    headers=headers, verify=False)
        data = response.json()

        if not data['isLastPage']:
            last_page = False
            start = start + limit
        else:
            last_page = True

        for d in data['values']:
            if re.search('lead', d['name']):
                groups.append(d['name'])
                count = count + 1

    # print(groups)
    # print(count)
    addUsers(groups)


# Method to add user to the leads group
def addUsers(groups):
    # Change this 'user' variable to the user id that you want to add to the lead groups
    user = "grafana2jira"

    for group in groups:
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        payload = "{\r\n    \"group\": \"" + group + "\",\r\n    \"users\": [\r\n    \t\"" + user + "\"\r\n    ]\r\n}"
        response = requests.request("POST", BitbucketURL + AddUsersAPI, headers=headers, data=payload, verify=False)
        # print(response.text.encode('utf8'))

    print("User " + str(user) + " added to groups: ")
    print(groups)


getGroups()
