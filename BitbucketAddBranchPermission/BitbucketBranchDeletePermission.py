#!/usr/bin/env python

'''
    This script adds a deletion prevention check on a branch pattern for
    specified repos in the file 'repos'.
    "pattern": variable to specify the branch or patter
    "repos": file containing all the repos to add permission to
    "bitbucket_project_key": Bitbucket project key
    __author__ = "Mohd Afnan Qureshi"
    __maintainer__ = "Mohd Afnan Qureshi"
    __email__ = "md.afnan1995@gmail.com"
    __status__ = "Production"
'''


# Imports
import requests
from urllib3.exceptions import InsecureRequestWarning


# Global variables
bitbucket_URL = 'https://bitbucket.com/'
bitbucket_branch_permissions = 'rest/branch-permissions/2.0/projects/'
bitbucket_project_key = 'KEY'
pattern = 'integration/*'
token = os.getenv('token')
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic ' + token
}


# Method to get all the repositories
def get_repos():
    file = open('repos', 'r')
    repos = file.readline()
    repos = repos.split(', ')
    return repos


# Method to add delete permission check
def add_delete_permission(repos):
    for repo in repos:
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        payload = "{\r\n\t\"type\": \"no-deletes\",\r\n\t\"matcher\": {\r\n\t\t\"id\": " \
                  "\"" + pattern + "\",\r\n\t\t\"displayId\": \"integration/*\",\r\n\t\t\"" \
                  "type\": {\r\n\t\t\t\"id\": \"PATTERN\",\r\n\t\t\t\"name\": \"Pattern\"" \
                  "\r\n\t\t},\r\n\t\t\"active\": true\r\n\t},\r\n\t\"users\": [\"user\"]," \
                  "\r\n\t\"groups\": [],\r\n\t\"accessKeys\": []\r\n}"
        response = requests.request("POST", bitbucket_URL + bitbucket_branch_permissions + bitbucket_project_key +
                                    '/repos/' + repo + "/restrictions", headers=headers, data=payload, verify=False)
        print(response.text.encode('utf8'))
        print(repo)


# Method calls
repos = get_repos()
add_delete_permission(repos)
