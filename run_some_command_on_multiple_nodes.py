import os
import subprocess
import sys
import logging
import datetime
from datetime import date

def Check_all_servers(servers):
    for node in servers:
        print("===================== Checking Node : "+str(node)+" ===============================")
        out=subprocess.Popen(['ssh', 'user@'+node, "egrep '^(VERSION|NAME)=' /etc/os-release"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        out, err = out.communicate()
        print(out)

def main():
    logging.info("Running the Script at :"+str(datetime.datetime.now()))
    servers=["node1","node2","node3","node4"]
    Check_all_servers(servers)
    
    
    
if __name__ == "__main__":
    #filename="/home/olia2-ua/Logs/ImagesCollector_"+date.today().strftime("%d%m%Y")+".log"
    #logging.basicConfig(level=logging.DEBUG, filename=filename, filemode="a+",format="%(asctime)-15s %(levelname)-8s %(message)s")
    main()
