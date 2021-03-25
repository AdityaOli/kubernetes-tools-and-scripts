import json
import os
import sys
import time

CLUSTER=str(sys.argv[1])
NAMESPACE=str(sys.argv[2])

dataFile="/home/user/Logs/"+CLUSTER+"_"+NAMESPACE+"_deploy.txt"


with open(dataFile) as json_file:
    data = json.load(json_file)
    for eachDeployment in data:
        apiname=json.dumps(eachDeployment["apiname"]).strip('"')
        replicas=json.dumps(eachDeployment["replicas"])
        #os.system("kubectl get deploy "+apiname+" --replicas="+replicas)
        os.system("kubectl config set-context --current --namespace="+NAMESPACE)
        os.system("kubectl scale deploy "+apiname+" --replicas="+replicas)
