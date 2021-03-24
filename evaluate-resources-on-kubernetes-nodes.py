import os
import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
import logging
import time
from datetime import date
import datetime

all_emails="EMAILIDS"
ops="EMAILIDFOROPS"

def Check_mount_spaces_on_Kubernetes_nodes(servers):
      messageArray=[]
      for node in servers:
        logging.info("Checking mount spaces on "+node)
        out=subprocess.Popen(['ssh', 'user@'+node, 'df -h'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = out.communicate()
        mountOutput=out
        array=out.split('\n')
        
        j=1 
        while j<len(array):
          if array[j]:
            tempArray=array[j].split(' ')
            filteredArray=[x for x in tempArray if x]
            if int(str(filteredArray[4]).replace("%",'')) >= 90:
              logging.error("ERROR : Node "+node+" has mount space greater than 90% for mount :"+filteredArray[0]+". The Current value is : "+filteredArray[4])
              message="ERROR : Node "+node+" has mount space greater than 90% for mount :"+filteredArray[0]+". The Current value is : "+filteredArray[4]
              messageArray.append(message)
          j+=1
      if messageArray:
            send_email("EMAILID",ops,"ALERT : Mount Point Disk Space Overflow",messageArray)

'''def Check_CPU_and_RAM_on_Kubernetes_nodes(servers):
      # LOGIN TO CLUSTER WITH KUBECTL
      out= subprocess.Popen(['kubectl', 'top', 'nodes'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      out, err = out.communicate()
      array=out.split(' ')

      filteredArray=[x for x in array if x]

      sortedData=[]
      name=0
      while name<len(filteredArray)-1:
        singleEntry=[]
        singleEntry.append(filteredArray[name])
        singleEntry.append(filteredArray[name+1])
        singleEntry.append(filteredArray[name+2])
        singleEntry.append(filteredArray[name+3])
        singleEntry.append(filteredArray[name+4])
        sortedData.append(singleEntry)
        name+=5
        
      sortedData=sortedData[1:]
      for x in sortedData:
        
        CPU=x[2]=x[2].replace('%','')
        MEM=x[4]=x[4].replace('%','')
        Message=""
        if int(CPU)>70:
          Message="Hi, the CPU on server "+x[0]+" has exceeded 80%. The current value is "+CPU+"%" 
        if int(MEM)>70:
          Message="Hi, the MEMORY on server "+x[0]+" has exceeded 80%. The current value is "+MEM+"%"
          
        if Message!="":
          targets=["aditya.oli1@infosys.com","CRITICAL : Kubernetes High Resource Usage Alert",Message]
          os.system("sh "+os.getcwd()+"/Scripts/Temp/send_email.sh "+targets)
'''      
def Check_SWAP_space_on_Kubernetes_nodes(servers):
      messageArray=[]
      for node in servers:
        logging.info("Checking SWAP space on "+node)
        out=subprocess.Popen(['ssh', 'user@'+node, 'free -m'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = out.communicate()
        swapOutput=out
        array=out.split('\n')
        Memory=array[1].split(' ')
        MemoryArray=[x for x in Memory if x]    
        Swap=array[2].split(' ')
        SwapArray=[x for x in Swap if x]                
        logging.info("Checking SWAP : ")
        logging.info("Currently Swap used is : "+str(float(SwapArray[2])/float(SwapArray[1])*100)+"%")
        if float(SwapArray[2])/float(SwapArray[1])*100 > 90.0:
              logging.error("ERROR : Node "+node+" has swap space consumption greater than 90%. The Current value is : "+str(float(SwapArray[2])/float(SwapArray[1])*100))
              message="ERROR : Node "+node+" has swap space consumption greater than 90%. The Current value is : "+str(float(SwapArray[2])/float(SwapArray[1])*100)
              messageArray.append(message)
      if messageArray:
            send_email("EMAILID",ops,"ALERT : High Swap Consumption",messageArray)
  
def Check_Load_Averages_on_Kubernetes_nodes(servers):
  messageArray=[]      
  for node in servers:
        logging.info("Checking load average on "+node)
        out=subprocess.Popen(['ssh', 'user@'+node, 'uptime'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = out.communicate()
        array=out.split(' ')
        loadArray=[x for x in array if x]
        OneMinute=float(loadArray[len(loadArray)-3].replace(",",""))
        FiveMinute=float(loadArray[len(loadArray)-2].replace(",",""))
        FifteenMinute=float(loadArray[len(loadArray)-1].replace(",",""))
        numberOfCPU=subprocess.Popen(['ssh', 'user@'+node, 'nproc'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        numberOfCPU, err = numberOfCPU.communicate()
        numberOfCPU=int(numberOfCPU)
        OneMinute=OneMinute/numberOfCPU
        FiveMinute=FiveMinute/numberOfCPU
        FifteenMinute=FifteenMinute/numberOfCPU
        if OneMinute > 20 or FiveMinute > 20 or FifteenMinute > 20:
              logging.error("ERROR : Node "+node+" has very high load average. The Current value is : "+str(OneMinute)+","+str(FiveMinute)+","+str(FifteenMinute))
              message="ERROR : Node "+node+" has very high load average. The Current value is : "+str(OneMinute)+","+str(FiveMinute)+","+str(FifteenMinute)
              messageArray.append(message)
  if messageArray:
        send_email("EMAILID",ops,"ALERT : High Load Average",message)
              
def Check_RAM_On_Kubernetes_Nodes(servers):
      messageArray=[]
      for node in servers:
            logging.info("======================================================")
            logging.info("Checking Memory on "+node)
            out=subprocess.Popen(['ssh', 'user@'+node, 'free -m'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = out.communicate()
            logging.info(out)
            swapOutput=out
            array=out.split('\n')
            Memory=array[1].split(' ')
            MemoryArray=[x for x in Memory if x] 
            
            logging.info("Current Memory free is : "+str(float(MemoryArray[6]))+" / "+str(float(MemoryArray[1]))+" * 100 = "+str(float(MemoryArray[6])/float(MemoryArray[1])*100)+"%")
            if float(MemoryArray[6])/float(MemoryArray[1])*100 < 10.0:
                  logging.error("ERROR : Node "+node+" has Memory consumption percentage greater than 85%. The Current value is : "+str(100.0-(float(MemoryArray[6])/float(MemoryArray[1])*100)))
                  message="ERROR : Node "+node+" has Memory consumption percentage greater than 85%. The Current value is : "+str(100.0-(float(MemoryArray[6])/float(MemoryArray[1])*100))
                  messageArray.append(message)
      if messageArray:
            send_email("EMAILID",ops,"ALERT : High Memory Usage",messageArray)
                  
def Check_docker_system_stats_on_Kubernetes_nodes(servers):
      for node in servers:
        logging.info("Checking Docker stats on "+node)
        out=subprocess.Popen(['ssh', 'user@'+node, 'do'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = out.communicate()
        swapOutput=out
        array=out.split('\n')
        logging.info("Checking Memory : ")
        tempArray=array[1].split(' ')
        filteredArray=[x for x in tempArray if x]
        logging.info("Checking SWAP : ")
        
def Check_mount_connectivity_on_Kubernetes_nodes(servers):
      for node in servers:
        logging.info("Checking Mount Points Connectivity on "+node)
        out=subprocess.Popen(['ssh', 'user@'+node, 'cat /proc/mounts |grep -i nfs'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = out.communicate()
        swapOutput=out
        
def Check_Pod_Lifecycle_Event_Generator_on_Kubernetes_nodes():
      logging.info("Checking for PLEG on both Clusters")
      logging.info("Checking Cluster1")
      Check_PLEG('ClusterLogin')
      logging.info("Checking Cluster2")
      Check_PLEG('ClusterLogin') 
      
def Check_PLEG(cluster):
      string_to_search_for="PLEG is not healthy" 
      out=subprocess.Popen(['Login to CLsuter'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      out=subprocess.Popen(['kubectl', 'describe','nodes'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      out, err = out.communicate()
      if string_to_search_for in out:
            message="Hi, There seems to be PLEG errors on the nodes on "+cluster+". One of the reasons might be that docker and kubelet are too slow to communicate, or your NFS mounts are unresponsive. Please check respectively. \n Regards, \n K8s Bot."
            send_email("EMAILID",ops,"ALERT : PLEG Failure on Kubernetes Nodes",message)

def Check_JMS_queue_for_failures(servers):
      print()

def send_email(sender,receiver,subject,message):
      logging.info("Sending Email Alert!")
      me = sender
      you = receiver

      msg = MIMEMultipart('alternative')
      msg['Subject'] = subject
      msg['From'] = me
      msg['To'] = you
      if "Kogan Callback" in subject:
            message="".join(message)
      if "High Load Average" in subject:
            message="".join(message)
      else:
            message="<br><br><br>".join(message)
      
      
      html = """\
      <html>
        <head>
        <title>Alert</title>
        <style>
        table, th, td {
            border: 1px solid blue;
            border-collapse: collapse;
        }
        th, td {
            padding: 5px;
        }
        strong {
          bgcolor: white;
          color: red;
        }
        </style>
        </head>
        <body>
        <table style='width:100%'>
        <tr>
            <th><strong>"""+subject+"""</strong></th>
          </tr>
          <tr>
            <td>"""+message+"""</td>
          </tr>
        </table>
        </body></html>
      """
      part2 = MIMEText(html, 'html')
      msg.attach(part2)
      try:
        s = smtplib.SMTP('localhost')
        s.sendmail(me, you, msg.as_string())
        s.quit()         
        logging.info("Successfully sent email")
      except Exception:
       logging.error("Error: unable to send email")
      
def Remove_greater_than_last_seven_days_log_files():
    path = "/home/user/Scripts/Alerts/Evaluator/Logs/"
    now = time.time()
    for filename in os.listdir(path):
        if "evaluator" in filename and ".log" in filename:
              if os.path.getmtime(os.path.join(path, filename)) < now - 7 * 86400:
                  if os.path.isfile(os.path.join(path, filename)):
                    logging.error("DELETING "+ filename)
                    os.remove(os.path.join(path, filename)) 
                    
def check_LDAP_Connection_On_Kubernetes_Servers():
      servers=["server1","server2"]
      messageArray=[]
      for node in servers:
        logging.info("Checking LDAP on "+node)
        
        out1=subprocess.Popen(['ssh', 'user@'+node, 'nc -z -v nodeIP 636'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out1, err1 = out1.communicate()
        out2=subprocess.Popen(['ssh', 'user@'+node, 'nc -z -v nodeIP 636'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out2, err2 = out2.communicate()
        out3=subprocess.Popen(['ssh', 'user@'+node, 'nc -z -v nodeIP 389'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out3, err3 = out3.communicate()
        out4=subprocess.Popen(['ssh', 'user@'+node, 'nc -z -v nodeIP 389'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out4, err4 = out4.communicate()
        
        #print(out1, out2, out3, out4)
        #print(err1,err2,err3,err4)
        
        if "Connected" in err1 and "Connected" in err2 and "Connected" in err3 and "Connected" in err4:
            print("All Good")
            logging.info("INFO : Node "+node+" LDAP OK!")
        else:
            print("Not Good")
            message="ERROR : Node "+node+" has LDAP Issues."
            messageArray.append(message)
      if messageArray:
            send_email("EMAILID",ops,"ALERT : LDAP Connection Broken",messageArray)      


def main():
  servers=["node1","node2","node3"]
  logging.info("Running the Script at :"+str(datetime.datetime.now()))
  Check_mount_spaces_on_Kubernetes_nodes(servers)
  check_LDAP_Connection_On_Kubernetes_Servers()
  Check_Load_Averages_on_Kubernetes_nodes(servers)
  Check_RAM_On_Kubernetes_Nodes(servers)
  Check_Pod_Lifecycle_Event_Generator_on_Kubernetes_nodes()
  Remove_greater_than_last_seven_days_log_files()
  
    
if __name__ == "__main__":
    filename="/home/user/Scripts/Alerts/Evaluator/Logs/evaluator_"+date.today().strftime("%d%m%Y")+".log"
    logging.basicConfig(level=logging.DEBUG, filename=filename, filemode="a+",format="%(asctime)-15s %(levelname)-8s %(message)s")
    main()
    
