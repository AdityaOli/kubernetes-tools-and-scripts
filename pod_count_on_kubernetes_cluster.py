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
import json


def send_email(sender,receiver,subject,message):
      me = sender
      you = receiver

      msg = MIMEMultipart('alternative')
      msg['Subject'] = subject
      msg['From'] = me
      msg['To'] = you
      #message="".join(message)
      
      
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
      except Exception:
            print("Error while sending email!")


def Check_Pod_Count_In_Both_Clusters():
      opc1=Check_Pod_Count(<CLUSTER 1>)
      opc2=Check_Pod_Count(<CLUSTER 2>)     
      #output=opc1+opc2
      
      output=[]
      
      for eachline in opc1:
            output.append(eachline)
      for eachline in opc2:
            output.append(eachline)
      #print(output)      

      message=""
      for eachNode in output:

            if(float(eachNode['Used'])/float(eachNode['Total'])>=0.9):
                  message=message+"<span style='color:red'>"+eachNode['ServerName']+" : "+eachNode['Used']+"/"+eachNode['Total']+"</span></br>"
                  
            elif(float(eachNode['Used'])/float(eachNode['Total'])>=0.7 and (float(eachNode['Used'])/float(eachNode['Total']))<0.9):
                  message=message+"<span style='color:#ffbf00'>"+eachNode['ServerName']+" : "+eachNode['Used']+"/"+eachNode['Total']+"</span></br>"
            else:
                  message=message+"<span style='color:green'>"+eachNode['ServerName']+" : "+eachNode['Used']+"/"+eachNode['Total']+"</span></br>"
            
      if opc1 and opc2:
            send_email("K8sBot@YOURCOMPANY.com","YOUREMAIL","Daily | Pod Count Report",message)

def store_to_file(message):
      for everyElement in message:
            print(everyElement)
      
def Check_Pod_Count(cluster):
      finalResponse=""
      outputData=[]
      context=""
      if "cluster1" in cluster:
            context='cluster1-context'
      if "cluster2" in cluster:
            context='cluster2-context'
      
      my_env = os.environ.copy()
      my_env["PATH"] = "/home/olia2-ua:"+my_env["PATH"]
      out=subprocess.Popen(['LOGIN TO CLUSTER 1'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=my_env)    
      out, err = out.communicate()
      print(out)
      out=subprocess.Popen(['kubectl','config','use-context',context], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=my_env)    
      out, err = out.communicate()
      print(out)
      out=subprocess.Popen(['kubectl', 'get', 'namespaces', "-o=jsonpath=\"{.items[*]['metadata.name']}\""], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=my_env)
      out, err = out.communicate()
      print(out)
      out=out.replace("\"","").split(' ')      
      all_namespaces=out
      podCountDict={}
      for eachNamespace in all_namespaces:
            out=subprocess.Popen(['kubectl', 'get', 'pods', '-n',eachNamespace,'-o','wide'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=my_env)
            out, err = out.communicate()
            eachNamespace=("\n").join(out.split("\n")[1:])
            eachPod=eachNamespace.split("\n")
            for pod in eachPod:
                  pod=pod.split(" ")
                  pod=[x for x in pod if x]
                  if len(pod)==8:
                        if pod[6] in podCountDict:
                              podCountDict[pod[6]]+=1
                        else:
                              podCountDict[pod[6]]=1
    
      for eachNode in podCountDict:
            finalString=""
            tempOutputData={}
            out=subprocess.Popen(['kubectl','get', 'node',eachNode,'-o','json'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=my_env)
            out, err = out.communicate()
            #print(err)
            out=json.loads(out)
            used=str(podCountDict[eachNode])
            if float(used)/float(out["status"]["capacity"]["pods"]) > 0.90:
                  #finalString="<span style='color:red'><strong>"+out["metadata"]["name"]+" : "+used+"/"+out["status"]["capacity"]["pods"]+"</strong></span>"
                  finalString=out["metadata"]["name"]+" : "+used+"/"+out["status"]["capacity"]["pods"]
                  tempOutputData["ServerName"]=out["metadata"]["name"]
                  tempOutputData["Used"]=used
                  tempOutputData["Total"]=out["status"]["capacity"]["pods"]
                  outputData.append(tempOutputData)
            else:
                  finalString=out["metadata"]["name"]+" : "+used+"/"+out["status"]["capacity"]["pods"]
                  tempOutputData["ServerName"]=out["metadata"]["name"]
                  tempOutputData["Used"]=used
                  tempOutputData["Total"]=out["status"]["capacity"]["pods"]
                  outputData.append(tempOutputData)
            finalResponse=finalResponse+finalString+"\n"
      return outputData
      
def main():

      Check_Pod_Count_In_Both_Clusters()
        
if __name__ == "__main__":
    main()
