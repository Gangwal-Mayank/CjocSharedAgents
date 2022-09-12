import requests
import json
import sys
import getpass
import inquirer
from requests.auth import HTTPBasicAuth
from requests import get
from requests.exceptions import ConnectionError
jenkins_url = input("Enter jenkins url:")
username = input("Enter username:")
password = getpass.getpass()
questions = [inquirer.List('Report Type', message="What report you would like to see?",choices=['Detailed','Available for lease at OC level', 'Leased but offline'])]
answers = inquirer.prompt(questions)
print (answers["Report Type"])
if not(jenkins_url.startswith("http://") or jenkins_url.startswith("https://")):
    print ("Invdliad url format")
    sys.exit()
#response = requests.get(jenkins_url+'cjoc/view/all/api/json',auth=HTTPBasicAuth(username, password))
try:
    response = requests.get(jenkins_url+'cjoc/view/all/api/json',auth=HTTPBasicAuth(username, password))
    if (response.status_code == 200):
        i = 0
        j = 0
        k = 0
        if (answers["Report Type"] == "Detailed"):
                print ("################################ List of Shared Agents at OC level and thier status ################################")
        for jobs in response.json()['jobs']:
                if (response.json()['jobs'][i]['_class'] == "com.cloudbees.opscenter.server.model.SharedSlave"):
                        AgentName =  (response.json()['jobs'][i]['name'])
                        curlresponse = get (jenkins_url+'cjoc/view/all/job/'+AgentName+'/status', auth=(username, password))
                        if "Available for lease" in curlresponse.text:
                                if (answers["Report Type"] == "Detailed" or answers["Report Type"] == "Available for lease at OC level"):  
                                        print (AgentName + " is available for lease")
                        if "Off-line" in curlresponse.text:
                                if (answers["Report Type"] == "Detailed"):
                                        print (AgentName + " is offline and disabled")
                        if "Node on lease" in curlresponse.text:
                                if (answers["Report Type"] == "Detailed"):
                                        print (AgentName + " is leased")
                        j = j + 1
                i = i + 1
        if (answers["Report Type"] == "Detailed"):
                print ("####################################################################################################################")
                print ("Total number of shared agents at CJOC level: " + str(j))
                print ("####################################################################################################################")
        i = 0
        if (answers["Report Type"] == "Detailed"):
                print ("########################### List of managed controlles and status of thier leased agents ###########################")
        for jobs in response.json()['jobs']:
                if (response.json()['jobs'][i]['_class'] == "com.cloudbees.opscenter.server.model.ManagedMaster"):
                        ControllerName = (response.json()['jobs'][i]['name'])
                        if (answers["Report Type"] == "Detailed"):
                                print ("################################ Controller Name: " + ControllerName + " ################################")
                        k = k + 1
                        controllerApi = requests.get(jenkins_url+ControllerName.lower()+'/computer/api/json', auth=HTTPBasicAuth(username, password))
                        l = 0
                        for controllers in controllerApi.json()['computer']:
                                if (controllerApi.json()['computer'][l]['_class'] == "com.cloudbees.opscenter.client.cloud.OperationsCenterCloudComputer"):
                                        if (answers["Report Type"] == "Detailed"):
                                                print ("Agent Name: " + controllerApi.json()['computer'][l]['displayName'])
                                        if (controllerApi.json()['computer'][l]['offline']):
                                                if (answers["Report Type"] == "Detailed" or answers["Report Type"] == "Leased but offline"):
                                                        print ("Agent Status: " + controllerApi.json()['computer'][l]['displayName'] + " " + controllerApi.json()['computer'][l]['offlineCauseReason'])
                                        else:
                                                if (answers["Report Type"] == "Detailed"):
                                                        print ("Agent Status: This Agent is online and leased")
                                l = l + 1
                i = i+1
        if (answers["Report Type"] == "Detailed"):
                print ("####################################################################################################################")
                print ("Total number of shared agents: " + str(j))
                print ("Total number of managed controllers: " + str(k))
                print ("####################################################################################################################")
    else:
        print ("Invalid credentials")
        sys.exit()
except ConnectionError:
    print ("Invalid Url")

