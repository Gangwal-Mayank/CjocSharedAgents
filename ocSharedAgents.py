import requests
import json
import sys
import getpass
from requests.auth import HTTPBasicAuth
from requests import get
from requests.exceptions import ConnectionError
jenkins_url = input("Enter jenkins url:")
username = input("Enter username:")
password = getpass.getpass()
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
        print ("################################ List of Shared Agents at OC level and thier status ################################")
        for jobs in response.json()['jobs']:
                if (response.json()['jobs'][i]['_class'] == "com.cloudbees.opscenter.server.model.SharedSlave"):
                        AgentName =  (response.json()['jobs'][i]['name'])
                        curlresponse = get (jenkins_url+'cjoc/view/all/job/'+AgentName+'/status', auth=(username, password))
                        if "Available for lease" in curlresponse.text:
                                print (AgentName + " is available for lease")
                        if "Off-line" in curlresponse.text:
                                print (AgentName + " is offline and disabled")
                        if "Node on lease" in curlresponse.text:
                                print (AgentName + " is leased")
                        j = j + 1
                i = i + 1
        print ("####################################################################################################################")
        print ("Total number of shared agents at CJOC level: " + str(j))
        print ("####################################################################################################################")
        i = 0
        print ("########################### List of managed controlles and status of thier leased agents ###########################")
        for jobs in response.json()['jobs']:
                if (response.json()['jobs'][i]['_class'] == "com.cloudbees.opscenter.server.model.ManagedMaster"):
                        ControllerName = (response.json()['jobs'][i]['name'])
                        print ("################################ Controller Name: " + ControllerName + " ################################")
                        k = k + 1
                        controllerApi = requests.get(jenkins_url+ControllerName.lower()+'/computer/api/json', auth=HTTPBasicAuth(username, password))
                        l = 0
                        for controllers in controllerApi.json()['computer']:
                                if (controllerApi.json()['computer'][l]['_class'] == "com.cloudbees.opscenter.client.cloud.OperationsCenterCloudComputer"):
                                        print ("Agent Name: " + controllerApi.json()['computer'][l]['displayName'])
                                        if (controllerApi.json()['computer'][l]['offline']):
                                                print ("Agent Status: " + controllerApi.json()['computer'][l]['offlineCauseReason'])
                                        else:
                                                print ("Agent Status: This Agent is online and leased")
                                l = l + 1
                i = i+1
        print ("####################################################################################################################")
        print ("Total number of shared agents: " + str(j))
        print ("Total number of managed controllers: " + str(k))
        print ("####################################################################################################################")
    else:
        print ("Invalid credentials")
        sys.exit()
except ConnectionError:
    print ("Invalid Url")
